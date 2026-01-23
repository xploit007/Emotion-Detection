"""
Train DistilBERT for emotion classification.

Usage:
    python train_bert.py
"""

import os

# Disable TensorFlow to avoid Keras conflicts
os.environ["USE_TF"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import torch
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, f1_score
from transformers import (
    DistilBertTokenizer,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments,
    EarlyStoppingCallback,
)
from datasets import Dataset

from config import (
    MODEL_NAME,
    NUM_LABELS,
    MAX_LENGTH,
    BATCH_SIZE,
    LEARNING_RATE,
    NUM_EPOCHS,
    EMOTIONS,
    LABEL2ID,
    ID2LABEL,
    MODEL_DIR,
    AUGMENTED_DATA_PATH,
)


def get_device():
    """Determine the best available device."""
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def load_data():
    """Load and prepare the dataset."""
    print(f"Loading data from {AUGMENTED_DATA_PATH}...")
    df = pd.read_csv(AUGMENTED_DATA_PATH)

    # Convert sentiment labels to IDs
    df["label"] = df["sentiment"].map(LABEL2ID)

    # Check for any unmapped labels
    if df["label"].isna().any():
        unknown = df[df["label"].isna()]["sentiment"].unique()
        raise ValueError(f"Unknown sentiment labels found: {unknown}")

    print(f"Data shape: {df.shape}")
    print(f"Label distribution:\n{df['sentiment'].value_counts()}")

    return df


def tokenize_dataset(df, tokenizer):
    """Tokenize the dataset for BERT."""
    dataset = Dataset.from_pandas(df[["content", "label"]])

    def tokenize_function(examples):
        return tokenizer(
            examples["content"],
            padding="max_length",
            truncation=True,
            max_length=MAX_LENGTH,
        )

    tokenized = dataset.map(tokenize_function, batched=True)
    tokenized = tokenized.rename_column("label", "labels")
    tokenized.set_format("torch", columns=["input_ids", "attention_mask", "labels"])

    return tokenized


def compute_metrics(eval_pred):
    """Compute evaluation metrics."""
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)

    accuracy = accuracy_score(labels, predictions)
    f1 = f1_score(labels, predictions, average="macro")

    return {"accuracy": accuracy, "f1_macro": f1}


def train():
    """Main training function."""
    device = get_device()
    print(f"Using device: {device}")

    # Load data
    df = load_data()

    # Split data
    train_df, val_df = train_test_split(
        df, test_size=0.2, random_state=42, stratify=df["label"]
    )
    print(f"Train size: {len(train_df)}, Validation size: {len(val_df)}")

    # Initialize tokenizer
    print(f"Loading tokenizer: {MODEL_NAME}...")
    tokenizer = DistilBertTokenizer.from_pretrained(MODEL_NAME)

    # Tokenize datasets
    print("Tokenizing datasets...")
    train_dataset = tokenize_dataset(train_df, tokenizer)
    val_dataset = tokenize_dataset(val_df, tokenizer)

    # Initialize model
    print(f"Loading model: {MODEL_NAME}...")
    model = DistilBertForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=NUM_LABELS,
        id2label=ID2LABEL,
        label2id=LABEL2ID,
    )
    model.to(device)

    # Create output directory
    os.makedirs(MODEL_DIR, exist_ok=True)

    # Training arguments
    training_args = TrainingArguments(
        output_dir=MODEL_DIR,
        num_train_epochs=NUM_EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        learning_rate=LEARNING_RATE,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir=os.path.join(MODEL_DIR, "logs"),
        logging_steps=100,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1_macro",
        greater_is_better=True,
        fp16=torch.cuda.is_available(),
        report_to="none",
    )

    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)],
    )

    # Train
    print("\nStarting training...")
    trainer.train()

    # Save final model and tokenizer
    print(f"\nSaving model to {MODEL_DIR}...")
    trainer.save_model(MODEL_DIR)
    tokenizer.save_pretrained(MODEL_DIR)

    # Final evaluation
    print("\nFinal Evaluation:")
    results = trainer.evaluate()
    print(f"Accuracy: {results['eval_accuracy']:.4f}")
    print(f"F1 Macro: {results['eval_f1_macro']:.4f}")

    # Detailed classification report
    print("\nGenerating classification report...")
    predictions = trainer.predict(val_dataset)
    preds = np.argmax(predictions.predictions, axis=1)
    labels = predictions.label_ids

    print("\nClassification Report:")
    print(classification_report(labels, preds, target_names=EMOTIONS))

    print("\nTraining complete!")
    return results


if __name__ == "__main__":
    train()
