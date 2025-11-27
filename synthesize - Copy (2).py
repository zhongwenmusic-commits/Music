import os
from google.cloud import texttospeech

# --- ⚠️ PASTE YOUR PATH HERE ---
# Make sure this matches your "Copy as path" exactly (keep the 'r' at the start)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Google Cloud For TTS\Google Cloud LaBox\file launch.py\json key\crack-willow-479523-a6-39b66c38fc4f.json"

def synthesize_speech(text, output_filename):
    """Converts text to speech and saves it as an MP3 file."""
    
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # --- CHINESE MALE VOICE SETTINGS ---
    # ERROR FIX: Changed 'zh-CN' to 'cmn-CN'
    voice = texttospeech.VoiceSelectionParams(
        language_code="cmn-CN",      # Use 'cmn-CN' for Mandarin
        name="cmn-CN-Wavenet-B"      # Correct ID for the Male WaveNet voice
    )

    # --- AUDIO SETTINGS ---
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        pitch=0.0,           
        speaking_rate=0.5    
    )

    print("Generating audio...")
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Success! Audio content written to file "{output_filename}"')

# --- TEST TEXT ---
input_text = "爸爸" 
output_file = "bàba.mp3"

synthesize_speech(input_text, output_file)

input("Press Enter to exit...")