import sys
import os
import pickle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from lib.save_clusters import save_clustering_results, create_style_labeled_dataset

def main():
    # Get paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    # Load clustering results
    clustering_results_path = os.path.join(project_root, 'clustering_results', 'clusterer.pkl')
    filenames_path = os.path.join(project_root, 'clustering_results', 'filenames.npy')
    
    if not os.path.exists(clustering_results_path):
        print("Error: Clustering results not found. Please run clustering first.")
        sys.exit(1)
    
    # Load data
    with open(clustering_results_path, 'rb') as f:
        clusterer = pickle.load(f)
    
    filenames = np.load(filenames_path)
    
    # Paths
    data_dir = os.path.join(project_root, 'abstract_art_512')
    output_dir = os.path.join(project_root, 'clustering_results')
    
    print("Saving clustering results...")
    
    # Save clustering results properly
    cluster_mapping, cluster_stats = save_clustering_results(clusterer, filenames, output_dir)
    
    print('Clustering results saved successfully!')
    print(f'Total images: {len(cluster_mapping)}')
    print(f'Number of styles: {len(cluster_stats)}')
    
    # Print cluster distribution
    print("\nStyle distribution:")
    for style_id in sorted(cluster_stats.keys()):
        count = cluster_stats[style_id]['count']
        percentage = cluster_stats[style_id]['percentage']
        print(f"Style {style_id}: {count} images ({percentage:.1f}%)")

if __name__ == "__main__":
    main() 