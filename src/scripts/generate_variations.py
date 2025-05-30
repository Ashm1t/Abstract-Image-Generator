#!/usr/bin/env python3
"""
🎨 Fast Abstract Art Variation Generator

Welcome to the magic behind the beautiful blue UI! This script creates stunning art variations
using neural style transfer with your 15 discovered art styles.

The best part? No training required - we use your existing clustering work for instant results! ⚡

How it works:
1. 🔍 Loads your clustered art styles from clustering_results/
2. 🎨 Picks sample images from your chosen style
3. ✨ Applies neural style transfer magic (fast LAB color space method)
4. 🎯 Enhances based on style characteristics
5. 💾 Saves your beautiful new artwork

Made with ❤️ and a lot of ☕
"""

import os
import sys
import json
import random
import argparse
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import torch
import torchvision.transforms as transforms
from datetime import datetime

def load_cluster_mapping():
    """
    🗂️ Load the cluster mapping from your clustering results
    
    This tells us which images belong to which of our 15 discovered art styles.
    Without this file, we can't work our magic!
    """
    try:
        with open('clustering_results/cluster_mapping.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("😅 Oops! We can't find your clustering results!")
        print("Make sure clustering_results/cluster_mapping.json exists.")
        print("Have you run the clustering analysis yet?")
        sys.exit(1)

def get_style_images(style_id, cluster_mapping, max_images=50):
    """
    🎯 Get all the images that belong to a specific art style
    
    We limit to 50 images max for performance - nobody wants to wait forever! ⏰
    """
    style_images = []
    for image_path, cluster in cluster_mapping.items():
        if cluster == style_id:
            full_path = os.path.join('abstract_art_512', image_path)
            if os.path.exists(full_path):
                style_images.append(full_path)
    
    # 🎲 Shuffle and limit for variety and performance
    if len(style_images) > max_images:
        style_images = random.sample(style_images, max_images)
    
    return style_images

def apply_neural_style_transfer(content_img, style_img, strength=0.7):
    """
    🧠✨ Fast neural style transfer using color magic!
    
    This is where the real magic happens. We use LAB color space to transfer
    the style's colors to the content image while preserving its structure.
    
    It's like giving your artwork a makeover! 💄
    """
    # 📏 Make sure both images are the same size for blending
    content_img = content_img.resize((512, 512), Image.Resampling.LANCZOS)
    style_img = style_img.resize((512, 512), Image.Resampling.LANCZOS)
    
    # 🔬 Convert to LAB color space (L=lightness, A=green-red, B=blue-yellow)
    content_lab = content_img.convert('LAB')
    style_lab = style_img.convert('LAB')
    
    # 🎭 Split into separate channels
    content_l, content_a, content_b = content_lab.split()
    style_l, style_a, style_b = style_lab.split()
    
    # ✨ The magic: keep content's structure (L) but use style's colors (A, B)
    transferred = Image.merge('LAB', (content_l, style_a, style_b)).convert('RGB')
    
    # 🎛️ Blend with original for control (strength determines how much style to apply)
    result = Image.blend(content_img, transferred, strength)
    
    # 🎨 Add some style-specific enhancements for extra pizzazz
    result = enhance_for_style(result, get_style_characteristics(style_img))
    
    return result

def get_style_characteristics(style_img):
    """
    🔍 Analyze an image to understand its visual personality
    
    We look at colors, contrast, brightness - everything that makes this style unique!
    This helps us apply the right enhancements later.
    """
    # 🔢 Convert to numbers for analysis
    img_array = np.array(style_img)
    
    # 🌈 Color analysis - what colors dominate?
    avg_color = np.mean(img_array, axis=(0,1))
    color_variance = np.var(img_array, axis=(0,1))
    
    # 💡 Brightness and contrast analysis
    gray = style_img.convert('L')
    gray_array = np.array(gray)
    contrast = np.std(gray_array)
    brightness = np.mean(gray_array)
    
    return {
        'avg_color': avg_color,
        'color_variance': color_variance,
        'contrast': contrast,
        'brightness': brightness,
        'is_warm': avg_color[0] > avg_color[2],  # More red than blue = warm
        'is_high_contrast': contrast > 50,       # Bold vs subtle
        'is_bright': brightness > 128            # Light vs dark
    }

def enhance_for_style(img, characteristics):
    """
    🎨 Apply smart enhancements based on the style's personality
    
    High contrast styles get more drama, warm styles get color boosts, etc.
    It's like having an AI art director! 🎬
    """
    result = img.copy()
    
    # 🎭 Contrast enhancement based on style
    if characteristics['is_high_contrast']:
        result = ImageEnhance.Contrast(result).enhance(1.3)  # More drama!
    else:
        result = ImageEnhance.Contrast(result).enhance(1.1)  # Gentle enhancement
    
    # 🌈 Color enhancement for variety
    if characteristics['color_variance'].mean() > 1000:  # Lots of different colors
        result = ImageEnhance.Color(result).enhance(1.2)    # Make them pop!
    
    # ☀️ Brightness adjustments
    if characteristics['is_bright']:
        result = ImageEnhance.Brightness(result).enhance(1.1)   # Even brighter!
    else:
        result = ImageEnhance.Brightness(result).enhance(0.95)  # Slightly darker
    
    # 🔧 Filters for texture
    if characteristics['is_high_contrast']:
        result = result.filter(ImageFilter.EDGE_ENHANCE_MORE)  # Sharp and crisp
    else:
        result = result.filter(ImageFilter.SMOOTH)            # Soft and smooth
    
    return result

def generate_style_variation(style_id, variation_type='blend', seed=None):
    """
    🎨 The main event! Generate a beautiful art variation
    
    This orchestrates everything - loading images, applying effects, and creating magic!
    """
    if seed is not None:
        # 🎲 Set random seed for reproducible results (useful for testing)
        random.seed(seed)
        np.random.seed(seed)
    
    # 📂 Load up our style mapping
    cluster_mapping = load_cluster_mapping()
    
    # 🎯 Get images for our chosen style
    style_images = get_style_images(style_id, cluster_mapping)
    
    if len(style_images) < 2:
        raise ValueError(f"😅 Not enough images for style {style_id}! Found only {len(style_images)} images. Need at least 2 to work with.")
    
    # 🎭 Now for the fun part - create variations based on type!
    
    if variation_type == 'blend':
        # 🌀 Blend two images from the same style - smooth and harmonious
        img1_path = random.choice(style_images)
        img2_path = random.choice([img for img in style_images if img != img1_path])
        
        img1 = Image.open(img1_path).convert('RGB')
        img2 = Image.open(img2_path).convert('RGB')
        
        # 📏 Resize for consistency
        img1 = img1.resize((512, 512), Image.Resampling.LANCZOS)
        img2 = img2.resize((512, 512), Image.Resampling.LANCZOS)
        
        # 🎛️ Blend with a random amount (30-70% mix)
        alpha = random.uniform(0.3, 0.7)
        result = Image.blend(img1, img2, alpha)
        
    elif variation_type == 'filter':
        # ✨ Apply style-specific filters - enhance what's already there
        img_path = random.choice(style_images)
        img = Image.open(img_path).convert('RGB').resize((512, 512), Image.Resampling.LANCZOS)
        
        characteristics = get_style_characteristics(img)
        result = enhance_for_style(img, characteristics)
        
    elif variation_type == 'color_morph':
        # 🎨 Color transfer magic between two images
        content_path = random.choice(style_images)
        style_path = random.choice([img for img in style_images if img != content_path])
        
        content_img = Image.open(content_path).convert('RGB')
        style_img = Image.open(style_path).convert('RGB')
        
        result = apply_neural_style_transfer(content_img, style_img, strength=0.6)
        
    elif variation_type == 'cross_cluster':
        # 🔀 Mix different styles - the most adventurous option!
        other_style = random.choice([s for s in range(15) if s != style_id])
        other_style_images = get_style_images(other_style, cluster_mapping)
        
        if other_style_images:
            content_path = random.choice(style_images)
            style_path = random.choice(other_style_images)
            
            content_img = Image.open(content_path).convert('RGB')
            style_img = Image.open(style_path).convert('RGB')
            
            # 🎭 Cross-style with moderate strength to keep it interesting but not chaotic
            result = apply_neural_style_transfer(content_img, style_img, strength=0.5)
        else:
            # 🔄 Fallback if we can't find other style images
            img_path = random.choice(style_images)
            img = Image.open(img_path).convert('RGB').resize((512, 512), Image.Resampling.LANCZOS)
            result = enhance_for_style(img, get_style_characteristics(img))
    
    elif variation_type == 'mixed':
        # 🎰 Surprise me! Pick a random variation type
        var_type = random.choice(['blend', 'filter', 'color_morph', 'cross_cluster'])
        return generate_style_variation(style_id, var_type, seed)
    
    else:
        raise ValueError(f"🤔 Unknown variation type: {variation_type}")
    
    return result

def main():
    """
    🚀 Command line interface - this is what gets called from the web app!
    """
    parser = argparse.ArgumentParser(
        description='🎨 Generate beautiful abstract art variations using your clustering results!'
    )
    parser.add_argument('--style', type=int, required=True, 
                       help='🎭 Art style ID (0-14) - each one has its own personality!')
    parser.add_argument('--variation_type', type=str, default='mixed',
                       choices=['blend', 'filter', 'color_morph', 'cross_cluster', 'mixed'],
                       help='✨ How should we remix your art? (Default: mixed for surprises!)')
    parser.add_argument('--seed', type=int, 
                       help='🎲 Random seed for reproducible results (optional)')
    parser.add_argument('--output_dir', type=str, default='art_variations',
                       help='📁 Where to save your masterpiece (default: art_variations/)')
    parser.add_argument('--num_variations', type=int, default=1,
                       help='🔢 How many variations to create (default: 1)')
    
    args = parser.parse_args()
    
    # ✅ Validate the style ID
    if args.style < 0 or args.style > 14:
        print("😅 Oops! Style ID must be between 0 and 14.")
        print("We discovered exactly 15 unique art styles (0-14).")
        sys.exit(1)
    
    # 📁 Make sure we have a place to save our art
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 🎉 Let the user know what we're doing
    print(f"Creating {args.num_variations} variation(s) for style {args.style}")
    print(f"Using variation type: {args.variation_type}")
    print(f"Saving to: {args.output_dir}")
    
    # 🎭 Time to create some art!
    for i in range(args.num_variations):
        try:
            variation = generate_style_variation(
                args.style,
                args.variation_type,
                args.seed + i if args.seed is not None else None
            )
            
            # 📝 Generate a unique filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]  # Include milliseconds
            filename = f'variation_{timestamp}_{args.variation_type}_s{args.style}.png'
            output_path = os.path.join(args.output_dir, filename)
            
            # 💾 Save with high quality
            variation.save(output_path, 'PNG', quality=95)
            
            # 📢 Print the path for the web app to pick up
            print(output_path)
            
        except Exception as e:
            print(f"Error creating variation {i+1}: {str(e)}", file=sys.stderr)
            sys.exit(1)

if __name__ == '__main__':
    main() 