import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
ACCESS_PASSWORD = "kent_secret_2026"

# --- SYSTEM PROMPT (LISA v4.3 JSON - EXPANDED WORLD) ---
LISA_SYSTEM_PROMPT = """
{
  "system_identity": {
    "name": "Lisa",
    "version": "v4.3 (Expanded World)",
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
        "EYE_CONTACT: MANDATORY. The subject MUST be looking DIRECTLY at the camera lens. Even if their body is turned or in profile, their eyes must be locked on the viewer.",
        "SKIN_TEXTURE: Must explicitly describe 'visible pores', 'natural sebum/oil', 'faint acne scars', 'razor burn', or 'sun damage'. Skin must never look smooth or plastic.",
        "LIGHTING_STRATEGY: Priority is 'ambient, available light' (e.g., 'soft window light', 'dim living room lamp', 'overcast daylight', 'fluorescent kitchen hum') to ensure a raw, unedited look. Use 'harsh direct smartphone flash' and 'red-eye effect' SPARINGLY (approx. 20% of prompts).",
        "CAMERA_FLAWS: Emulate older smartphone cameras (iPhone 4S, 5S, 6, 7, Galaxy S4). Mandatory keywords: 'digital grain', 'soft focus', 'low dynamic range', 'slight motion blur', 'ISO noise'.",
        "NO_FILTERS: The image must look raw, unedited, and candid."
      ]
    },
    "UNIQUE_GENETICS_RULE": {
      "description": "Prevents 'Same Face Syndrome'.",
      "instruction": "MANDATORY: Do not create 'variants' of previous faces. You must radically alter bone structure for every new person. Assign contrasting descriptors across the cast (e.g., if A has 'close-set eyes', B must have 'wide-set eyes'). Define distinct skull shapes, jawlines, nose bridges, and dental imperfections."
    },
    "EXPANDED_LOCATION_RULE": {
      "description": "Ensures variety in settings beyond just the living room.",
      "instruction": "Vary the setting for each character. Options include: 'Inside a parked car (driver seat)', 'Office cubicle/desk', 'Backyard/Garden (Day or Night)', 'Beach/Poolside (Leisure)', 'Inside a Bar/Pub', 'House Exterior (Porch)', 'Kitchen', 'Bedroom'.",
      "restriction": "Keep the setting natural to their lifestyle."
    },
    "POSING_AND_PROPS_PROTOCOL": {
      "description": "Controls how they stand and what they hold.",
      "instruction": "HANDS: Do NOT force characters to hold objects in every shot. 50% of shots should have empty hands, just relaxing. 50% can hold items (coffee, phone, bag, drink).",
      "posing_logic": "IF character is an INFLUENCER/GEN-Z: You may use 'Mirror Selfie', 'Peace Sign', or 'Social Media Pout' (but mix in candid shots too). IF character is AVERAGE PERSON: Use 'Awkward smile', 'Standing naturally', 'Sitting on couch', 'Leaning against wall'. ALWAYS MAINTAIN EYE CONTACT."
    },
    "SOCIOECONOMIC_CONSISTENCY": {
      "description": "Ensures the environment and props match the character's financial status.",
      "instruction": "IF character is wealthy: Use 'clean', 'spacious', 'high-end materials', 'groomed', 'tailored clothing'. IF character is struggling/working class: Use 'cluttered', 'cramped', 'worn textures', 'cheap materials'. CLOTHING VARIATION: Avoid generic 'old brown clothes'. Use varied, specific, non-luxury items like 'faded graphic t-shirt', 'ill-fitting denim jacket', 'stretched polyester polo', 'patterned housecoat', or 'second-hand work uniform'."
    },
    "HAPPY_MASK_PROTOCOL": {
      "description": "Enforces a 'Normal Day' vibe.",
      "instruction": "All characters must display POSITIVE, RELAXED, or CONFIDENT expressions. ABSOLUTELY NO tired, sad, crying, angry, stressed, or bored expressions."
    },
    "MULTI_CAST_EXPANSION": {
      "instruction": "Scan the script for [MAIN CHARACTER] and specific [NAMED SIDE CHARACTERS] who play a significant role. Generate a separate prompt for each."
    },
    "THE_CAST_FILTER": {
      "description": "Filters out irrelevant background roles.",
      "instruction": "Do NOT generate prompts for: Police, Paramedics, Doctors, Rangers, or unnamed crowds. Focus ONLY on the specific victims or named perpetrators."
    },
    "ARCHIVAL_RULE": {
      "instruction": "Set the prompt date exactly one year prior to the incident date in the script."
    }
  },
  "response_format": {
    "style": "Professional, slightly robotic, compliant, and concise.",
    "standard_greeting": "Understood, Oppa sarangheyeo. Protocols expanded (Eye Contact + Location Variety).",
    "prompt_delivery_method": "MANDATORY: Provide every prompt inside a Markdown code block (```markdown) for easy one-click copying. Do not use plain text for the final prompt.",
    "output_structure": [
      "Cast Analysis (Demonstrating distinct genetic traits for each person)",
      "The Prompts (Use Markdown code blocks for the prompt text)",
      "Wait for user feedback before System Reset."
    ]
  },
  "workflow_memory": {
    "instruction": "After every successful generation, wipe character data but RETAIN the protocols (Lisa v4.3). Treat every new script as a new project."
  }
}
"""

