import os
import joblib

# Import your training routine
from train_model import main as train_and_serialize_artifacts

# --- Paths to artifacts ---
# The training script now exports a single Pipeline object which includes
# both the TF-IDF vectorizer and the classifier.
_MODEL_PATH = os.path.join(os.path.dirname(__file__), "best_model.pkl")

# --- In-memory cache ---
_model = None

def _train_and_serialize():
    """Run the training routine and load the resulting pipeline."""
    # train_model.py writes out ``best_model.pkl``
    train_and_serialize_artifacts()

    # load the serialized pipeline
    model = joblib.load(_MODEL_PATH)
    return model


def _load_artifacts():
    """Load the model pipeline. Raise if artifacts are missing."""
    global _model

    if not os.path.exists(_MODEL_PATH):
        raise FileNotFoundError(
            "Model artifact 'best_model.pkl' not found. "
            "Run 'python train_model.py' to train and create it."
        )

    if _model is None:
        _model = joblib.load(_MODEL_PATH)

def predict(text: str) -> str:
    """Predict the emotion label for the given text."""
    _load_artifacts()
    return _model.predict([text])[0]
