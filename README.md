# ⚡ ViralGen 4.0

**ViralGen 4.0** is a powerful, mobile-optimized web application designed to automate the metadata generation process for content creators. Built with **Python** and **Streamlit**, it leverages Google's **Gemini 2.5 Flash** AI model to instantly generate viral-ready captions, titles, descriptions, and hashtags for Instagram Reels, YouTube Shorts, and X (Twitter).

![Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-ff4b4b)
![AI](https://img.shields.io/badge/Powered%20by-Gemini%20Flash-orange)

## 🚀 Features

* **Multi-Platform Support:** Generates tailored metadata for Instagram, YouTube Shorts, and Twitter simultaneously.
* **Direct API Integration:** Bypasses library dependencies by using direct HTTP requests to Google's API, ensuring stability and compatibility with the latest models (like `gemini-2.5-flash`).
* **Upload-Ready Output:** Strips away generic advice and focuses purely on copy-pasteable metadata (Captions, Tags, Titles).
* **Mobile-First Design:** Features a responsive "Dark Mode" Glassmorphism UI with touch-friendly buttons and tabs.
* **Smart Parsing:** Automatically separates Titles, Descriptions, and Hashtags into individual code blocks for one-click copying.

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (Python web framework)
* **Backend Logic:** Python (Requests library)
* **AI Engine:** Google Gemini API (Model: `gemini-2.5-flash` / `gemini-1.5-flash`)

## 📦 Installation & Local Run

To run this app on your local machine:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/viralgen-4.0.git](https://github.com/yourusername/viralgen-4.0.git)
    cd viralgen-4.0
    ```

2.  **Install dependencies:**
    ```bash
    pip install streamlit requests
    ```

3.  **Run the app:**
    ```bash
    streamlit run app.py
    ```

4.  The app will open in your browser at `http://localhost:8501`.

## ☁️ Deployment (Streamlit Cloud)

This app is optimized for free deployment on Streamlit Community Cloud.

1.  Push your code to GitHub.
2.  Go to [share.streamlit.io](https://share.streamlit.io/).
3.  Select your repository and click **Deploy**.
4.  **Crucial Step:** Go to the App Settings -> **Secrets** and add your API key:
    ```toml
    GEMINI_API_KEY = "your_google_api_key_here"
    ```

## 🔑 Configuration

The app requires a Google Gemini API Key. You can obtain one for free at [Google AI Studio](https://aistudio.google.com/).

* **Local Use:** Enter the key in the sidebar when the app runs.
* **Deployed Use:** Store the key in Streamlit Secrets (recommended) or enter it manually in the sidebar.

## 📝 Usage

1.  **Enter Topic:** Type your video idea (e.g., "5 Money Habits").
2.  **Select Category:** Choose your niche (e.g., "Money / Wealth").
3.  **Select Vibe:** Choose the tone (e.g., "High Energy").
4.  **Set Model (Optional):** Default is set to `gemini-2.5-flash`, but you can change it in the sidebar if needed.
5.  **Generate:** Click the button and use the "Copy" icons to grab your metadata.

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
