"""
Emotion detection model inference module.

Supports DistilBERT transformer model with automatic device detection.
Downloads model from HuggingFace Hub if not available locally.
"""

import os
import re
import torch
from typing import Dict, Tuple

from config import MODEL_DIR, EMOTIONS, MAX_LENGTH

# HuggingFace Hub repository for the model
HF_REPO_ID = "xploit007/emotion-detection-distilbert"

# --- Global cache ---
_model = None
_tokenizer = None
_device = None


def _get_device():
    """Determine the best available device."""
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def _minimal_clean(text: str) -> str:
    """Minimal preprocessing for BERT input."""
    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)
    # Remove @mentions
    text = re.sub(r"@\w+", "", text)
    # Normalize whitespace
    text = " ".join(text.split())
    return text.strip()


def _download_model_from_hub():
    """Download model from HuggingFace Hub."""
    from huggingface_hub import snapshot_download

    print(f"Downloading model from HuggingFace Hub: {HF_REPO_ID}...")
    snapshot_download(
        repo_id=HF_REPO_ID,
        local_dir=MODEL_DIR,
        local_dir_use_symlinks=False,
    )
    print("Model downloaded successfully!")


def _load_model():
    """Load the model and tokenizer into memory."""
    global _model, _tokenizer, _device

    if _model is not None:
        return

    # Check if model exists locally, if not download from HuggingFace
    model_config_path = os.path.join(MODEL_DIR, "config.json")
    if not os.path.exists(model_config_path):
        os.makedirs(MODEL_DIR, exist_ok=True)
        _download_model_from_hub()

    # Import here to avoid slow startup if model not needed
    from transformers import (
        DistilBertTokenizer,
        DistilBertForSequenceClassification,
    )

    _device = _get_device()

    _tokenizer = DistilBertTokenizer.from_pretrained(MODEL_DIR)
    _model = DistilBertForSequenceClassification.from_pretrained(MODEL_DIR)
    _model.to(_device)
    _model.eval()


def predict(text: str) -> str:
    """
    Predict the emotion label for the given text.

    Args:
        text: Input text to classify

    Returns:
        Predicted emotion label (one of 7 emotions)
    """
    _load_model()

    # Preprocess
    clean_text = _minimal_clean(text)

    # Tokenize
    inputs = _tokenizer(
        clean_text,
        padding="max_length",
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="pt",
    )
    inputs = {k: v.to(_device) for k, v in inputs.items()}

    # Inference
    with torch.no_grad():
        outputs = _model(**inputs)
        prediction = torch.argmax(outputs.logits, dim=1).item()

    return EMOTIONS[prediction]


def predict_with_confidence(text: str) -> Tuple[str, Dict[str, float]]:
    """
    Predict emotion with confidence scores for all classes.

    Args:
        text: Input text to classify

    Returns:
        Tuple of (predicted_label, {emotion: confidence})
    """
    _load_model()

    clean_text = _minimal_clean(text)

    inputs = _tokenizer(
        clean_text,
        padding="max_length",
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="pt",
    )
    inputs = {k: v.to(_device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = _model(**inputs)
        probabilities = torch.softmax(outputs.logits, dim=1)[0]

    confidence_scores = {
        emotion: round(prob.item() * 100, 2)
        for emotion, prob in zip(EMOTIONS, probabilities)
    }

    predicted_idx = torch.argmax(probabilities).item()
    predicted_label = EMOTIONS[predicted_idx]

    return predicted_label, confidence_scores
