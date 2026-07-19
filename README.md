# 🎙️ Multilingual AI Voice Assistant

A Python-based AI voice assistant that listens, understands, and responds in multiple major Indian languages. Built with **FastAPI**, **SpeechRecognition**, and **gTTS**, it converts spoken input into text, processes the query, and replies back with natural voice output — all through a simple web interface.

---

## ✨ Features

- 🎤 **Speech-to-Text** — Captures and transcribes voice input using the `SpeechRecognition` library
- 🌐 **Multilingual Support** — Understands and responds in all major Indian languages
- 🔊 **Text-to-Speech** — Converts responses into natural-sounding speech using `gTTS` (Google Text-to-Speech)
- ⚡ **FastAPI Backend** — Lightweight, high-performance REST API powering the assistant
- 🖥️ **Web Interface** — Simple HTML/CSS/JS frontend to interact with the assistant directly from the browser

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Speech Recognition | SpeechRecognition |
| Text-to-Speech | gTTS (Google Text-to-Speech) |
| Frontend | HTML5, CSS3, JavaScript |

---

## 📁 Project Structure

```
Multilingual-AI-Voice-Assistant/
│
├── linguaai/              # Core application (backend + frontend)
│   ├── main.py             # FastAPI app entry point
│   ├── static/              # CSS & JavaScript files
│   ├── templates/            # HTML templates
│   └── ...
│
├── requirements.txt        # Python dependencies
└── README.md
```

> Note: Update the structure above if your actual folder layout differs.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- pip
- A working microphone (for voice input)

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/gudduKumar548/Multilingual-AI-Voice-Assistant.git
   cd Multilingual-AI-Voice-Assistant/linguaai
   ```

2. Create a virtual environment (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Run the FastAPI server
   ```bash
   uvicorn main:app --reload
   ```

5. Open your browser and go to
   ```
   http://127.0.0.1:8000
   ```

---

## 🎯 Usage

1. Open the web interface in your browser.
2. Click the microphone icon and speak your query in your preferred Indian language.
3. The assistant transcribes your speech, processes the query, and responds back with voice output.

---

## 🗣️ Supported Languages

Supports all major Indian languages including Hindi, English, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi, and more.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add your feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Guddu Kumar**
- GitHub: [@gudduKumar548](https://github.com/gudduKumar548)
- LinkedIn: [guddu-kumar](https://linkedin.com/in/guddu-kumar-b3b534258)
- Email: contactgk01@gmail.com
