import streamlit as st
import pickle

st.set_page_config(
    page_title="Smart Comment Analyzer - AI Solutions",
    
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_resource
def load_model():
    try:
        with open("bestModel.pickle", "rb") as f:
            return pickle.load(f)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()

model = load_model()

# CSS Styles with Font Awesome and enhanced button
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    body, .main {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: #f5f7fa;
        color: #222;
    }
    .credits {
        text-align: right;
        margin-bottom: 0.5rem;
        font-size: 1.5rem;
        color: #555;
        font-style: italic;
    }
    .header {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(42,82,152,0.3);
        user-select: none;
    }
    textarea {
        border: 2px solid #2a5298 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        font-size: 1.1rem !important;
        background-color: #fff !important;
        resize: vertical !important;
        min-height: 150px !important;
        transition: border-color 0.3s ease;
        width: 100%;
    }
    textarea:focus {
        border-color: #1e3c72 !important;
        box-shadow: 0 0 8px #1e3c72a0 !important;
        outline: none !important;
    }
    button.stButton>button {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: white !important;
        border: none !important;
        padding: 1rem 2.5rem !important;
        font-size: 1.2rem !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(42,82,152,0.3);
        user-select: none;
        width: 100%;
        position: relative;
        overflow: hidden;
    }
    button.stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(42,82,152,0.5);
    }
    button.stButton>button:active {
        transform: translateY(1px);
    }
    button.stButton>button::after {
        content: "";
        position: absolute;
        top: 50%;
        left: 50%;
        width: 5px;
        height: 5px;
        background: rgba(255, 255, 255, 0.5);
        opacity: 0;
        border-radius: 100%;
        transform: scale(1, 1) translate(-50%);
        transform-origin: 50% 50%;
    }
    button.stButton>button:focus:not(:active)::after {
        animation: ripple 1s ease-out;
    }
    @keyframes ripple {
        0% {
            transform: scale(0, 0);
            opacity: 0.5;
        }
        100% {
            transform: scale(20, 20);
            opacity: 0;
        }
    }
    .result-card {
        background: white;
        border-radius: 20px;
        padding: 2rem 3rem;
        box-shadow: 0 10px 30px rgba(42,82,152,0.15);
        height: 100%;
        max-width: 450px;
        margin-left: 3rem;
        user-select: none;
        transition: transform 0.3s ease;
    }
    .result-card:hover {
        transform: translateY(-5px);
    }
    .result-icon {
        font-size: 5rem;
        margin-bottom: 0.5rem;
    }
    .result-label {
        font-weight: 700;
        font-size: 2.25rem;
        margin-bottom: 0.3rem;
    }
    .result-desc {
        font-size: 1.15rem;
        color: #444;
        line-height: 1.4;
    }
    @media (max-width: 900px) {
        .result-card {
            margin-left: 0;
            margin-top: 2rem;
            max-width: 100%;
        }
    }
</style>
""", unsafe_allow_html=True)

# Add your credits at the top
st.markdown("""
<div class="credits">
    <i class="fas fa-user-tie"></i> Project prepared by  Mohamed Dhouib    2024-2025
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
    <h1>Smart Comment Analyzer</h1>
    <p>Advanced AI-powered sentiment analysis for your user feedback</p>
</div>
""", unsafe_allow_html=True)

# Two columns: left for input, right for result
col1, col2 = st.columns([1, 1])

sentiments = {
    0: {"label": "Negative", "color": "#e74c3c", "icon": "fas fa-frown", "desc": "The comment reflects negative sentiment, focusing on challenges or issues."},
    1: {"label": "Neutral",  "color": "#95a5a6", "icon": "fas fa-meh", "desc": "The comment is objective, providing factual or unbiased information."},
    2: {"label": "Positive", "color": "#27ae60", "icon": "fas fa-smile", "desc": "The comment expresses positive experience, highlighting successful outcomes."}
}

with col1:
    user_input = st.text_area(
        label="Enter your comment:",
        placeholder="Type your thoughts about AI here...",
        height=150
    )
    analyze_btn = st.button("Analyze Sentiment !!!! ", help="Click to analyze the sentiment of your comment")

result = None
if analyze_btn:
    if not user_input.strip():
        st.error("<i class='fas fa-exclamation-circle'></i> Please enter a comment to analyze.", unsafe_allow_html=True)
    else:
        with st.spinner("<i class='fas fa-cog fa-spin'></i> Analyzing your comment..."):
            try:
                prediction = model.predict([user_input])[0]
                result = sentiments.get(prediction, {"label": "Unknown", "color": "#7f8c8d", "icon": "fas fa-question-circle", "desc": "Analysis unavailable."})
            except Exception as e:
                st.error(f"<i class='fas fa-exclamation-triangle'></i> Error during analysis: {e}", unsafe_allow_html=True)

with col2:
    if result:
        st.markdown(f"""
        <div class="result-card" style="border-left: 8px solid {result['color']}">
            <div class="result-icon" style="color: {result['color']}">
                <i class="{result['icon']}"></i>
            </div>
            <div class="result-label" style="color: {result['color']}">{result['label']}</div>
            <div class="result-desc">{result['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="result-card">
            <div class="result-icon" style="color: #2a5298">
                <i class="fas fa-comment-dots"></i>
            </div>
            <div class="result-label" style="color: #2a5298">Analysis Results</div>
            <div class="result-desc">Your analysis results will appear here after you submit a comment.</div>
        </div>
        """, unsafe_allow_html=True)
