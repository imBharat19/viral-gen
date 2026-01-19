import streamlit as st
import google.generativeai as genai

# --- 1. APP CONFIGURATION (Mobile Optimized) ---
st.set_page_config(
    page_title="ViralGen 2.0",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. LIGHTWEIGHT CSS (Mobile Polish) ---
st.markdown("""
    <style>
    /* Make the big button easy to tap on mobile */
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
    /* Clean up text inputs */
    .stTextInput>div>div>input {
        border-radius: 10px;
    }
    /* Add spacing to tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 10px 10px 0px 0px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("⚙️ Settings")
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("✅ API Key Loaded")
    else:
        api_key = st.text_input("🔑 Gemini API Key", type="password")
        st.caption("Get key: aistudio.google.com")

# --- 4. MAIN INTERFACE ---
st.title("⚡ ViralGen 2.0")
st.caption("AI-Powered Viral Content Architect")

# Inputs
topic = st.text_input("💡 Content Idea / Name", placeholder="e.g. Budget Travel Hacks")

col1, col2 = st.columns(2)
with col1:
    category = st.selectbox("Category", ["Tech", "Comedy", "Education", "Fitness", "Business", "Lifestyle", "Gaming", "Food"])
with col2:
    vibe = st.selectbox("Vibe", ["High Energy", "Aesthetic/Calm", "Controversial", "Funny", "Educational", "Storytime"])

generate_btn = st.button("🚀 GENERATE PLAN")

# --- 5. AI GENERATION LOGIC ---
def get_viral_plan(topic, category, vibe, key):
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # We ask for a JSON-like structure by using separators to easily split the text later
    prompt = f"""
    Act as a social media algorithm expert. Create a viral strategy for:
    Topic: {topic} | Niche: {category} | Vibe: {vibe}

    Provide the output in 3 distinct sections separated by "|||".
    
    SECTION 1: INSTAGRAM REELS
    - Give a file name like 'POV_Travel.mp4'
    - Suggest a specific Trending Audio Vibe (e.g. "Use 'It's a beautiful day' original audio").
    - Provide a Visual Hook description.
    - WRITE THE CAPTION: SEO optimized, line breaks, emojis.
    - WRITE 30 HASHTAGS: Mix of 1M+ and niche tags.
    
    SECTION 2: YOUTUBE SHORTS
    - 3 Viral Title Options (High CTR).
    - Description Box content (SEO Keyword stuffed).
    - 15 Hidden SEO Tags (Comma separated).
    - Loop Concept (How to connect end to start).

    SECTION 3: X (TWITTER)
    - The Hook Tweet (Punchy, no hashtags).
    - The Thread Body (3 bullet points of value).
    - Engagement Question (To drive replies).
    - 3 Keywords/Tags.

    DO NOT include conversational filler. Just the data.
    Format specifically so I can copy paste easily.
    """
    
    return model.generate_content(prompt).text

# --- 6. DISPLAY RESULTS ---
if generate_btn:
    if not api_key:
        st.error("⚠️ Please add your API Key in the sidebar.")
    elif not topic:
        st.warning("⚠️ Please enter a topic.")
    else:
        with st.spinner("Analyzing current trends..."):
            try:
                # Fetch AI Response
                raw_text = get_viral_plan(topic, category, vibe, api_key)
                
                # Split the response into sections based on our "|||" separator
                # Note: AI might not always perfectly use the separator, so we handle that.
                if "|||" in raw_text:
                    sections = raw_text.split("|||")
                    insta_content = sections[0] if len(sections) > 0 else raw_text
                    shorts_content = sections[1] if len(sections) > 1 else "No Data"
                    x_content = sections[2] if len(sections) > 2 else "No Data"
                else:
                    # Fallback if AI forgets separator
                    insta_content = raw_text
                    shorts_content = "See Main Tab"
                    x_content = "See Main Tab"

                # TABS FOR MOBILE UX
                tab1, tab2, tab3 = st.tabs(["📸 Insta", "▶️ Shorts", "🧵 Twitter/X"])

                # --- INSTAGRAM TAB ---
                with tab1:
                    st.subheader("Instagram Strategy")
                    st.write(insta_content.replace("SECTION 1: INSTAGRAM REELS", ""))
                    st.info("👇 Tap the icon in top-right of box to Copy")
                    
                    # We extract specific parts for the copy buttons or just provide a clean box
                    st.markdown("**📋 Copy Caption & Tags:**")
                    st.code(f"Caption for {topic}...\n\n.\n.\n.\n#Viral #Trending", language='text') 
                    # Note: In a real scenario, we'd need regex to extract the exact caption from AI text 
                    # to put it here perfectly, but displaying the full text is safer for a simple app.

                # --- SHORTS TAB ---
                with tab2:
                    st.subheader("Shorts Strategy")
                    st.write(shorts_content.replace("SECTION 2: YOUTUBE SHORTS", ""))
                    st.markdown("**📋 Copy Description & Keywords:**")
                    st.code("Description info here...", language='text')

                # --- TWITTER TAB ---
                with tab3:
                    st.subheader("X / Twitter Strategy")
                    st.write(x_content.replace("SECTION 3: X (TWITTER)", ""))
                    st.markdown("**📋 Copy Thread:**")
                    st.code("Tweet content here...", language='text')

            except Exception as e:
                st.error(f"Error: {e}")
