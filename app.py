import streamlit as st
import google.generativeai as genai
import time

# --- 1. APP CONFIGURATION ---
st.set_page_config(
    page_title="ViralGen 3.0",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS FOR MOBILE & UI ---
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
    .stSelectbox>div>div>div { border-radius: 10px; }
    /* Tabs Design */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 8px 8px 0px 0px;
        padding: 10px;
        font-size: 14px;
    }
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
    
    st.info("ℹ️ If you get a 404 error, try running: `pip install -U google-generativeai`")

# --- 4. MAIN INTERFACE ---
st.title("🚀 ViralGen 3.0")
st.caption("Motivational & Viral Content Engine")

# Inputs
topic = st.text_input("💡 Content Idea / Topic", placeholder="e.g. Stop being lazy")

col1, col2 = st.columns(2)
with col1:
    # UPDATED CATEGORIES
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
    # AUTO-SUGGEST VIBE BASED ON CATEGORY
    default_vibe = 0
    if "AI Edits" in category: default_vibe = 0 # High Energy
    elif "Speaker" in category: default_vibe = 1 # Cinematic
    elif "Space" in category: default_vibe = 5 # Mysterious
    elif "Funny" in category: default_vibe = 3 # Meme
    
    vibe = st.selectbox("Vibe", 
        ["High Energy (Phonk/Fast)", "Cinematic (Epic/Slow)", "Dark/Gritty", "Funny/Meme", "Educational/Clean", "Mysterious/Cosmic"],
        index=default_vibe
    )

generate_btn = st.button("⚡ GENERATE STRATEGY")

# --- 5. AI LOGIC (WITH FALLBACK) ---
def get_model(key):
    genai.configure(api_key=key)
    # Try the latest flash model first, fallback to pro if it fails
    return genai.GenerativeModel('gemini-1.5-flash')

def get_viral_plan(topic, category, vibe, key):
    model = get_model(key)
    
    prompt = f"""
    Act as a Viral Content Expert for Reels and Shorts.
    
    Topic: {topic}
    Category: {category}
    Vibe: {vibe}

    STRICT INSTRUCTION:
    If Category is "Motivational (AI Edits)", suggest dark aesthetics, neon subtitles, and phonk/sigma music.
    If Category is "Motivational (Speaker)", suggest emotive background music, slow zooms, and bold white/yellow captions.
    If Category is "Space", suggest deep synth audio and 4k cosmos visuals.

    Generate 3 sections separated by "|||".
    
    SECTION 1: INSTAGRAM REELS
    - Trending Audio Name (Real existing audio/song trend).
    - Visual Hook: (Specific camera angle or clip style).
    - Caption: (SEO optimized with hook in first line).
    - 30 Hashtags: (Mix of #fyp #viral and niche tags).
    
    SECTION 2: YOUTUBE SHORTS
    - 3 Viral Title Options (High CTR, CAPS LOCK for emphasis).
    - Description Box (Keywords woven into sentences).
    - 15 Hidden Tags.
    - Loop Idea (Seamless transition).

    SECTION 3: X (TWITTER)
    - Hook Tweet (Punchy, under 280 chars).
    - Thread Outline (3 main points).
    - Engagement Question.
    
    Keep it concise. No fluff.
    """
    
    try:
        return model.generate_content(prompt).text
    except Exception as e:
        # If Flash fails, try Pro (older but stable)
        try:
            fallback_model = genai.GenerativeModel('gemini-pro')
            return fallback_model.generate_content(prompt).text
        except:
            raise e

# --- 6. DISPLAY RESULTS ---
if generate_btn:
    if not api_key:
        st.error("⚠️ Please add your API Key in the sidebar.")
    elif not topic:
        st.warning("⚠️ Please enter a topic.")
    else:
        with st.spinner("🔄 Analyzing Trends & Algorithms..."):
            try:
                raw_text = get_viral_plan(topic, category, vibe, api_key)
                
                # Split Sections
                if "|||" in raw_text:
                    sections = raw_text.split("|||")
                    insta_content = sections[0].replace("SECTION 1: INSTAGRAM REELS", "").strip()
                    shorts_content = sections[1].replace("SECTION 2: YOUTUBE SHORTS", "").strip()
                    x_content = sections[2].replace("SECTION 3: X (TWITTER)", "").strip()
                else:
                    insta_content = raw_text
                    shorts_content = "See Main Tab"
                    x_content = "See Main Tab"

                # TABS
                tab1, tab2, tab3 = st.tabs(["📸 Insta/Reels", "▶️ YT Shorts", "🧵 Twitter/X"])

                # INSTAGRAM
                with tab1:
                    st.subheader("Instagram Strategy")
                    st.write(insta_content)
                    st.markdown("---")
                    st.caption("👇 **Quick Copy Caption:**")
                    # Try to extract just caption if possible, else empty code block
                    st.code(f"{topic} #Viral #{category.split()[0]}", language="text")

                # SHORTS
                with tab2:
                    st.subheader("Shorts Strategy")
                    st.write(shorts_content)
                    st.markdown("---")
                    st.caption("👇 **Quick Copy Description:**")
                    st.code(f"{topic} - Watch till the end! #Shorts", language="text")

                # TWITTER
                with tab3:
                    st.subheader("X Strategy")
                    st.write(x_content)
                    st.caption("👇 **Quick Copy Tweet:**")
                    st.code(f"Here is why {topic} matters... 🧵", language="text")

            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Tip: Check if your API key is valid or try updating the library.")
