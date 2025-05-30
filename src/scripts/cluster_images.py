import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.clustering import cluster_dataset

def main():
    # Get the absolute path to the dataset
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    data_dir = os.path.join(project_root, "abstract_art_512")
    
    if not os.path.exists(data_dir):
        print(f"Error: Dataset directory not found at {data_dir}")
        print("Please make sure the 'abstract_art_512' directory is in the project root.")
        sys.exit(1)
    
    print("Starting clustering analysis...")
    print("-" * 50)
    
    # Run clustering with smaller batch size for debugging
    clusterer, filenames = cluster_dataset(
        data_dir,
        n_clusters=15,
        batch_size=8  # Reduced batch size
    )
    
    print("\nClustering complete! Results saved in 'clustering_results' directory.")

if __name__ == "__main__":
    main() 