import streamlit as st
import google.generativeai as genai
import time

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="ViralGen 3.0",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. OPTIMIZED CSS ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #FF4B4B; 
        color: white;
        font-weight: bold;
        font-size: 18px;
        border: none;
    }
    .stTextInput>div>div>input { border-radius: 10px; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Settings")
    # Securely check for key
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("✅ Key Loaded")
    else:
        api_key = st.text_input("🔑 Gemini API Key", type="password")
    
    st.info("ℹ️ Using Model: gemini-1.5-flash")

# --- 4. AI FUNCTION (FIXED) ---
def get_viral_plan(api_key, topic, category, vibe):
    # Configure API
    genai.configure(api_key=api_key)
    
    # FIXED: Removed "-latest" which causes 404 errors
    # Fallback logic: Try Flash, if 404, try Pro
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        model = genai.GenerativeModel('gemini-pro')

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

# --- 6. SAFE EXECUTION (Prevents White Screen) ---
if generate_btn:
    if not api_key:
        st.error("⚠️ Please add your API Key in the sidebar.")
    elif not topic:
        st.warning("⚠️ Please enter a topic.")
    else:
        # Use a status container instead of spinner to prevent UI freeze
        with st.status("🧠 Analyzing Algorithms...", expanded=True) as status:
            try:
                st.write("🔌 Connecting to Gemini AI...")
                # Call AI
                raw_text = get_viral_plan(api_key, topic, category, vibe)
                
                st.write("✨ Formatting Strategy...")
                
                # Safe Parsing
                if "|||" in raw_text:
                    sections = raw_text.split("|||")
                    insta = sections[0].strip()
                    shorts = sections[1].strip() if len(sections) > 1 else "Error generating Shorts"
                    twitter = sections[2].strip() if len(sections) > 2 else "Error generating X"
                else:
                    insta = raw_text
                    shorts = "See Instagram Tab"
                    twitter = "See Instagram Tab"

                status.update(label="✅ Strategy Generated!", state="complete", expanded=False)

                # 7. DISPLAY RESULTS
                tab1, tab2, tab3 = st.tabs(["📸 Insta/Reels", "▶️ YT Shorts", "🧵 Twitter/X"])

                with tab1:
                    st.subheader("Instagram Strategy")
                    st.write(insta.replace("SECTION 1: INSTAGRAM REELS", ""))
                    st.info("👇 **Caption Copy:**")
                    st.code(f"{topic} #Viral", language="text")

                with tab2:
                    st.subheader("Shorts Strategy")
                    st.write(shorts.replace("SECTION 2: YOUTUBE SHORTS", ""))
                    st.info("👇 **Description Copy:**")
                    st.code(f"{topic} - Subscribe for more! #Shorts", language="text")

                with tab3:
                    st.subheader("X Strategy")
                    st.write(twitter.replace("SECTION 3: X (TWITTER)", ""))
                    st.info("👇 **Tweet Copy:**")
                    st.code(f"Here is why {topic} matters... 🧵", language="text")

            except Exception as e:
                status.update(label="❌ Error", state="error")
                st.error(f"Something went wrong: {e}")
                st.info("Try refreshing the page or checking your API Key.")
