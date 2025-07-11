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

text = st.text_area("Enter your text here:", height=150)

if st.button("Predict Emotion"):
    with st.spinner("Analyzing…"):
        label = model.predict(text).lower()
    emoji = EMOJI.get(label, "")
    
    # Styled result
    st.markdown(
        f"<h2 style='text-align:center;'>{emoji} Predicted emotion: <span style='color:#4caf50;'>{label.capitalize()}</span></h2>",
        unsafe_allow_html=True
    )
    
    # Bonus animation for joy
    if label == "joy":
        st.balloons()
    elif label == "sadness":
        st.snow()
    elif label == "anger":
        st.error("😡 Take a deep breath!")
    # …and so on
