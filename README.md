# Speech-to-Text-Translator-with-Video-and-Dictionary-Support

This project is a **Tkinter-based GUI application** designed for real-time speech recognition, translation, and video translation into various regional languages. It also features a dictionary lookup for individual words. The app leverages **Google's Speech Recognition** and **Google Translate API** to offer an easy-to-use interface for users to convert spoken English into several supported languages, both for speech and video translations.

## Features
1. **Speech Recognition & Translation**:
   - Recognizes spoken English through a microphone.
   - Translates the recognized text into a user-selected regional language (supports languages like Malayalam, Hindi, Tamil, etc.).
   - Converts the translated text to speech and plays it back using Google Text-to-Speech (gTTS).

2. **Video Translation**:
   - Extracts audio from a video file (.mp4).
   - Transcribes the extracted audio into text.
   - Translates the transcribed text into a selected language.
   - Replaces the video’s original audio with the translated audio and saves it as a new video.

3. **Dictionary Lookup**:
   - Allows users to enter individual words and get translations in their chosen language.
   
4. **Translation History**:
   - Keeps a log of recognized and translated text, which users can view in a separate window.

5. **User Login**:
   - Simulates a login process that unlocks the translation features after successful authentication.


## How it Works
1. **Speech Translation**:
   - After logging in, the user selects a target language from the dropdown.
   - The app listens to the user's speech and displays the recognized text.
   - The text is translated into the selected language and can be played back as audio.
   
2. **Video Translation**:
   - Users can upload a video file, extract its audio, transcribe and translate it.
   - The translated audio replaces the original in the video, and the app saves the new version.

3. **Dictionary**:
   - Users can look up words in the selected language by entering the word in the dictionary section.

## How to Run
1. Clone the repository.
2. Install the necessary Python libraries from the `requirements.txt` file.
3. Run the script, and a GUI window will open where you can log in and start using the features.

## Future Enhancements
- Add YouTube video support via the `pytube` library to allow direct video downloads and translation.
