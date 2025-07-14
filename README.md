# Emotion Detection

This project trains a Logistic Regression classifier to detect emotions in text and provides a simple web demo using Streamlit.

## Usage

1. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Download the spaCy language model (required before running `train_model.py` or the Streamlit demo):
   ```bash
   python -m spacy download en_core_web_sm
   ```
3. Train the model (this creates `best_model.pkl`):
   ```bash
   python train_model.py
   ```
4. Run the demo app:
   ```bash
   streamlit run app.py
   ```

The training data is provided in `text_emotions.csv`.
