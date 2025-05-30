import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.data_preparation import analyze_dataset, verify_dataset

def main():
    # Get the absolute path to the dataset
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    data_dir = os.path.join(project_root, "abstract_art_512")
    
    if not os.path.exists(data_dir):
        print(f"Error: Dataset directory not found at {data_dir}")
        print("Please make sure the 'abstract_art_512' directory is in the project root.")
        sys.exit(1)
    
    print("Starting dataset analysis...")
    print("-" * 50)
    
    # Analyze dataset statistics
    analyze_dataset(data_dir)
    
    print("\nVerifying dataset loading...")
    print("-" * 50)
    
    # Verify dataset loading
    verify_dataset(data_dir)

if __name__ == "__main__":
    main() 