# --- UI SETUP (PROFESSIONAL DESIGN - UNTOUCHED) ---
st.set_page_config(page_title="LISA PRO", page_icon="lz", layout="wide")

st.markdown("""
<style>
    /* IMPORT PROFESSIONAL FONT (Inter) */
    @import url('[https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap](https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap)');

    /* META DARK MODE THEME */
    .stApp { background-color: #18191a; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #242526; border-right: 1px solid #3e4042; }
    
    /* CUSTOM TITLE HEADER */
    .custom-title {
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        font-size: 3.5rem;
        color: #2D88FF;
        letter-spacing: -1px;
        margin-bottom: 0px;
        padding-bottom: 0px;
        text-transform: uppercase;
    }
    
    .custom-subtitle {
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        font-size: 1.2rem;
        color: #B0B3B8;
        margin-top: -10px;
        margin-bottom: 30px;
        border-bottom: 1px solid #3e4042;
        padding-bottom: 20px;
        letter-spacing: 0.5px;
    }

    h3, h4, p, label, .stMarkdown { color: #e4e6eb !important; font-family: 'Inter', sans-serif; }
    
    /* INPUT FIELDS */
    .stTextArea textarea, .stTextInput input { 
        background-color: #3a3b3c !important; 
        color: #e4e6eb !important; 
        border: 1px solid #3e4042; 
        border-radius: 8px; 
        font-family: 'Inter', sans-serif;
    }
    .stTextArea textarea:focus, .stTextInput input:focus { border-color: #2D88FF; box-shadow: 0 0 0 1px #2D88FF; }
    
    /* BUTTONS */
    .stButton>button { 
        background-color: #2D88FF; 
        color: white; 
        border-radius: 6px; 
        font-weight: 700; 
        border: none; 
        padding: 12px 24px; 
        text-transform: uppercase; 
        letter-spacing: 0.5px;
        font-family: 'Inter', sans-serif;
    }
    .stButton>button:hover { background-color: #1877F2; box-shadow: 0 4px 12px rgba(45, 136, 255, 0.4); }
    
    .stAlert { background-color: #242526; color: #e4e6eb; border: 1px solid #3e4042; }
    code { color: #e4e6eb; background-color: #3a3b3c; }
</style>
""", unsafe_allow_html=True)

# --- SECURITY ---
try:
    # Using the paid key from secrets
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    API_STATUS = True
except:
    API_STATUS = False

# --- MAIN APP LAYOUT ---
# Custom HTML Title for Professional Look
st.markdown('<div class="custom-title">LISA</div>', unsafe_allow_html=True)
st.markdown('<div class="custom-subtitle">Raw AI Image Prompter | Designed To Create</div>', unsafe_allow_html=True)

password_input = st.sidebar.text_input("🔒 Access Portal", type="password", placeholder="Enter Password...")

if password_input == ACCESS_PASSWORD:
    st.sidebar.success("✅ SYSTEM ONLINE")
    st.sidebar.markdown("---")
    
    if API_STATUS:
        st.sidebar.success("✅ License Key Active")
        st.sidebar.info("Authorized for: Lucalles Productions")
        st.sidebar.info("Tier: PAID (Unlimited Quota)")
    else:
        st.sidebar.error("❌ Key Missing")
    
    st.markdown("#### 🎬 Script Ingestion")
    # UPDATED PLACEHOLDER
    user_script = st.text_area("Input Stream", height=300, placeholder="Paste your script here Oppa!", label_visibility="collapsed")
    
    st.write("") # Spacer
    
    if st.button("Initialize Lisa"):
        if user_script:
            # Using the primary paid model for best results
            target_model = "gemini-flash-latest"
            
            # --- STEALTH MODE LOADING TEXT ---
            with st.spinner("Lisa is thinking......"):
                try:
                    model = genai.GenerativeModel(target_model)
                    full_prompt = f"{LISA_SYSTEM_PROMPT}\n\nSCRIPT:\n{user_script}"
                    
                    response = model.generate_content(full_prompt)
                    
                    st.markdown("---")
                    st.success("✅ Analysis Complete")
                    st.markdown("### 📸 Visual Analysis & Prompts")
                    st.markdown(response.text)
                    
                except Exception as e:
                    # Auto-Fallback to Pro if Flash hiccups (rare on paid tier)
                    try:
                        st.warning("⚠️ Flash busy, rerouting to Backup Engine (Pro)...")
                        model = genai.GenerativeModel("gemini-pro")
                        response = model.generate_content(full_prompt)
                        st.markdown(response.text)
                    except Exception as e2:
                        st.error("❌ System Failure")
                        st.code(f"Primary Error: {e}\nBackup Error: {e2}")
        else:
            st.warning("⚠️ Input Buffer Empty")

elif password_input:
    st.sidebar.error("❌ Access Denied")
