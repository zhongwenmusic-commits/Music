import os
from google.cloud import texttospeech

# --- PASTE YOUR PATH BELOW ---
# Remove the quotes from the "Copy as path" if you paste them inside these quotes.
# It should look like: r"C:\Users\...\key.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Google Cloud For TTS\Google Cloud LaBox\file launch.py\json key\crack-willow-479523-a6-39b66c38fc4f.json"

def synthesize_speech(text, output_filename):
    """Converts text to speech and saves it as an MP3 file."""
    
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", 
        name="en-US-Wavenet-F" 
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filename}"')

# --- Run the synthesis ---
input_text = "Hello! This is a test to verify the hardcoded path works."
output_file = "output.mp3"
synthesize_speech(input_text, output_file)