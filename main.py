import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="System Scanner")
st.title("🕵️ Model Scanner")

# Load Key
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    st.success("✅ Key Loaded")
except Exception as e:
    st.error(f"Key Error: {e}")
    st.stop()

# Scan for Models
st.write("---")
st.write("### 📡 Contacting Google...")

if st.button("Start Scan"):
    try:
        found_any = False
        # Ask Google for the list
        for m in genai.list_models():
            # We only care about models that can generate text/content
            if 'generateContent' in m.supported_generation_methods:
                st.code(f"{m.name}")
                found_any = True
        
        if not found_any:
            st.warning("⚠️ No models found. Check API Key permissions.")
            
    except Exception as e:
        st.error(f"❌ Scan Failed: {e}")
