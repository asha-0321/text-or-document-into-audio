import streamlit as st
pip install gtts
from gtts import gTTS
from googletrans import Translator
import os
import base64
from PyPDF2 import PdfReader
import docx2txt
!pip install gtts

# Dictionary to map language codes to full names
LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "es": "Spanish",
    "te": "Telugu",
    "fr": "French",
    "it": "Italian",
    "gu": "Gujarati",
    "mr": "Marathi",
    "ta": "Tamil",
    "ur": "Urdu",
    "bn": "Bengali",
    "de": "German",
    "pt": "Portuguese",
    "nl": "Dutch",
    "ja": "Japanese",
    "ko": "Korean",
    "ru": "Russian",
    "ar": "Arabic",
    "th": "Thai",
    "tr": "Turkish",
    "pl": "Polish",
    "cs": "Czech",
    "sv": "Swedish",
    "da": "Danish",
    "fi": "Finnish",
    "el": "Greek",
    "hu": "Hungarian",
    "uk": "Ukrainian",
    "no": "Norwegian",
    "id": "Indonesian",
    "vi": "Vietnamese",
    "ro": "Romanian",
    "fa": "Persian",
    "iw": "Hebrew",
    "bg": "Bulgarian",
    "ca": "Catalan",
    "hr": "Croatian",
    "sr": "Serbian",
    "sk": "Slovak",
    "sl": "Slovenian",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "et": "Estonian",
    "is": "Icelandic",
    "ga": "Irish",
    "sq": "Albanian",
    "mk": "Macedonian",
    "hy": "Armenian",
    "ka": "Georgian",
    "ne": "Nepali",
    "si": "Sinhala",
    "km": "Khmer",
    "jw": "Javanese"
}

# Function to translate text
def translate_text(text, target_language='en'):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text

# Function to convert text to speech and save as an MP3 file
def convert_text_to_speech(text, output_file, language='en'):
    if text:
        tts = gTTS(text=text, lang=language)
        tts.save(output_file)
        return True
    return False

# Function to generate a download link for a file
def get_binary_file_downloader_html(link_text, file_path, file_format):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    b64_file = base64.b64encode(file_data).decode()
    download_link = f'<a href="data:{file_format};base64,{b64_file}" download="{os.path.basename(file_path)}">{link_text}</a>'
    return download_link

def main():
    st.title("Text to Audio Conversion")

    # Get user input
    input_option = st.selectbox("Choose input type", ["Text", "File"])

    text = ""
    if input_option == "Text":
        text = st.text_area("Enter text to convert to speech:", height=300)
    elif input_option == "File":
        uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "docx"])
        if uploaded_file is not None:
            if uploaded_file.type == "text/plain":
                text = str(uploaded_file.read(), "utf-8")
            elif uploaded_file.type == "application/pdf":
                pdf_reader = PdfReader(uploaded_file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                text = docx2txt.process(uploaded_file)

    target_language_name = st.selectbox("Select text language:", list(LANGUAGES.values()))

    # Get the corresponding language code
    target_language_code = [code for code, name in LANGUAGES.items() if name == target_language_name][0]

    # Add a button to trigger the text-to-speech conversion
    if st.button("Convert to Speech and Download Audio"):
        output_file = "output.mp3"
        
        # Translate text to the selected language
        translated_text = translate_text(text, target_language_code)

        # Display the translated text
        st.write("Translated Text:")
        st.write(translated_text)

        # Convert translated text to speech
        success = convert_text_to_speech(translated_text, output_file, language=target_language_code)

        if success:
            # Play the generated speech
            audio_file = open(output_file, 'rb')
            st.audio(audio_file.read(), format='audio/mp3')

            # Provide a download link for the MP3 file
            st.markdown(get_binary_file_downloader_html("Download Audio File", output_file, 'audio/mp3'), unsafe_allow_html=True)
        else:
            st.warning("Failed to generate audio. Please check your input.")

if __name__ == "__main__":
    main()
