"""Configuration constants for the emotion detection model."""

import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Model configuration
MODEL_NAME = "distilbert-base-uncased"
NUM_LABELS = 7
MAX_LENGTH = 128
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
NUM_EPOCHS = 3
WARMUP_STEPS = 500

# Emotion labels (alphabetical order for consistent label encoding)
EMOTIONS = [
    "anger",
    "fear",
    "joy",
    "love",
    "neutral",
    "sadness",
    "surprise",
]

# Label mappings
LABEL2ID = {label: i for i, label in enumerate(EMOTIONS)}
ID2LABEL = {i: label for i, label in enumerate(EMOTIONS)}

# Paths
MODEL_DIR = os.path.join(BASE_DIR, "models", "emotion_distilbert")
DATA_DIR = os.path.join(BASE_DIR, "data")
ORIGINAL_DATA_PATH = os.path.join(BASE_DIR, "text_emotions.csv")
AUGMENTED_DATA_PATH = os.path.join(DATA_DIR, "text_emotions_with_neutral.csv")
