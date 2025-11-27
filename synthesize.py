import tkinter as tk
from tkinter import messagebox, scrolledtext
from google.cloud import texttospeech
import os
import threading 

# ==========================================
# 1. SETUP AUTHENTICATION (Your Exact Path)
# ==========================================
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Google Cloud For TTS\Google Cloud LaBox\file launch.py\json key\crack-willow-479523-a6-39b66c38fc4f.json"

# ==========================================
# 2. THE GENERATION LOGIC
# ==========================================
def run_batch_generation():
    # Disable button
    btn_generate.config(state=tk.DISABLED, text="Working...")
    
    # Get text
    raw_text = text_input.get("1.0", tk.END).strip()
    
    # Get Settings from Sliders
    user_pitch = scale_pitch.get()
    user_speed = scale_speed.get()

    if not raw_text:
        messagebox.showerror("Error", "The box is empty!")
        btn_generate.config(state=tk.NORMAL, text="Generate Batch")
        return

    items = raw_text.split('|')
    total_count = len(items)
    success_count = 0
    errors = []

    try:
        # Initialize Client
        client = texttospeech.TextToSpeechClient()
        
        # Voice Settings (Mandarin Male)
        voice = texttospeech.VoiceSelectionParams(
            language_code="cmn-CN",
            name="cmn-CN-Wavenet-B"
        )
        
        # Audio Settings (Using User Inputs)
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            pitch=user_pitch,          # Read from Pitch Slider
            speaking_rate=user_speed   # Read from Speed Slider
        )

        # LOOP through items
        for index, item in enumerate(items):
            item = item.strip()
            if not item: continue 

            try:
                parts = item.split()
                if len(parts) >= 2:
                    hanzi_text = parts[0]
                    filename_text = parts[1]
                else:
                    hanzi_text = parts[0]
                    filename_text = parts[0]

                # Update Status
                status_label.config(text=f"Processing {index+1}/{total_count}: {hanzi_text}...", fg="blue")
                root.update() 

                # Call API
                synthesis_input = texttospeech.SynthesisInput(text=hanzi_text)
                response = client.synthesize_speech(
                    input=synthesis_input, voice=voice, audio_config=audio_config
                )

                # Save File
                filename = f"{filename_text}.mp3"
                with open(filename, "wb") as out:
                    out.write(response.audio_content)
                
                success_count += 1

            except Exception as e:
                print(f"Error on {item}: {e}")
                errors.append(item)

        # FINISHED
        status_label.config(text=f"Done! Created {success_count} files.", fg="green")
        if errors:
            messagebox.showwarning("Completed with Errors", f"Errors: {', '.join(errors)}")
        else:
            messagebox.showinfo("Success", f"All {success_count} files generated!")

    except Exception as main_e:
        messagebox.showerror("Critical Error", f"API Error:\n{main_e}")
        status_label.config(text="Critical Error", fg="red")

    btn_generate.config(state=tk.NORMAL, text="Generate Batch")

def start_thread():
    threading.Thread(target=run_batch_generation).start()

# ==========================================
# 3. USER INTERFACE
# ==========================================
root = tk.Tk()
root.title("Batch Chinese Audio Generator (+Settings)")
root.geometry("600x650") # Made taller for settings

# --- Instructions ---
instr_label = tk.Label(root, text="Format: Hanzi Pinyin | Hanzi Pinyin", font=("Arial", 11))
instr_label.pack(pady=(10, 5))
example_label = tk.Label(root, text="Example: 你好 nihao | 谢谢 xiexie", font=("Arial", 9, "italic"), fg="gray")
example_label.pack(pady=(0, 10))

# --- Text Box ---
text_input = scrolledtext.ScrolledText(root, width=60, height=12, font=("Arial", 12))
text_input.pack(pady=5, padx=10)

# --- SETTINGS FRAME ---
settings_frame = tk.LabelFrame(root, text="Voice Settings", font=("Arial", 10, "bold"), padx=10, pady=10)
settings_frame.pack(pady=10, fill="x", padx=20)

# Pitch Slider
tk.Label(settings_frame, text="Pitch (Low to High):").pack(anchor="w")
scale_pitch = tk.Scale(settings_frame, from_=-10.0, to=10.0, resolution=0.1, orient=tk.HORIZONTAL, length=500)
scale_pitch.set(0.0) # Default
scale_pitch.pack()

# Speed Slider
tk.Label(settings_frame, text="Speed (Slow to Fast):").pack(anchor="w")
scale_speed = tk.Scale(settings_frame, from_=0.5, to=2.0, resolution=0.05, orient=tk.HORIZONTAL, length=500)
scale_speed.set(1.0) # Default
scale_speed.pack()

# --- Generate Button ---
btn_generate = tk.Button(root, text="Generate All Files", font=("Arial", 12, "bold"), 
                         bg="#4CAF50", fg="white", height=2, width=20, 
                         command=start_thread)
btn_generate.pack(pady=20)

# --- Status ---
status_label = tk.Label(root, text="Ready", font=("Arial", 10, "bold"))
status_label.pack(side=tk.BOTTOM, pady=10)

root.mainloop()