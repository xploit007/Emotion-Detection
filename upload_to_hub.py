"""
Upload the trained model to HuggingFace Hub.

Usage:
    1. Login to HuggingFace: huggingface-cli login
    2. Run this script: python upload_to_hub.py
"""

from huggingface_hub import HfApi, create_repo
import os

# Configuration
REPO_ID = "xploit007/emotion-detection-distilbert"
MODEL_DIR = "models/emotion_distilbert"

def upload_model():
    """Upload model to HuggingFace Hub."""
    api = HfApi()

    # Create the repository (if it doesn't exist)
    try:
        create_repo(repo_id=REPO_ID, exist_ok=True, private=False)
        print(f"Repository created/exists: https://huggingface.co/{REPO_ID}")
    except Exception as e:
        print(f"Note: {e}")

    # Upload the model folder
    print(f"\nUploading model from {MODEL_DIR}...")
    api.upload_folder(
        folder_path=MODEL_DIR,
        repo_id=REPO_ID,
        repo_type="model",
    )

    print(f"\nModel uploaded successfully!")
    print(f"View at: https://huggingface.co/{REPO_ID}")

if __name__ == "__main__":
    if not os.path.exists(MODEL_DIR):
        print(f"Error: Model directory '{MODEL_DIR}' not found.")
        print("Run 'python train_bert.py' first to train the model.")
    else:
        upload_model()
