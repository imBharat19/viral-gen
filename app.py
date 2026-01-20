import streamlit as st
import requests

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="ViralGen 5.0",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. ULTRA-MODERN CSS (Mobile Optimized) ---
st.markdown("""
    <style>
    /* Global Background */
    .stApp {
        background-color: #050505;
        background-image: linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 30px 30px;
    }
    
    /* Inputs */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #1a1a1a;
        color: #e0e0e0;
        border-radius: 12px;
        border: 1px solid #333;
    }
    
    /* Generate Button - Gradient Pulse */
    .stButton>button {
        background: linear-gradient(45deg, #FF3131, #FF914D);
        color: white;
        border: none;
        border-radius: 12px;
        height: 3.8em;
        width: 100%;
        font-weight: 800;
        font-size: 18px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        box-shadow: 0 0 20px rgba(255, 49, 49, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 30px rgba(255, 49, 49, 0.6);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1a1a;
        border-radius: 10px;
        color: #888;
        border: 1px solid #333;
        padding: 10px 20px;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #FF3131; color: white; border-color: #FF3131;
    }

    /* --- MOBILE COPY FIX --- */
    [data-testid="stCode"] pre {
        white-space: pre-wrap !important;
        word-break: break-word !important;
        padding-right: 50px !important;
        background-color: #111 !important;
        border: 1px solid #333;
    }
    
    /* Typography */
    h1 { 
        text-align: center; 
        background: -webkit-linear-gradient(0deg, #FF3131, #FF914D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5em;
        font-weight: 900;
        margin-bottom: -10px;
    }
    p { color: #888; text-align: center; }
    h3, caption { color: #ccc !important; font-family: sans-serif; }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Engine Settings")
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("✅ Neural Engine Active")
    else:
        api_key = st.text_input("🔑 Enter Gemini API Key", type="password")
    
    st.markdown("---")
    model_name = st.text_input("🤖 Model", value="gemini-2.5-flash")

# --- 4. ALGORITHM-HACKING LOGIC ---
def generate_metadata(topic, category, vibe, api_key, model):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    
    # --- THE SEO & VIRAL PROMPT ---
    prompt = f"""
    Act as a Senior SEO Strategist & Viral Content Expert (Specializing in 2026 Algorithms).
    
    Target: {topic}
    Niche: {category}
    Vibe: {vibe}

    GOAL: Maximum Reach, High CTR, and Search Ranking.
    
    STRICT RULES:
    1. **NO AI WORDS:** Do not use 'AI', 'Phonk', 'ChatGPT', 'Robot', or 'Generated'. Keep it 100% Organic.
    2. **SEO OPTIMIZATION:** Place high-volume keywords at the START of titles and descriptions.
    3. **VIRAL PSYCHOLOGY:** Use curiosity gaps and strong hooks.
    4. **FORMAT:** Use specific separator "~SEPARATOR~".

    OUTPUT STRUCTURE:

    SECTION 1: INSTAGRAM
    [Write a Caption. First sentence must be a 'Stop-Scroll' hook. Use line breaks for readability.]
    ~SEPARATOR~
    [Write 30 Trending Hashtags. Mix of High-Volume (1M+) and Specific Niche tags. Space separated.]

    |||

    SECTION 2: YOUTUBE SHORTS
    [Write 1 VIRAL TITLE. ALL CAPS. Under 50 chars. Must trigger curiosity.]
    ~SEPARATOR~
    [Write Description. First 2 lines must contain main SEO keywords naturally. Add Call-to-Action.]
    ~SEPARATOR~
    [Write 15 High-Traffic Tags. Comma separated. Focus on search terms users actually type.]

    |||

    SECTION 3: X (TWITTER)
    [Write a Thread Starter. Short, Punchy, Controversial or High Value. No hashtags in the hook.]
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Connection Error: {e}"

# --- 5. UI LAYOUT ---
st.markdown("<h1>ViralGen 5.0</h1>", unsafe_allow_html=True)
st.markdown("<p>Algorithm-Optimized Metadata Engine</p><br>", unsafe_allow_html=True)

with st.container():
    topic = st.text_input("🔥 What topic is trending?", placeholder="e.g. Passive Income 2026")
    
    c1, c2 = st.columns(2)
    with c1:
        category = st.selectbox("Category", [
            "Motivational (Cinematic/Visual)", 
            "Motivational (Speaker)", 
            "Money / Wealth / Crypto", 
            "Gym / Aesthetics", 
            "Space / Mystery", 
            "Travel / Luxury", 
            "Tech / Future", 
            "Comedy / Relatable"
        ])
    with c2:
        vibe = st.selectbox("Vibe", [
            "High Intensity / Fast", 
            "Dark / Moody", 
            "Emotional / Deep", 
            "Controversial / Bold", 
            "Educational / Sharp"
        ])

    st.write("")
    generate = st.button("🚀 HACK THE ALGORITHM")

# --- 6. OUTPUT PROCESSING ---
if generate:
    if not api_key:
        st.error("⚠️ API Key missing")
    elif not topic:
        st.warning("⚠️ Enter a topic")
    else:
        with st.status("🧠 Analyzing Search Trends...", expanded=True) as status:
            raw_text = generate_metadata(topic, category, vibe, api_key, model_name)
            
            if "Error" in raw_text:
                status.update(label="❌ Failed", state="error")
                st.error(f"Error: {raw_text}")
            else:
                status.update(label="✅ Optimized Data Ready", state="complete", expanded=False)
                
                try:
                    # Initialize vars
                    insta_cap, insta_tags = "Error", "Error"
                    sh_title, sh_desc, sh_tags = "Error", "Error", "Error"
                    tweet = "Error"

                    if "|||" in raw_text:
                        parts = raw_text.split("|||")
                        
                        # INSTAGRAM
                        if len(parts) > 0:
                            p1 = parts[0].replace("SECTION 1: INSTAGRAM", "").strip()
                            if "~SEPARATOR~" in p1:
                                insta_cap, insta_tags = p1.split("~SEPARATOR~")
                            else: insta_cap = p1

                        # SHORTS
                        if len(parts) > 1:
                            p2 = parts[1].replace("SECTION 2: YOUTUBE SHORTS", "").strip()
                            if "~SEPARATOR~" in p2:
                                sh_parts = p2.split("~SEPARATOR~")
                                sh_title = sh_parts[0].strip() if len(sh_parts) > 0 else ""
                                sh_desc = sh_parts[1].strip() if len(sh_parts) > 1 else ""
                                sh_tags = sh_parts[2].strip() if len(sh_parts) > 2 else ""
                        
                        # TWITTER
                        if len(parts) > 2: tweet = parts[2].replace("SECTION 3: X (TWITTER)", "").strip()

                    # DISPLAY TABS
                    t1, t2, t3 = st.tabs(["📸 Insta", "▶️ Shorts SEO", "🐦 X Thread"])
                    
                    with t1:
                        st.caption("🔥 Viral Caption")
                        st.code(insta_cap.strip(), language="text")
                        st.caption("📈 Trending Tags")
                        st.code(insta_tags.strip(), language="text")
                    
                    with t2:
                        st.caption("🏆 High-CTR Title")
                        st.code(sh_title.strip(), language="text")
                        st.caption("🔍 SEO Description")
                        st.code(sh_desc.strip(), language="text")
                        st.caption("🏷️ Search Tags")
                        st.code(sh_tags.strip(), language="text")
                    
                    with t3:
                        st.caption("💬 Engagement Hook")
                        st.code(tweet.strip(), language="text")

                except Exception as e:
                    st.error(f"Parsing Error: {e}")
