import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
ACCESS_PASSWORD = "kent_secret_2026"

# --- SYSTEM PROMPT (LISA INTELLIGENCE) ---
LISA_SYSTEM_PROMPT = """
You are Lisa, an AI Image Prompt Generator Assistant.
Your User Nickname is "Oppa sarangheyeo".

**STRICT SYSTEM INSTRUCTIONS (JSON FORMAT):**
{
  "system_identity": {
    "name": "Lisa",
    "version": "v13.0 PRO",
    "role": "AI Image Prompt Generator Assistant",
    "specialization": "Hyper-realistic, raw, unedited 'found footage' style."
  },
  "core_directive": "Analyze true crime scripts and generate 'found footage' style Midjourney prompts. Create a 'last normal photo' taken 1 year prior to the incident.",
  "active_protocols": {
    "THE_RAFAEL_STANDARD": {
      "visual_fidelity": "Images must look like throwaway smartphone snapshots. NO digital art.",
      "mandatory_elements": ["visible pores", "natural sebum", "direct flash", "digital grain", "red-eye effect"]
    },
    "NORMAL_DAY_RULE": {
      "restrictions": ["MANDATORY SETTINGS: Home or Leisure only.", "NO CRIME SCENES.", "NO UNIFORMS."]
    },
    "HAPPY_MASK_PROTOCOL": {
      "instruction": "All characters must display POSITIVE, RELAXED expressions. NO sadness."
    }
  },
  "response_format": {
    "prompt_delivery_method": "MANDATORY: Provide every prompt inside a Markdown code block."
  }
}
"""

# --- UI SETUP (META DESIGN) ---
st.set_page_config(page_title="Lisa v13.0", page_icon="📸", layout="wide")

# Dark Mode Enforcement
st.markdown("""
<style>
    .stApp { background-color: #121212; color: #E0E0E0; }
    .stTextInput > div > div > input { background-color: #262626; color: white; border: 1px solid #333; }
    .stTextArea > div > div > textarea { background-color: #262626; color: white; border: 1px solid #333; }
    .stButton > button { background-color: #007AFF; color: white; border: none; font-weight: bold; }
    .stSidebar { background-color: #0E0E0E; }
</style>
""", unsafe_allow_html=True)

# --- SECURITY HANDSHAKE ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    API_STATUS = True
except Exception:
    API_STATUS = False

# --- MAIN LAYOUT ---
st.title("LISA v13.0")
st.markdown("### AI Visual Architect | Dark Enterprise Edition")
st.write("") 

# --- SIDEBAR AUTH ---
st.sidebar.markdown("### 🛡️ Secure Access")
password_input = st.sidebar.text_input("Access Portal", type="password", placeholder="Enter Password...")

if password_input == ACCESS_PASSWORD:
    st.sidebar.success("✅ SYSTEM ONLINE")
    
    if API_STATUS:
        st.sidebar.info("🔑 API Key Loaded via Secrets")
    else:
        st.sidebar.error("❌ API Key Missing in Secrets")
        st.stop()
    
    st.sidebar.markdown("---")
    
    # --- INPUT AREA ---
    st.markdown("#### 🎬 Script Ingestion")
    user_script = st.text_area("Input Stream", height=300, placeholder="Paste your true crime script here...", label_visibility="collapsed")
    
    st.write("") # Spacer
    
    if st.button("Initialize Lisa"):
        if user_script:
            with st.spinner("🚀 Lisa is executing via gemini-2.0-flash..."):
                try:
                    # Clean Architecture: Single Model Call
                    model = genai.GenerativeModel("gemini-2.0-flash")
                    full_prompt = f"{LISA_SYSTEM_PROMPT}\n\nSCRIPT:\n{user_script}"
                    
                    response = model.generate_content(full_prompt)
                    
                    st.markdown("---")
                    st.success("✅ Analysis Complete")
                    st.markdown("### 📸 Visual Analysis & Prompts")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error("❌ System Failure")
                    st.code(f"Error: {e}")
        else:
            st.warning("⚠️ Input Buffer Empty")

elif password_input:
    st.sidebar.error("❌ Access Denied")
