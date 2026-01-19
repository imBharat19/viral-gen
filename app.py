import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="ViralGen 3.0",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. OPTIMIZED CSS (Safe for Mobile) ---
st.markdown("""
    <style>
    /* Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #FF4B4B; 
        color: white;
        font-weight: bold;
        font-size: 18px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #FF2B2B; 
    }
    /* Input Fields */
    .stTextInput>div>div>input { border-radius: 10px; }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 8px 8px 0px 0px;
        padding: 10px;
        font-size: 14px;
    }
    /* Hide Header/Footer for clean look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Settings")
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("✅ Key Loaded")
    else:
        api_key = st.text_input("🔑 Gemini API Key", type="password")
    
    st.info("ℹ️ Using Gemini 1.5 Flash (Fastest Model)")

# --- 4. CACHED AI FUNCTIONS (Prevents Lag) ---
@st.cache_resource
def configure_model(key):
    genai.configure(api_key=key)
    # Using 'latest' variant to avoid version errors
    return genai.GenerativeModel('gemini-1.5-flash-latest')

def get_viral_plan(model, topic, category, vibe):
    prompt = f"""
    Act as a Viral Content Strategist.
    Topic: {topic} | Category: {category} | Vibe: {vibe}

    STRICT OUTPUT FORMAT:
    Provide 3 sections separated strictly by the characters "|||".
    
    SECTION 1: INSTAGRAM REELS
    - Trending Audio Suggestion
    - Visual Hook (Camera angle/Action)
    - Caption (With hook & line breaks)
    - 30 Mixed Hashtags
    
    |||
    
    SECTION 2: YOUTUBE SHORTS
    - 3 Viral Title Options (CAPS for impact)
    - Description (SEO Keywords included)
    - 15 Hidden Tags
    - Loop Concept
    
    |||
    
    SECTION 3: X (TWITTER)
    - Hook Tweet
    - Thread Body (3 points)
    - Engagement Question
    
    Keep it concise. No conversational filler.
    """
    
    # Generate content
    response = model.generate_content(prompt)
    return response.text

# --- 5. MAIN UI ---
st.title("⚡ ViralGen 3.0")
st.caption("Motivational & Viral Content Engine")

# Inputs
topic = st.text_input("💡 Content Idea / Topic", placeholder="e.g. Stop being lazy")

col1, col2 = st.columns(2)
with col1:
    category = st.selectbox("Category", [
        "Motivational (AI Edits)",
        "Motivational (Speaker)",
        "Money / Wealth",
        "Space / Astronomy",
        "Gym / Fitness",
        "Funny / Comedy",
        "Travel",
        "Tech",
        "Business"
    ])
with col2:
    # Auto-select vibe logic
    default_vibe = 0
    if "AI Edits" in category: default_vibe = 0
    elif "Speaker" in category: default_vibe = 1
    elif "Space" in category: default_vibe = 5
    elif "Funny" in category: default_vibe = 3
    
    vibe = st.selectbox("Vibe", 
        ["High Energy (Phonk/Fast)", "Cinematic (Epic/Slow)", "Dark/Gritty", "Funny/Meme", "Educational/Clean", "Mysterious/Cosmic"],
        index=default_vibe
    )

generate_btn = st.button("🚀 GENERATE STRATEGY")

# --- 6. EXECUTION LOGIC ---
if generate_btn:
    if not api_key:
        st.error("⚠️ Please add your API Key in the sidebar.")
    elif not topic:
        st.warning("⚠️ Please enter a topic.")
    else:
        # Show a progress bar instead of just a spinner to keep UI alive
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("🔌 Connecting to AI...")
            progress_bar.progress(20)
            
            # 1. Configure Model (Cached)
            model = configure_model(api_key)
            
            status_text.text("🧠 Brainstorming Viral Hooks...")
            progress_bar.progress(50)
            
            # 2. Generate
            raw_text = get_viral_plan(model, topic, category, vibe)
            
            status_text.text("✨ Formatting Result...")
            progress_bar.progress(80)

            # 3. Safe Parsing (Prevents White Screen Crash)
            if "|||" in raw_text:
                sections = raw_text.split("|||")
                insta = sections[0].strip()
                shorts = sections[1].strip() if len(sections) > 1 else "Error generating Shorts"
                twitter = sections[2].strip() if len(sections) > 2 else "Error generating X"
            else:
                # Fallback if AI forgets separator
                insta = raw_text
                shorts = "See Instagram Tab"
                twitter = "See Instagram Tab"

            progress_bar.progress(100)
            status_text.empty() # Clear status message
            progress_bar.empty() # Clear progress bar

            # 4. Display Tabs
            tab1, tab2, tab3 = st.tabs(["📸 Insta/Reels", "▶️ YT Shorts", "🧵 Twitter/X"])

            with tab1:
                st.subheader("Instagram Strategy")
                st.write(insta.replace("SECTION 1: INSTAGRAM REELS", ""))
                st.markdown("---")
                st.caption("👇 **Caption Copy:**")
                st.code(f"{topic} #Viral", language="text")

            with tab2:
                st.subheader("Shorts Strategy")
                st.write(shorts.replace("SECTION 2: YOUTUBE SHORTS", ""))
                st.markdown("---")
                st.caption("👇 **Description Copy:**")
                st.code(f"{topic} - Subscribe for more! #Shorts", language="text")

            with tab3:
                st.subheader("X Strategy")
                st.write(twitter.replace("SECTION 3: X (TWITTER)", ""))
                st.caption("👇 **Tweet Copy:**")
                st.code(f"Here is why {topic} matters... 🧵", language="text")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Tip: If the error persists, refresh the page.")
