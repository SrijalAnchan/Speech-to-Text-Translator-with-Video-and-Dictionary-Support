import tempfile
import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import ttkbootstrap as tb
import pytube
from moviepy.editor import VideoFileClip, AudioFileClip
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import pygame
from pydub import AudioSegment

# Initialize the recognizer and translator
recognizer = sr.Recognizer()
translator = Translator()

# Initialize pygame mixer
pygame.mixer.init()

# Supported languages
languages = {
    "Malayalam": "ml",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Sanskrit": "sa",
    "Arabic": "ar",
    "Gujarati": "gu",
    "Odia": "or",
}

# List to store translation history
history = []

# Function to update history
def update_history(original, translation):
    history.append((original, translation))

# Function to recognize speech and translate
def recognize_and_translate():
    with sr.Microphone() as source:
        status_label.config(text="Listening...", bootstyle="info")
        root.update()  # Refresh the GUI

        try:
            voice = recognizer.listen(source, timeout=20, phrase_time_limit=10)
            text = recognizer.recognize_google(voice, language="en")
            status_label.config(text=f"Recognized: {text}", bootstyle="success")
            root.update()  # Refresh the GUI

            target_language = language_var.get()
            translation = translate_text(text, languages[target_language])
            translation_label.config(text=f"Translation: {translation}")
            root.update()  # Refresh the GUI

            # Update history
            update_history(text, translation)

            # Pronounce the translated text in a new thread
            threading.Thread(target=pronounce_translation, args=(translation, languages[target_language])).start()

        except sr.UnknownValueError:
            messagebox.showerror("Error", "Could not understand audio")
        except sr.RequestError as e:
            messagebox.showerror("Error", f"Request error: {e}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def translate_text(text, target_lang):
    max_length = 5000  # Max length for Google Translate API
    translated_text = ""

    if len(text) > max_length:
        parts = [text[i:i + max_length] for i in range(0, len(text), max_length)]
        for part in parts:
            translated_part = translator.translate(part, dest=target_lang).text
            translated_text += translated_part + " "
    else:
        translated_text = translator.translate(text, dest=target_lang).text

    return translated_text.strip()

def pronounce_translation(text, lang):
    try:
        tts = gTTS(text=text, lang=lang)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            temp_filename = fp.name
            tts.save(temp_filename)

        pygame.mixer.music.load(temp_filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():  # wait for the sound to finish playing
            continue

        os.remove(temp_filename)
    except Exception as e:
        messagebox.showerror("Error", f"Could not play the translation: {e}")

def clear_text():
    status_label.config(text="Click 'Recognize Speech' to start", bootstyle="secondary")
    translation_label.config(text="")
    root.update()

def fetch_dictionary_meaning():
    word = word_entry.get()
    if word:
        target_language = language_var.get()
        translation = translator.translate(word, dest=languages[target_language])
        meaning_label.config(text=f"Meaning: {translation.text}")
        root.update()
    else:
        messagebox.showwarning("Warning", "Please enter a word to look up!")

def login():
    username = username_entry.get()
    password = password_entry.get()

    # Simulate authentication (replace with actual authentication logic)
    if username == "user" and password == "password":
        # Enable translation section after successful login
        frame.pack()
        dictionary_frame.pack()
        login_frame.pack_forget()  # Hide login frame
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def open_history_window():
    history_window = tk.Toplevel(root)
    history_window.title("Translation History")
    history_window.geometry("600x400")
    history_window.configure(background='lightblue')

    history_label = ttk.Label(history_window, text="Translation History:", bootstyle='primary')
    history_label.pack(pady=10)

    history_text = tk.Text(history_window, wrap=tk.WORD, font=('Helvetica', 12))
    history_text.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    for original, translation in history:
        history_text.insert(tk.END, f"Original: {original}\nTranslation: {translation}\n\n")

    history_text.config(state=tk.DISABLED)  # Make the history read-only

def download_video(video_path):
    video = VideoFileClip(video_path)
    audio_path = video_path.replace('.mp4', '.wav')
    video.audio.write_audiofile(audio_path)
    return audio_path

def transcribe_audio(audio_path):
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        return text

def translate_video():
    video_path = filedialog.askopenfilename(title="Select Video File", filetypes=(("MP4 files", ".mp4"), ("All files", ".*")))
    if not video_path:
        messagebox.showwarning("Warning", "Please select a video file!")
        return

    try:
        # Step 1: Extract audio from the video
        audio_path = download_video(video_path)

        # Step 2: Transcribe the audio to text
        transcribed_text = transcribe_audio(audio_path)
        print(f"Transcribed Text: {transcribed_text}")

        # Step 3: Translate the text
        target_language = language_var.get()
        translated_text = translate_text(transcribed_text, languages[target_language])
        print(f"Translated Text: {translated_text}")

        # Step 4: Convert the translated text to speech
        tts = gTTS(text=translated_text, lang=languages[target_language])
        translated_audio_path = audio_path.replace('.wav', '_translated.mp3')
        tts.save(translated_audio_path)

        # Step 5: Replace the original audio in the video with the translated audio
        original_video = VideoFileClip(video_path)
        translated_audio = AudioFileClip(translated_audio_path)
        translated_video_path = video_path.replace('.mp4', '_translated.mp4')

        # Set the translated audio as the new audio for the video
        new_video = original_video.set_audio(translated_audio)
        new_video.write_videofile(translated_video_path, codec='libx264', audio_codec='aac')

        messagebox.showinfo("Success", f"Translated video saved as {translated_video_path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main Tkinter window
root = tb.Window(themename="cosmo")
root.title("Speech to Regional Language Translator with Dictionary")
root.geometry("800x600")  # Set the window size
root.configure(background='#e1f5fe')  # Set background color to light blue

# Create login frame
login_frame = ttk.Frame(root)
login_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Create and place login form widgets
username_label = ttk.Label(login_frame, text="Username:", bootstyle='info')
username_label.pack(pady=10)
username_entry = ttk.Entry(login_frame, width=30)
username_entry.pack(pady=5)

password_label = ttk.Label(login_frame, text="Password:", bootstyle='info')
password_label.pack(pady=10)
password_entry = ttk.Entry(login_frame, width=30, show="*")
password_entry.pack(pady=5)

login_button = ttk.Button(login_frame, text="Login", command=login, bootstyle='success')
login_button.pack(pady=10)

# Create and place frames for better layout control
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Create and place labels
status_label = ttk.Label(frame, text="Click 'Recognize Speech' to start", wraplength=600, bootstyle='info')
status_label.pack(pady=10)

translation_label = ttk.Label(frame, text="", wraplength=600)
translation_label.pack(pady=10)

# Create and place language selection dropdown
language_var = tk.StringVar(value="Malayalam")
language_label = ttk.Label(frame, text="Select Target Language:", bootstyle='info')
language_label.pack(pady=10)
language_menu = ttk.OptionMenu(frame, language_var, *languages.keys())
language_menu.pack(pady=10)

# Create and place the recognize button
recognize_button = ttk.Button(frame, text="Recognize Speech", command=recognize_and_translate, bootstyle='primary')
recognize_button.pack(pady=10)

# Create and place the clear button
clear_button = ttk.Button(frame, text="Clear", command=clear_text, bootstyle='secondary')
clear_button.pack(pady=10)

# Create and place the translation history button
history_button = ttk.Button(frame, text="Translation History", command=open_history_window, bootstyle='warning')
history_button.pack(pady=10)

# Create and place the video translation button
video_translate_button = ttk.Button(frame, text="Translate Video", command=translate_video, bootstyle='success')
video_translate_button.pack(pady=10)

# Dictionary lookup frame
dictionary_frame = ttk.Frame(root)
dictionary_label = ttk.Label(dictionary_frame, text="Dictionary Lookup", bootstyle='info')
dictionary_label.pack(pady=10)
word_label = ttk.Label(dictionary_frame, text="Enter Word:", bootstyle='info')
word_label.pack(pady=10)
word_entry = ttk.Entry(dictionary_frame, width=30)
word_entry.pack(pady=5)
lookup_button = ttk.Button(dictionary_frame, text="Lookup Meaning", command=fetch_dictionary_meaning, bootstyle='success')
lookup_button.pack(pady=10)
meaning_label = ttk.Label(dictionary_frame, text="", wraplength=600)
meaning_label.pack(pady=10)

# Hide the main frame initially (only show login frame)
frame.pack_forget()
dictionary_frame.pack_forget()

# Start the Tkinter main loop
root.mainloop()