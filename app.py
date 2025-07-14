import streamlit as st
import model

# --- Page config ---
st.set_page_config(
    page_title="Emotion Detection 🎭",
    page_icon="🤖",
    layout="centered",
)

# --- Emoji map for each emotion label ---
EMOJI = {
    "joy": "😂",
    "sadness": "😢",
    "anger": "😠",
    "fear": "😨",
    "surprise": "😲",
    "disgust": "🤢",
    # add more as your model supports them
}

# --- App UI ---
st.title("Emotion Detection Demo")

# — Disclaimer with metrics —
st.info(
    """
    **Note:** This is just a demo and may not always be accurate.  
    • Accuracy: 86.18%  
    • Precision: 88.30%  
    • Recall: 76.66%  
    • F1-score: 80.93%
    """
)

text = st.text_area("Enter your text here:", height=150)

if st.button("Predict Emotion"):
    with st.spinner("Analyzing…"):
        label = model.predict(text).lower()
    emoji = EMOJI.get(label, "")

    # Styled result
    st.markdown(
        f"<h2 style='text-align:center;'>{emoji} Predicted emotion: "
        f"<span style='color:#4caf50;'>{label.capitalize()}</span></h2>",
        unsafe_allow_html=True,
    )

    # Emotion‐specific messages
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