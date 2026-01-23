import streamlit as st
import model

# --- Page config ---
st.set_page_config(
    page_title="Emotion Detection AI",
    page_icon="🎭",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- Emotion Configuration ---
EMOTIONS_CONFIG = {
    "joy": {"emoji": "😁", "color": "#FFD700", "bg": "linear-gradient(135deg, #FFD700, #FFA500)", "message": "That's wonderful! Keep spreading the positivity!"},
    "sadness": {"emoji": "😢", "color": "#6B8DD6", "bg": "linear-gradient(135deg, #6B8DD6, #8E7CC3)", "message": "It's okay to feel sad. Take care of yourself."},
    "anger": {"emoji": "😠", "color": "#E74C3C", "bg": "linear-gradient(135deg, #E74C3C, #C0392B)", "message": "Take a deep breath. This too shall pass."},
    "fear": {"emoji": "😨", "color": "#9B59B6", "bg": "linear-gradient(135deg, #9B59B6, #8E44AD)", "message": "You're braver than you believe. Stay strong!"},
    "surprise": {"emoji": "😲", "color": "#F39C12", "bg": "linear-gradient(135deg, #F39C12, #E67E22)", "message": "Life is full of surprises! Embrace them."},
    "love": {"emoji": "😍", "color": "#E91E63", "bg": "linear-gradient(135deg, #E91E63, #FF6B6B)", "message": "Love is beautiful! Spread it around."},
    "neutral": {"emoji": "😐", "color": "#95A5A6", "bg": "linear-gradient(135deg, #95A5A6, #7F8C8D)", "message": "Just stating the facts. Clear and simple."},
    "disgust": {"emoji": "🤢", "color": "#27AE60", "bg": "linear-gradient(135deg, #27AE60, #2ECC71)", "message": "Take a moment to process that feeling."},
}

# --- Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

    * {
        font-family: 'Poppins', sans-serif;
    }

    .main {
        background: linear-gradient(180deg, #0a0a0a 0%, #1a1a2e 100%);
    }

    .stApp {
        background: linear-gradient(180deg, #0a0a0a 0%, #1a1a2e 100%);
    }

    /* Animated Header */
    .header-container {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradientShift 8s ease infinite;
        padding: 2.5rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .header-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: white;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }

    .header-subtitle {
        font-size: 1.1rem;
        color: rgba(255,255,255,0.9);
        margin-top: 0.5rem;
    }

    /* Stats Cards */
    .stats-container {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
    }

    .stat-card {
        flex: 1;
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }

    .stat-value {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .stat-label {
        font-size: 0.85rem;
        color: rgba(255,255,255,0.6);
        margin-top: 0.3rem;
    }

    /* Input Section */
    .input-section {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }

    .input-label {
        font-size: 1rem;
        font-weight: 500;
        color: rgba(255,255,255,0.8);
        margin-bottom: 0.8rem;
    }

    /* Text Area */
    .stTextArea textarea {
        background: rgba(255,255,255,0.05) !important;
        border: 2px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        color: white !important;
        font-size: 1rem !important;
        padding: 1rem !important;
        transition: border-color 0.3s ease !important;
    }

    .stTextArea textarea:focus {
        border-color: #23a6d5 !important;
        box-shadow: 0 0 20px rgba(35,166,213,0.2) !important;
    }

    /* Button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #00d2ff, #3a7bd5) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0,210,255,0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(0,210,255,0.4) !important;
    }

    /* Result Card */
    .result-card {
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin: 1.5rem 0;
        animation: slideUp 0.5s ease;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    }

    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .result-emoji {
        font-size: 4rem;
        margin-bottom: 0.5rem;
        animation: bounce 1s ease infinite;
    }

    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    .result-label {
        font-size: 1.8rem;
        font-weight: 700;
        color: white;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .result-message {
        font-size: 1rem;
        color: rgba(255,255,255,0.9);
        margin-top: 1rem;
        font-style: italic;
    }

    /* Confidence Bars */
    .confidence-container {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 1.5rem;
    }

    .confidence-title {
        font-size: 1rem;
        font-weight: 600;
        color: rgba(255,255,255,0.8);
        margin-bottom: 1rem;
    }

    .confidence-bar-wrapper {
        margin-bottom: 0.8rem;
    }

    .confidence-bar-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.3rem;
        font-size: 0.85rem;
    }

    .confidence-bar-label span:first-child {
        color: rgba(255,255,255,0.7);
    }

    .confidence-bar-label span:last-child {
        color: rgba(255,255,255,0.5);
    }

    .confidence-bar {
        height: 8px;
        background: rgba(255,255,255,0.1);
        border-radius: 4px;
        overflow: hidden;
    }

    .confidence-bar-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.8s ease;
    }

    /* Example Buttons */
    .examples-container {
        margin-bottom: 1.5rem;
    }

    .examples-title {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.5);
        margin-bottom: 0.8rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: rgba(255,255,255,0.4);
        font-size: 0.85rem;
    }

    .footer a {
        color: #23a6d5;
        text-decoration: none;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🎭 Emotion Detection AI</h1>
    <p class="header-subtitle">Powered by DistilBERT Transformer • Analyze emotions in text instantly</p>
</div>
""", unsafe_allow_html=True)

# --- Stats Cards ---
st.markdown("""
<div class="stats-container">
    <div class="stat-card">
        <div class="stat-value">93.5%</div>
        <div class="stat-label">Accuracy</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">91.1%</div>
        <div class="stat-label">F1 Score</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">7</div>
        <div class="stat-label">Emotions</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">~50ms</div>
        <div class="stat-label">Response</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Example Buttons ---
st.markdown('<p class="examples-title">✨ Try these examples:</p>', unsafe_allow_html=True)
example_cols = st.columns(4)
examples = [
    ("😊 Happy", "I just got promoted at work and I'm so excited!"),
    ("😢 Sad", "I miss my best friend who moved away last year"),
    ("😠 Angry", "I can't believe they cancelled my flight without notice!"),
    ("😐 Neutral", "The meeting is scheduled for 3 PM tomorrow"),
]

selected_example = None
for i, (label, text) in enumerate(examples):
    with example_cols[i]:
        if st.button(label, key=f"example_{i}", use_container_width=True):
            selected_example = text

# --- Text Input ---
default_text = selected_example if selected_example else ""
text = st.text_area(
    "Enter your text to analyze:",
    value=default_text,
    height=120,
    placeholder="Type or paste any text here to detect its emotional tone...",
    key="text_input"
)

# --- Analyze Button ---
analyze_clicked = st.button("🔍 Analyze Emotion", use_container_width=True)

# --- Process and Display Results ---
if analyze_clicked or selected_example:
    input_text = text if text.strip() else selected_example

    if input_text and input_text.strip():
        with st.spinner("🧠 Analyzing emotional patterns..."):
            label, confidence_scores = model.predict_with_confidence(input_text)

        emotion_config = EMOTIONS_CONFIG.get(label, EMOTIONS_CONFIG["neutral"])

        # Result Card
        st.markdown(f"""
        <div class="result-card" style="background: {emotion_config['bg']};">
            <div class="result-emoji">{emotion_config['emoji']}</div>
            <div class="result-label">{label}</div>
            <div class="result-message">"{emotion_config['message']}"</div>
        </div>
        """, unsafe_allow_html=True)

        # Confidence Scores
        st.markdown('<div class="confidence-container">', unsafe_allow_html=True)
        st.markdown('<div class="confidence-title">📊 Confidence Breakdown</div>', unsafe_allow_html=True)

        # Sort by confidence
        sorted_scores = sorted(confidence_scores.items(), key=lambda x: x[1], reverse=True)

        bars_html = ""
        for emotion, score in sorted_scores:
            config = EMOTIONS_CONFIG.get(emotion, {"color": "#95A5A6", "emoji": "😐"})
            bars_html += f"""
            <div class="confidence-bar-wrapper">
                <div class="confidence-bar-label">
                    <span>{config['emoji']} {emotion.capitalize()}</span>
                    <span>{score:.1f}%</span>
                </div>
                <div class="confidence-bar">
                    <div class="confidence-bar-fill" style="width: {score}%; background: {config['color']};"></div>
                </div>
            </div>
            """

        st.markdown(bars_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.warning("⚠️ Please enter some text to analyze.")

# --- Footer ---
st.markdown("""
<div class="footer">
    Built with ❤️ using <a href="https://streamlit.io" target="_blank">Streamlit</a> &
    <a href="https://huggingface.co/transformers" target="_blank">HuggingFace Transformers</a>
</div>
""", unsafe_allow_html=True)
