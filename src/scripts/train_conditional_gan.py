import sys
import os
import argparse
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
from lib.gan_trainer import ConditionalGANTrainer
from lib.conditional_dataset import create_conditional_dataloader

def parse_args():
    parser = argparse.ArgumentParser(description='Train Conditional GAN for Abstract Art Generation')
    
    # Data parameters
    parser.add_argument('--data_dir', type=str, default='abstract_art_512',
                       help='Path to dataset directory')
    parser.add_argument('--cluster_mapping', type=str, default='clustering_results/cluster_mapping.json',
                       help='Path to cluster mapping JSON file')
    
    # Model parameters
    parser.add_argument('--latent_dim', type=int, default=128,
                       help='Latent dimension for generator')
    parser.add_argument('--num_styles', type=int, default=15,
                       help='Number of art styles/clusters')
    parser.add_argument('--img_size', type=int, default=512,
                       help='Image size (height and width)')
    
    # Training parameters (tuned for cluster imbalance and RTX 3050)
    parser.add_argument('--batch_size', type=int, default=3,
                       help='Batch size for training (reduced for 512x512 images)')
    parser.add_argument('--num_epochs', type=int, default=100,
                       help='Number of training epochs')
    parser.add_argument('--lr_g', type=float, default=0.0001,
                       help='Learning rate for generator (conservative for stability)')
    parser.add_argument('--lr_d', type=float, default=0.0001,
                       help='Learning rate for discriminator')
    parser.add_argument('--lambda_style', type=float, default=8.0,
                       help='Weight for style consistency loss (higher for imbalanced clusters)')
    
    # Logging and saving
    parser.add_argument('--save_dir', type=str, default='gan_training',
                       help='Directory to save training results')
    parser.add_argument('--log_interval', type=int, default=20,
                       help='Steps between logging')
    parser.add_argument('--save_interval', type=int, default=200,
                       help='Steps between saving samples')
    
    # Hardware
    parser.add_argument('--num_workers', type=int, default=2,
                       help='Number of data loading workers')
    parser.add_argument('--device', type=str, default='auto',
                       help='Training device (cuda/cpu/auto)')
    
    # Resume training
    parser.add_argument('--resume', type=str, default=None,
                       help='Path to checkpoint to resume from')
    
    return parser.parse_args()

def create_mock_cluster_mapping(data_dir, num_styles=15):
    """Create a mock cluster mapping for testing when clustering results are not available"""
    print("Creating mock cluster mapping for testing...")
    
    import os
    import random
    
    image_files = [f for f in os.listdir(data_dir) if f.endswith('.jpg')]
    
    # Randomly assign styles for testing
    cluster_mapping = {}
    for filename in image_files:
        cluster_mapping[filename] = random.randint(0, num_styles - 1)
    
    return cluster_mapping

def main():
    args = parse_args()
    
    # Setup device
    if args.device == 'auto':
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    else:
        device = torch.device(args.device)
    
    print(f"Using device: {device}")
    
    # Get absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    data_dir = os.path.join(project_root, args.data_dir)
    cluster_mapping_path = os.path.join(project_root, args.cluster_mapping)
    save_dir = os.path.join(project_root, args.save_dir)
    
    # Check if data exists
    if not os.path.exists(data_dir):
        print(f"Error: Dataset directory not found at {data_dir}")
        sys.exit(1)
    
    # Handle cluster mapping
    if not os.path.exists(cluster_mapping_path):
        print(f"Warning: Cluster mapping not found at {cluster_mapping_path}")
        print("Creating mock cluster mapping for testing...")
        
        # Create mock mapping and save it
        cluster_mapping = create_mock_cluster_mapping(data_dir, args.num_styles)
        
        os.makedirs(os.path.dirname(cluster_mapping_path), exist_ok=True)
        with open(cluster_mapping_path, 'w') as f:
            json.dump(cluster_mapping, f, indent=2)
        
        print(f"Mock cluster mapping saved to {cluster_mapping_path}")
    
    # Create data loader with cluster-aware sampling
    print("Creating data loader...")
    try:
        dataloader, dataset = create_conditional_dataloader(
            data_dir=data_dir,
            cluster_mapping_path=cluster_mapping_path,
            batch_size=args.batch_size,
            num_workers=args.num_workers
        )
        print(f"Data loader created successfully!")
        print(f"Dataset size: {len(dataset)} images")
        
        # Analyze cluster distribution for parameter tuning
        cluster_stats_path = os.path.join(project_root, 'clustering_results', 'cluster_stats.json')
        if os.path.exists(cluster_stats_path):
            with open(cluster_stats_path, 'r') as f:
                cluster_stats = json.load(f)
            
            # Calculate class weights for imbalanced clusters
            total_images = sum(stats['count'] for stats in cluster_stats.values())
            min_count = min(stats['count'] for stats in cluster_stats.values())
            max_count = max(stats['count'] for stats in cluster_stats.values())
            
            print(f"\nCluster Analysis:")
            print(f"Total images: {total_images}")
            print(f"Smallest cluster: {min_count} images")
            print(f"Largest cluster: {max_count} images")
            print(f"Imbalance ratio: {max_count/min_count:.1f}:1")
            
            # Adjust lambda_style based on imbalance
            imbalance_ratio = max_count / min_count
            if imbalance_ratio > 5:
                args.lambda_style = args.lambda_style * 1.5  # Increase style loss weight for imbalanced data
                print(f"Increased style loss weight to {args.lambda_style} due to cluster imbalance")
        
    except Exception as e:
        print(f"Error creating data loader: {e}")
        sys.exit(1)
    
    # Clear any existing cached models to avoid architecture mismatch
    if os.path.exists(save_dir):
        import shutil
        print(f"Clearing existing training directory to avoid architecture conflicts...")
        shutil.rmtree(save_dir)
    
    # Initialize trainer with fresh weights
    print("Initializing GAN trainer...")
    trainer = ConditionalGANTrainer(
        latent_dim=args.latent_dim,
        num_styles=args.num_styles,
        img_size=args.img_size,
        lr_g=args.lr_g,
        lr_d=args.lr_d,
        lambda_style=args.lambda_style,
        device=device
    )
    
    # Resume from checkpoint if specified
    start_epoch = 0
    if args.resume:
        if os.path.exists(args.resume):
            start_epoch = trainer.load_checkpoint(args.resume)
            print(f"Resumed training from epoch {start_epoch}")
        else:
            print(f"Warning: Checkpoint not found at {args.resume}, starting from scratch")
    
    # Save training configuration
    os.makedirs(save_dir, exist_ok=True)
    config = vars(args)
    config['device'] = str(device)
    config['dataset_size'] = len(dataset)
    config['start_epoch'] = start_epoch
    
    with open(os.path.join(save_dir, 'training_config.json'), 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"Training configuration saved to {save_dir}/training_config.json")
    
    # Start training
    print("Starting training...")
    trainer.train(
        dataloader=dataloader,
        num_epochs=args.num_epochs,
        save_dir=save_dir,
        log_interval=args.log_interval,
        save_interval=args.save_interval
    )

if __name__ == "__main__":
    main() 