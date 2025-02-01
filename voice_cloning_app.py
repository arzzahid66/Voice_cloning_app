import streamlit as st
import io
import re
from pyht import Client
from pyht.client import TTSOptions

# Replace these with your actual User ID and API key if needed
USER_ID = ""
API_KEY = ""

# Initialize the Client once at the top level
client = Client(user_id=USER_ID, api_key=API_KEY)

def main():
    st.title("AI-Powered Voice Cloning Tool")
    # 1. Input for custom voice link
    st.subheader("Enter the voice link (e.g., s3://...)")
    voice_link = st.text_input(
        label="Voice Link",
        help="Example:s3://voice-cloning-zero-shot/fb8aae6e-deae-4cbc-a068-ad0e110a2c7d/original/manifest.json"
    )

    # 2. Text input for TTS
    st.subheader("Enter text to be spoken (up to 50 words):")
    user_text = st.text_area(
        label="Text Input",
        height=150,
        help="Type or paste the text (max 50 words)."
    )

    # Generate button
    if st.button("Generate Cloned Voice"):
        # Validate inputs
        if not voice_link.strip():
            st.warning("Please provide a voice link before generating the audio.")
            return

        cleaned_text = user_text.strip()
        if not cleaned_text:
            st.warning("Please enter some text before generating the audio.")
            return

        word_count = len(re.findall(r"\S+", cleaned_text))
        if word_count > 50:
            st.error(f"You've entered {word_count} words. Please limit input to 50 words.")
            return

        # Generate and play the audio
        st.info("Generating audio...")
        audio_data = generate_audio(cleaned_text, voice_link)

        if audio_data:
            st.success("Audio generated successfully!")
            st.audio(audio_data, format="audio/mp3")
        else:
            st.error("Failed to generate audio.")

def generate_audio(text: str, voice_link: str) -> bytes:
    """
    Convert the given text to speech using the pyht TTS client
    with a custom voice link. Returns the audio as bytes, or None if an error occurs.
    """
    try:
        # Build TTS options dynamically from the user-provided voice link
        options = TTSOptions(voice=voice_link)

        # Create a buffer for the audio
        audio_buffer = io.BytesIO()
        
        # Call TTS and write chunks to our in-memory buffer
        for chunk in client.tts(text, options, voice_engine='PlayDialog-http'):
            audio_buffer.write(chunk)

        # Reset the buffer to the beginning
        audio_buffer.seek(0)
        return audio_buffer.getvalue()

    except Exception as e:
        st.error(f"Error generating audio: {e}")
        return None

if __name__ == "__main__":
    main()
