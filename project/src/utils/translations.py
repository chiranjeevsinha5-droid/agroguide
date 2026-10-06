import streamlit as st
from googletrans import Translator, LANGUAGES

# Initialize the translator
translator = Translator()

# Use Streamlit's cache to avoid re-translating the same text over and over
@st.cache_data
def translate_text(text, target_lang_code):
    """
    Translates a given text to the target language using Google Translate AI.
    Caches the result to improve performance.
    """
    if not text:
        return ""
    try:
        # If the target is English, just return the original text
        if target_lang_code == 'en':
            return text
        
        translated = translator.translate(text, dest=target_lang_code)
        return translated.text
    except Exception as e:
        # If translation fails, return the original text
        st.error(f"Translation Error: {e}")
        return text

def get_supported_languages():
    """
    Returns a dictionary of supported languages for the dropdown.
    """
    # We can select a few common languages for the UI
    supported = {
        'English': 'en',
        'हिन्दी': 'hi',
        'मराठी': 'mr',
        'বাংলা': 'bn',
        'ગુજરાતી': 'gu',
        'தமிழ்': 'ta',
        'తెలుగు': 'te',
        'ਪੰਜਾਬੀ': 'pa'
    }
    return supported

