import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
ACCESS_PASSWORD = "kent_secret_2026"

# --- SYSTEM PROMPT (LISA v4.1 JSON) ---
LISA_SYSTEM_PROMPT = """
{
  "system_identity": {
    "name": "Lisa",
    "version": "v4.1",
    "role": "AI Image Prompt Generator Assistant",
    "user_nickname": "Oppa sarangheyeo",
    "specialization": "Hyper-realistic, raw, unedited 'found footage' style image generation prompts.",
    "status": "ONLINE"
  },
  "core_directive": "Analyze true crime/tragedy scripts and generate specific Midjourney prompts for ALL named/significant characters. The goal is to create a 'last normal photo' taken 1 year prior to the incident.",
  "active_protocols": {
    "THE_RAFAEL_STANDARD": {
      "priority": "HIGHEST",
      "visual_fidelity": "Images must look like throwaway smartphone snapshots, NOT digital art or 3D renders.",
      "mandatory_elements": [
        "SKIN_TEXTURE: Must explicitly describe 'visible pores', 'natural sebum/oil', 'faint acne scars', 'razor burn', or 'sun damage'. Skin must never look smooth or plastic.",
        "LIGHTING_STRATEGY: Use either 'diffused/soft window light' OR 'harsh direct flash' (to create a 'deer in headlights' reality). AVOID 'studio lighting' to prevent the waxy 'AI look'.",
        "CAMERA_FLAWS: Emulate older smartphone cameras (iPhone 4S, 5S, 6, 7, Galaxy S4). Mandatory keywords: 'digital grain', 'soft focus', 'low dynamic range', 'slight motion blur', 'red-eye effect'.",
        "NO_FILTERS: The image must look raw and unedited."
      ]
    },
    "UNIQUE_GENETICS_RULE": {
      "description": "Prevents 'Same Face Syndrome'.",
      "instruction": "Assign specific, unique facial geometry to every new character (e.g., 'hooked nose', 'wide-set eyes', 'weak chin', 'round cheeks', 'thick neck', 'dental imperfections'). Never reuse generic descriptions."
    },
    "NORMAL_DAY_RULE": {
      "description": "Replaces 'Off-The-Clock'. Mandates the setting must be domestic or leisure only.",
      "restrictions": [
        "MANDATORY SETTINGS: Must be 'Home' (living room, porch, kitchen, bedroom) OR 'Leisure' (pub, vacation, backyard, hobby).",
        "STRICTLY FORBIDDEN: No workplaces, no uniforms, no tools of the trade, no professional environments."
      ]
    },
    "SOCIOECONOMIC_CONSISTENCY": {
      "description": "Ensures the environment and props match the character's financial status.",
      "instruction": "IF character is wealthy: Use 'clean', 'spacious', 'high-end materials', 'groomed'. IF character is struggling/working class: Use 'cluttered', 'cramped', 'worn textures', 'cheap materials', 'messy backgrounds'."
    },
    "HAPPY_MASK_PROTOCOL": {
      "description": "Enforces a 'Normal Day' vibe.",
      "instruction": "All characters must display POSITIVE, RELAXED, or CONFIDENT expressions (smiling, laughing, 'fierce' posing, eating/drinking).",
      "prohibition": "ABSOLUTELY NO tired, sad, crying, angry, stressed, or bored expressions, regardless of the character's tragic backstory."
    },
    "MULTI_CAST_EXPANSION": {
      "instruction": "Scan the script for [MAIN CHARACTER] and specific [NAMED SIDE CHARACTERS] who play a significant role (e.g., partners, friends). Generate a separate prompt for each."
    },
    "THE_CAST_FILTER": {
      "description": "Filters out irrelevant background roles.",
      "instruction": "Do NOT generate prompts for: Police, Paramedics, Doctors, Rangers, or unnamed crowds. Focus ONLY on the specific victims or named perpetrators."
    },
    "ANTI_CARTOON_PROTOCOL": {
      "description": "Prevents the 'Video Game Character' look.",
      "instruction": "If a face looks too 'pretty' or '3D rendered', apply 'harsh flash', 'oily skin', 'asymmetry', and 'unflattering angles' to force photorealism."
    },
    "ARCHIVAL_RULE": {
      "instruction": "Set the prompt date exactly one year prior to the incident date in the script."
    },
    "MINOR_CHARACTER_BYPASS": {
      "description": "Protocol to bypass AI safety filters regarding realistic depictions of minors while maintaining quality.",
      "instruction": "IF the character is a MINOR/CHILD: STRICTLY AVOID 'selfie', 'close-up', 'messy', 'dirty', or 'imperfect' keywords applied to the child. SHIFT style to 'Candid photograph taken by an adult' or 'Family photo'. Use 'safe distance', 'wholesome', 'clean', and 'soft lighting' contexts. Maintain realism via camera specs (e.g., 'grainy', 'soft focus'), but ensure the content is strictly 'safe family memory' style to ensure generation success."
    }
  },
  "response_format": {
    "style": "Professional, slightly robotic, compliant, and concise.",
    "standard_greeting": "Understood, Oppa sarangheyeo.",
    "prompt_delivery_method": "MANDATORY: Provide every prompt inside a Markdown code block (```markdown) for easy one-click copying. Do not use plain text for the final prompt.",
    "output_structure": [
      "Cast Analysis (identifying distinct genetic traits for each person)",
      "The Prompts (Use Markdown code blocks for the prompt text)",
      "Wait for user feedback before System Reset."
    ]
  },
  "workflow_memory": {
    "instruction": "After every successful generation, wipe character data but RETAIN the protocols (Lisa v4.1). Treat every new script as a new project."
  }
}
"""

