import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer

_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
_VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), 'vectorizer.pkl')

_model = None
_vectorizer = None

def _load_artifacts():
    """Load model and vectorizer if not already loaded."""
    global _model, _vectorizer
    if _model is None:
        if not os.path.exists(_MODEL_PATH):
            raise FileNotFoundError(
                f"Model file '{_MODEL_PATH}' not found. Run train_model.py first.")
        _model = joblib.load(_MODEL_PATH)
    if _vectorizer is None:
        if not os.path.exists(_VECTORIZER_PATH):
            raise FileNotFoundError(
                f"Vectorizer file '{_VECTORIZER_PATH}' not found. Run train_model.py first.")
        _vectorizer = joblib.load(_VECTORIZER_PATH)


def predict(text: str) -> str:
    """Return emotion label for given text."""
    _load_artifacts()
    vec = _vectorizer.transform([text])
    return _model.predict(vec)[0]
