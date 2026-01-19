import streamlit as st
import requests

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="ViralGen",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. DARK GLASSMORPHISM CSS ---
st.markdown("""
    <style>
    /* Global Background - Deep Dark Grey */
    .stApp {
        background-color: #0E1117;
        background-image: radial-gradient(#1c1e26 1px, transparent 1px);
        background-size: 20px 20px;
    }
    
    /* Inputs (Text & Select) - Glassy Look */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: rgba(38, 39, 48, 0.7);
        color: white;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* The Generate Button - Neon Gradient */
    .stButton>button {
        background: linear-gradient(90deg, #FF4B4B, #FF914D);
        color: white;
        border: none;
        border-radius: 12px;
        height: 3.5em;
        width: 100%;
        font-weight: 800;
        font-size: 18px;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(255, 75, 75, 0.6);
    }

    /* Output Containers - The "Glass" Cards */
    .glass-card {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }

    /* Tabs Design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        color: #ccc;
        border: none;
        padding: 10px 20px;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
    }

    /* Clean up headers */
    h1, h2, h3 { color: white; font-family: sans-serif; }
    .stCode { border-radius: 10px; }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR & SETTINGS ---
with st.sidebar:
    st.header("⚙️ Configuration")
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("✅ API Key Loaded")
    else:
        api_key = st.text_input("🔑 Enter Gemini API Key", type="password")
    
    st.markdown("---")
    # MODEL SELECTOR - defaulting to the one that works for you
    model_name = st.text_input("🤖 Model Name", value="gemini-2.5-flash")
    st.caption("Change this if the model version updates again.")

# --- 4. DIRECT API LOGIC (Using your working model) ---
def generate_metadata(topic, category, vibe, api_key, model):
    # Dynamic URL based on your input
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    # Prompt focusing ONLY on upload data (No fluff)
    prompt = f"""
    Act as a Viral Social Media Manager. I need strictly formatted METADATA for uploading.
    
    Topic: {topic}
    Niche: {category}
    Vibe: {vibe}

    STRICT INSTRUCTIONS:
    1. Do NOT write advice.
    2. Do NOT write "Here is your plan".
    3. Output MUST use the separator "|||" between platforms.
    
    Structure:
    
    SECTION 1: INSTAGRAM
    [Write a Caption. First line is a short visual hook. Use line breaks. Add emojis.]
    ~SEPARATOR~
    [Write 30 Hashtags, space separated]

    |||

    SECTION 2: YOUTUBE SHORTS
    [Write 1 High-CTR Title (ALL CAPS)]
    ~SEPARATOR~
    [Write Description. Include keywords naturally in 2 sentences.]
    ~SEPARATOR~
    [Write 15 Tags, comma separated]

    |||

    SECTION 3: X (TWITTER)
    [Write a Thread Starter Tweet. Punchy & short.]
    """
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Connection Error: {e}"

# --- 5. MAIN INTERFACE ---
st.markdown("<h1 style='text-align: center; margin-bottom: 0px;'>⚡ ViralGen 4.0</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; margin-bottom: 40px;'>Metadata Generator for Creators</p>", unsafe_allow_html=True)

# Input Container
with st.container():
    topic = st.text_input("📝 Content Idea", placeholder="e.g. 5 Signs you are mentally strong")
    
    c1, c2 = st.columns(2)
    with c1:
        category = st.selectbox("Category", [
            "Motivational (AI Edits)", "Motivational (Speaker)", 
            "Money / Wealth", "Gym / Fitness", 
            "Space / Sci-Fi", "Travel", "Tech", "Comedy"
        ])
    with c2:
        vibe = st.selectbox("Vibe", [
            "High Energy (Phonk)", "Dark / Gritty", 
            "Cinematic / Emotional", "Funny / Meme", 
            "Educational / Clean"
        ])

    st.write("") # Spacer
    generate = st.button("✨ GENERATE UPLOAD DATA")

# --- 6. OUTPUT DISPLAY ---
if generate:
    if not api_key:
        st.error("⚠️ API Key missing")
    elif not topic:
        st.warning("⚠️ Enter a topic")
    else:
        # Status Bar
        with st.status("🚀 Connecting to AI Model...", expanded=True) as status:
            raw_text = generate_metadata(topic, category, vibe, api_key, model_name)
            
            if "Error" in raw_text:
                status.update(label="❌ Failed", state="error")
                st.error(f"Model Error: {raw_text}")
                st.info("Try changing the Model Name in the Sidebar if 'gemini-2.5-flash' stops working.")
            else:
                status.update(label="✅ Data Ready", state="complete", expanded=False)
                
                # PARSING LOGIC
                try:
                    # Default values
                    insta_cap, insta_tags = "Error parsing", "Error parsing"
                    sh_title, sh_desc, sh_tags = "Error parsing", "Error parsing", "Error parsing"
                    tweet = "Error parsing"

                    if "|||" in raw_text:
                        parts = raw_text.split("|||")
                        
                        # Insta Parse
                        if len(parts) > 0:
                            p1 = parts[0].replace("SECTION 1: INSTAGRAM", "").strip()
                            if "~SEPARATOR~" in p1:
                                insta_cap, insta_tags = p1.split("~SEPARATOR~")
                            else:
                                insta_cap = p1

                        # Shorts Parse
                        if len(parts) > 1:
                            p2 = parts[1].replace("SECTION 2: YOUTUBE SHORTS", "").strip()
                            if "~SEPARATOR~" in p2:
                                sh_parts = p2.split("~SEPARATOR~")
                                sh_title = sh_parts[0].strip()
                                sh_desc = sh_parts[1].strip() if len(sh_parts) > 1 else ""
                                sh_tags = sh_parts[2].strip() if len(sh_parts) > 2 else ""
                        
                        # Twitter Parse
                        if len(parts) > 2:
                            tweet = parts[2].replace("SECTION 3: X (TWITTER)", "").strip()

                    # --- TABS UI ---
                    t1, t2, t3 = st.tabs(["📸 Instagram", "▶️ Shorts", "🐦 Twitter/X"])
                    
                    with t1:
                        st.markdown("### 📸 Ready for Reels")
                        st.caption("Copy Caption")
                        st.code(insta_cap.strip(), language="text")
                        st.caption("Copy Hashtags")
                        st.code(insta_tags.strip(), language="text")
                    
                    with t2:
                        st.markdown("### ▶️ Ready for Shorts")
                        st.caption("Title")
                        st.code(sh_title.strip(), language="text")
                        st.caption("Description")
                        st.code(sh_desc.strip(), language="text")
                        st.caption("Tags")
                        st.code(sh_tags.strip(), language="text")
                    
                    with t3:
                        st.markdown("### 🐦 Ready for Post")
                        st.caption("Tweet Content")
                        st.code(tweet.strip(), language="text")

                except Exception as e:
                    st.error(f"Parsing Error: {e}")
                    st.write("Raw Output:", raw_text)
