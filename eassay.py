import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Eassay", page_icon="💜", layout="wide")

# Custom CSS for UI Enhancement
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Title Style */
    h1 {
        background: -webkit-linear-gradient(45deg, #C77DFF, #7B2CBF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    /* Button Style */
    .stButton > button {
        background: linear-gradient(90deg, #7B2CBF 0%, #9D4EDD 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(123, 44, 191, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(123, 44, 191, 0.5);
    }
    
    /* Card Container */
    .essay-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 40px;
        margin-top: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    .essay-card h3 {
        color: #E0AAFF;
        margin-bottom: 20px;
    }

    /* Hide Streamlit Anchor Links */
    a.anchor-link {
        display: none !important;
    }
    
    /* Target common Streamlit header anchors */
    [data-testid="stHeader"] a, 
    h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
        display: none !important;
        pointer-events: none;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1>Eassay 💜</h1>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Configuration")
    
    # Try to get API key from secrets, otherwise show input
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("API Key loaded from secrets! 🔒")
    else:
        api_key = st.text_input("Gemini API Key", type="password", help="Get your key from Google AI Studio")
    
    model_name = st.selectbox(
        "Select Model",
        [
            "gemini-2.0-flash",
            "gemini-2.0-flash-lite", 
            "gemini-flash-latest",
            "gemini-pro-latest"
        ],
        index=0,
        help="Try a different model if you hit rate limits."
    )
    
    st.divider()
    
    tone = st.selectbox(
        "Tone",
        ["Formal", "Informal", "Persuasive", "Descriptive", "Narrative"]
    )

    word_count = st.slider(
        "Word Count",
        min_value=100,
        max_value=1000,
        step=50,
        value=300
    )
    
    st.markdown("---")
    st.markdown("Made with 💜 by Sanika")

# Main Content Area
st.markdown('<h3 style="margin-bottom: 20px;">Create content that matters</h3>', unsafe_allow_html=True)

st.markdown('<p style="font-size: 24px; font-weight: 600; margin-bottom: 10px;">What would you like to write about?</p>', unsafe_allow_html=True)
topic = st.text_area(
    "What would you like to write about?",
    label_visibility="collapsed",
    placeholder="e.g. The impact of artificial intelligence on modern education systems...",
    height=150
)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    generate_btn = st.button("✨ Generate Essay", use_container_width=True)

if generate_btn:
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar to continue.")
    elif not topic:
        st.warning("Please enter a topic first.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name)
            
            with st.spinner('✨ Weaving your words...'):
                prompt = f"""
                Write a {tone} essay about '{topic}'.
                The essay should be approximately {word_count} words long.
                Structure the essay with clear headings for Introduction, Body, and Conclusion.
                Format the output in HTML. Use <h4> tags for section headings.
                Important: 
                - Do NOT include a main title (H1/H2) at the top.
                - Do NOT wrap the output in <html>, <body>, or <div> tags. 
                - Return ONLY the content (paragraphs and headings).
                - Do NOT use Markdown code fences (```html).
                """
                
                response = model.generate_content(prompt)
                
                # Clean up response (remove code fences and potential wrapper tags if AI ignores instructions)
                essay_content = response.text
                essay_content = essay_content.replace("```html", "").replace("```", "")
                essay_content = essay_content.replace("<html>", "").replace("</html>", "")
                essay_content = essay_content.replace("<body>", "").replace("</body>", "")
                
                # Custom Card Output
                st.markdown(f"""
                <div class="essay-card">
                    <h3>{topic}</h3>
                    <div style="margin-bottom: 20px; font-size: 0.9em; opacity: 0.8;">
                        <span>📝 {tone}</span> • <span>📏 ~{word_count} words</span>
                    </div>
                    <div>
                        {essay_content}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            if "429" in str(e):
                st.error("⏳ **Quota Exceeded**")
                st.warning(f"You've hit the usage limit. Try switching to `{model_name}` or wait a moment.")
            else:
                st.error(f"An error occurred: {str(e)}")
