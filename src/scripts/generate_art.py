import sys
import os
import argparse
import torch
import json
from torchvision.utils import save_image, make_grid
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.conditional_gan import ConditionalGenerator

def parse_args():
    parser = argparse.ArgumentParser(description='Generate abstract art using trained conditional GAN')
    
    parser.add_argument('--model_path', type=str, required=True,
                       help='Path to trained generator model (.pth file)')
    parser.add_argument('--style_id', type=int, default=-1,
                       help='Style ID to generate (0-14), -1 for all styles')
    parser.add_argument('--num_samples', type=int, default=8,
                       help='Number of samples to generate per style')
    parser.add_argument('--output_dir', type=str, default='generated_art',
                       help='Directory to save generated images')
    parser.add_argument('--latent_dim', type=int, default=128,
                       help='Latent dimension (must match trained model)')
    parser.add_argument('--num_styles', type=int, default=15,
                       help='Number of styles (must match trained model)')
    parser.add_argument('--img_size', type=int, default=512,
                       help='Image size (must match trained model)')
    parser.add_argument('--device', type=str, default='auto',
                       help='Device to use (cuda/cpu/auto)')
    
    return parser.parse_args()

def load_style_descriptions(style_descriptions_path):
    """Load style descriptions if available"""
    if os.path.exists(style_descriptions_path):
        with open(style_descriptions_path, 'r') as f:
            return json.load(f)
    return None

def generate_images(generator, style_id, num_samples, latent_dim, device):
    """Generate images for a specific style"""
    generator.eval()
    
    with torch.no_grad():
        # Generate random noise
        noise = torch.randn(num_samples, latent_dim, device=device)
        
        # Create style labels
        style_labels = torch.full((num_samples,), style_id, device=device, dtype=torch.long)
        
        # Generate images
        generated_images = generator(noise, style_labels)
        
        # Denormalize for saving
        generated_images = (generated_images + 1) / 2
        generated_images = torch.clamp(generated_images, 0, 1)
    
    return generated_images

def main():
    args = parse_args()
    
    # Setup device
    if args.device == 'auto':
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    else:
        device = torch.device(args.device)
    
    print(f"Using device: {device}")
    
    # Load generator
    print(f"Loading generator from {args.model_path}...")
    generator = ConditionalGenerator(
        latent_dim=args.latent_dim,
        num_styles=args.num_styles,
        img_size=args.img_size
    ).to(device)
    
    try:
        # Try loading as state dict first
        generator.load_state_dict(torch.load(args.model_path, map_location=device))
        print("Loaded generator state dict successfully")
    except:
        try:
            # Try loading as full checkpoint
            checkpoint = torch.load(args.model_path, map_location=device)
            generator.load_state_dict(checkpoint['generator_state_dict'])
            print("Loaded generator from checkpoint successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            sys.exit(1)
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Load style descriptions
    style_descriptions_path = "clustering_results/style_descriptions.json"
    style_descriptions = load_style_descriptions(style_descriptions_path)
    
    # Determine which styles to generate
    if args.style_id == -1:
        styles_to_generate = list(range(args.num_styles))
        print(f"Generating images for all {args.num_styles} styles...")
    else:
        styles_to_generate = [args.style_id]
        print(f"Generating images for style {args.style_id}...")
    
    # Generate images
    all_generated = []
    style_labels = []
    
    for style_id in styles_to_generate:
        print(f"Generating {args.num_samples} images for style {style_id}...")
        
        # Get style description
        if style_descriptions and str(style_id) in style_descriptions:
            style_desc = style_descriptions[str(style_id)]
            print(f"Style {style_id}: {style_desc}")
        
        # Generate images
        generated = generate_images(generator, style_id, args.num_samples, args.latent_dim, device)
        all_generated.append(generated)
        style_labels.extend([style_id] * args.num_samples)
        
        # Save individual style grid
        style_grid = make_grid(generated, nrow=min(4, args.num_samples), padding=2)
        style_output_path = os.path.join(args.output_dir, f'style_{style_id:02d}_samples.png')
        save_image(style_grid, style_output_path)
        print(f"Saved style {style_id} samples to {style_output_path}")
    
    # Create combined grid if generating multiple styles
    if len(styles_to_generate) > 1:
        all_images = torch.cat(all_generated, dim=0)
        combined_grid = make_grid(all_images, nrow=args.num_samples, padding=2)
        combined_output_path = os.path.join(args.output_dir, 'all_styles_grid.png')
        save_image(combined_grid, combined_output_path)
        print(f"Saved combined grid to {combined_output_path}")
    
    print(f"Generation complete! Images saved to {args.output_dir}")

if __name__ == "__main__":
    main() 