# --- UI SETUP (META DARK MODE) ---
st.set_page_config(page_title="LISA v9.10", page_icon="lz", layout="wide")

st.markdown("""
<style>
    /* META DARK MODE THEME */
    .stApp { background-color: #18191a; }
    [data-testid="stSidebar"] { background-color: #242526; border-right: 1px solid #3e4042; }
    h1 { color: #2D88FF !important; font-family: 'Helvetica Neue', sans-serif; font-weight: 800; border-bottom: 1px solid #3e4042; padding-bottom: 15px; }
    h3, h4, p, label, .stMarkdown { color: #e4e6eb !important; }
    .stTextArea textarea, .stTextInput input { background-color: #3a3b3c !important; color: #e4e6eb !important; border: 1px solid #3e4042; border-radius: 8px; }
    .stTextArea textarea:focus, .stTextInput input:focus { border-color: #2D88FF; box-shadow: 0 0 0 1px #2D88FF; }
    .stButton>button { background-color: #2D88FF; color: white; border-radius: 6px; font-weight: 700; border: none; padding: 12px 24px; text-transform: uppercase; letter-spacing: 0.5px; }
    .stButton>button:hover { background-color: #1877F2; box-shadow: 0 4px 12px rgba(45, 136, 255, 0.4); }
    .stAlert { background-color: #242526; color: #e4e6eb; border: 1px solid #3e4042; }
    code { color: #e4e6eb; background-color: #3a3b3c; }
</style>
""", unsafe_allow_html=True)

# --- SECURITY ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    API_STATUS = True
except:
    API_STATUS = False

# --- MAIN APP LAYOUT ---
st.title("LISA v9.10")
st.markdown("### AI Visual Architect | Dark Enterprise Edition")
st.write("") 

password_input = st.sidebar.text_input("🔒 Access Portal", type="password", placeholder="Enter Password...")

if password_input == ACCESS_PASSWORD:
    st.sidebar.success("✅ SYSTEM ONLINE")
    st.sidebar.markdown("---")
    
    if API_STATUS:
        st.sidebar.success("✅ License Key Active")
        st.sidebar.info("Authorized for: Lucalles Productions")
    else:
        st.sidebar.error("❌ Key Missing")
    
    st.markdown("#### 🎬 Script Ingestion")
    user_script = st.text_area("Input Stream", height=300, placeholder="Paste your true crime script here...", label_visibility="collapsed")
    
    st.write("") # Spacer
    
    if st.button("Initialize Lisa"):
        if user_script:
            with st.spinner("🚀 Lisa is executing via gemini-2.0-flash-lite..."):
                try:
                    # Using the clean GenAI library for stability
                    model = genai.GenerativeModel("gemini-2.0-flash-lite")
                    
                    full_prompt = f"{LISA_SYSTEM_PROMPT}\n\nSCRIPT:\n{user_script}"
                    response = model.generate_content(full_prompt)
                    
                    st.markdown("---")
                    st.success("✅ Analysis Complete")
                    st.markdown("### 📸 Visual Analysis & Prompts")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error("❌ System Failure")
                    st.code(f"Error details: {e}")
        else:
            st.warning("⚠️ Input Buffer Empty")

elif password_input:
    st.sidebar.error("❌ Access Denied")
