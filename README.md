# vaakmitra
the code base of an offline translator 

This project aims to develop an offline speech translation system to facilitate communication in regions with poor internet connectivity. The system utilizes AI-based techniques for speech recognition and translation, allowing users to converse in different languages without requiring an internet connection.

## Features

- Speech Recognition: Utilizes advanced speech recognition algorithms to transcribe spoken language into text.
- Language Translation: Translates transcribed text into the desired target language using machine translation models.
- Offline Functionality: Works seamlessly without an internet connection, making it ideal for use in areas with limited connectivity.
- User-Friendly Interface: Provides an intuitive interface for users to interact with the system, enabling easy communication in multiple languages.

## Technologies Used

- PyTorch: Deep learning framework used for speech recognition.
- Marian NMT: Neural machine translation framework for language translation.
- Flask: Lightweight web framework for building the server-side component of the system.
- Raspberry Pi: Hardware platform used for deploying the offline translator system.
- Vosk: State-of-the-art speech recognition toolkit optimized for Raspberry Pi.

## Installation

1. Clone the repository into raspberry pi4: git clone https://github.com/your-username/offline-translator.git
2.  Install dependencies:
pip install -r requirements.txt
3. Run the server:
python app.py

4. Access the system through a web browser at `http://localhost:5000`.

## Usage

1. Speak into the microphone to provide input in the source language.
2. Wait for the system to transcribe the speech into text.
3. Select the target language for translation.
4. View the translated text on the user interface.

## Contributing

Contributions are welcome! Feel free to submit bug reports, feature requests, or pull requests to help improve the project.

## License

This project is licensed under the [MIT License](LICENSE).
