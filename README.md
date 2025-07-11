# Emotion Detection

This project trains a Logistic Regression classifier to detect emotions in text and provides a simple web demo using Streamlit.

## Usage

1. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Train the model (this creates `model.pkl` and `vectorizer.pkl`):
   ```bash
   python train_model.py
   ```

3. Run the demo app:
   ```bash
   streamlit run app.py
   ```

The training data is provided in `text_emotions.csv`.
