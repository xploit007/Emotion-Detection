import streamlit as st
import model

# --- Page config ---
st.set_page_config(
    page_title="Emotion Detection 🎭",
    page_icon="🤖",
    layout="centered",
)

# --- Custom CSS ---
st.markdown(
    """
    <style>
    .main {
        background-color: #121212;
        color: #FFFFFF;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-size: 1.1em;
    }
    .stButton button:hover {
        background-color: #45A049;
    }
    .emotion-box {
        border: 2px solid #4CAF50;
        border-radius: 12px;
        padding: 1em;
        margin-top: 1em;
        text-align: center;
        font-size: 1.3em;
        background-color: #1e1e1e;
    }
    .header-banner {
        text-align: center;
        padding: 1.5em 0;
        background: linear-gradient(90deg, #4CAF50, #81C784);
        border-radius: 8px;
        color: white;
        margin-bottom: 1em;
    }
    .metrics-box {
        background-color: #1e1e1e;
        padding: 1em;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        margin-bottom: 1em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Emoji map ---
EMOJI = {
    "joy": "😂",
    "sadness": "😢",
    "anger": "😠",
    "fear": "😨",
    "surprise": "😲",
    "disgust": "🤢",
    "love": "😍",
}

# --- Header Banner ---
st.markdown(
    """
    <div class="header-banner">
        <h1>🎭 Emotion Detection Demo</h1>
        <p>Discover the emotion behind your words</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Metrics Box ---
st.markdown(
    """
    <div class="metrics-box">
    <strong>Note:</strong> This is just a demo and may not always be accurate.<br>
    • Accuracy: 86.18%<br>
    • Precision: 88.30%<br>
    • Recall: 76.66%<br>
    • F1-score: 80.93%<br><br>
    I am continuously working to improve the model's accuracy and expand its capabilities. Thank you for trying it out!
    </div>
    """,
    unsafe_allow_html=True,
)


# --- Text Input ---
text = st.text_area(
    "Enter your text below:",
    height=150,
    placeholder="Type something to analyze its emotion...",
)

# --- Predict Button ---
if st.button("🔍 Predict Emotion"):
    if text.strip() == "":
        st.warning("Please enter some text.")
    else:
        with st.spinner("Analyzing..."):
            label = model.predict(text).lower()

        emoji = EMOJI.get(label, "")

        # --- Styled Result ---
        st.markdown(
            f"""
            <div class="emotion-box">
                {emoji} <strong>Predicted Emotion:</strong> {label.capitalize()}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # --- Emotion-specific Messages ---
        if label == "joy":
            st.success("😂 That's wonderful! Keep the joy going!")
        elif label == "sadness":
            st.warning("😢 It's okay to feel sad. Take care of yourself.")
        elif label == "anger":
            st.error("😡 Take a deep breath and let it out slowly.")
        elif label == "fear":
            st.warning("😨 Stay strong, you’ve got this.")
        elif label == "surprise":
            st.info("😲 Wow, that’s surprising!")
        elif label == "love":
            st.info("😍 Love is a beautiful emotion, spread it around!")
        elif label == "disgust":
            st.warning("🤢 Take a moment to process and release that feeling.")
