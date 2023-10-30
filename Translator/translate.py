import os
import wave
import subprocess
from vosk import Model, KaldiRecognizer
from transformers import MarianTokenizer, MarianMTModel
from flask import Flask, render_template, request

app = Flask(__name__)

os.system('espeak -s 200 -p 5 "Hello, I am Vaak Mitra. Please select your input and output language , and i will do the rest"')
        



# Define the duration of audio recording (in seconds)
audio_duration = 5
audio_file_path = "audio.wav"  # Specify the full path to the audio file

# Define language models for Vosk
language_models = {
    "en": "/home/pi/Desktop/vosk-model-small-en-us-0.15",
    "hi": "/home/pi/Desktop/vosk-model-small-hi-0.22",
    "ja": "/home/pi/Desktop/vosk-model-small-ja-0.22"
    # Add more languages as needed
}


def recognize_speech(audio_file_path, input_lang):
    # Initialize the recognizer with the selected model
    model_path = language_models.get(input_lang)
    if model_path is None:
        return "Language model not found for the selected language."

    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 44100)

    # Open the audio file using the full path
    audio_file = wave.open(audio_file_path, "rb")

    # Read the audio data
    audio_data = audio_file.readframes(audio_file.getnframes())

    # Perform speech recognition
    recognizer.AcceptWaveform(audio_data)

    # Get the recognized text
    result = recognizer.Result()
    text = result[14:-3]

    return text

def translate_text(text, input_lang, output_lang):
    if input_lang==output_lang:
         return "Input and output language cannot be same"
    
    
    # Initialize the Marian tokenizer and translation model based on the user's selected languages
    model_name = f"Helsinki-NLP/opus-mt-{input_lang}-{output_lang}"
    if input_lang=="en" and output_lang=="ja":
        model_name=f"Helsinki-NLP/opus-tatoeba-en-ja"
        
        
        
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    # Split the input text into smaller segments
    max_length = 150  # Adjust the max_length as needed
    split_texts = [text[i:i + max_length] for i in range(0, len(text), max_length)]

    # Initialize an empty list to store translations
    translations = []

    # Translate each segment
    for split_text in split_texts:
        inputs = tokenizer(
            split_text,
            return_tensors="pt",
            padding="max_length",
            max_length=max_length,
            truncation=True,
        )

        translated_ids = model.generate(inputs["input_ids"], max_length=200, num_beams=5, early_stopping=True)

        # Decode and add the translation to the list
        translated_text = tokenizer.decode(translated_ids[0], skip_special_tokens=True)
        translations.append(translated_text)

    # Combine the translations into a single string
    translated_text = " ".join(translations)

    return translated_text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_lang = request.form['input_lang']
        output_lang = request.form['output_lang']

        # Record audio using arecord
        subprocess.run(["arecord", "-d", str(audio_duration), "-f", "S16_LE", "-r", "44100", "-c", "1", "-t", "wav", "-D", "hw:3,0", audio_file_path])
        
        os.system('espeak -s 150 -p 5 "Processing your audio , Please Wait"')
        # Perform speech recognition with the selected input language
        recognized_text = recognize_speech(audio_file_path, input_lang)

        # Translate the recognized text
        translated_text = translate_text(recognized_text, input_lang, output_lang)
        
        print("Recognized",recognized_text)
        print("Translated",translated_text)
        # Use eSpeak to speak the translated text
        os.system(f'espeak -s 150 -p 5 "{translated_text}"')
    
        # Delete the audio file after processing
        os.remove(audio_file_path)
        return render_template('index.html', recognized_text=recognized_text, translated_text=translated_text)

    return render_template('index.html')
    
@app.route('/about', methods=['GET', 'POST'])
def speak():
    if request.method == 'POST':
        text_to_speak = request.form['text_to_speak']
        input_lang = request.form['input_lang']
        output_lang = request.form['output_lang']

        # Translate the input text
        translated_text = translate_text(text_to_speak, input_lang, output_lang)

        # Use eSpeak to speak the translated text
        os.system(f'espeak -s 150 -p 5 "{translated_text}"')

        # Render the speak.html template and pass the translated text
        return render_template('speak.html', translated_text=translated_text)

    # Render the speak.html template without translated text if it's a GET request
    return render_template('speak.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
