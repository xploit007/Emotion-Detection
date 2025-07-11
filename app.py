import streamlit as st
import model

st.title("Emotion Detection Demo")
text = st.text_input("Enter text")
if st.button("Predict"):
    label = model.predict(text)
    st.write("Predicted emotion:", label)
