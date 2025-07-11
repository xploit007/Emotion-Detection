import os
import joblib

# Import your training routine
from train_model import main as train_and_serialize_artifacts

# --- Paths to artifacts ---
_MODEL_PATH      = os.path.join(os.path.dirname(__file__), "model.pkl")
_VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), "vectorizer.pkl")

# --- In-memory cache ---
_model      = None
_vectorizer = None

def _train_and_serialize():
    """
    Runs your existing train_model.py logic (which writes model.pkl
    and vectorizer.pkl to disk) and then loads them into memory.
    """
    # train_model.py's main() writes out both model.pkl and vectorizer.pkl
    train_and_serialize_artifacts()

    # now load them
    model      = joblib.load(_MODEL_PATH)
    vectorizer = joblib.load(_VECTORIZER_PATH)
    return model, vectorizer

def _load_artifacts():
    """Load (or if missing, train+load) the model and vectorizer."""
    global _model, _vectorizer

    missing = not (os.path.exists(_MODEL_PATH) and os.path.exists(_VECTORIZER_PATH))
    if missing:
        # train_model.py prints metrics and dumps both .pkl files
        print("Artifacts not found. Training model now…")
        _model, _vectorizer = _train_and_serialize()
        return

    # load once into memory
    if _model is None:
        _model = joblib.load(_MODEL_PATH)
    if _vectorizer is None:
        _vectorizer = joblib.load(_VECTORIZER_PATH)

def predict(text: str) -> str:
    """
    Transform input text and predict its emotion label.
    Will trigger training if artifacts are missing.
    """
    _load_artifacts()
    vec = _vectorizer.transform([text])
    return _model.predict(vec)[0]
