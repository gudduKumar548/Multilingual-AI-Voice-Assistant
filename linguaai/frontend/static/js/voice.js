
let recognition = null;
let isListening = false;
let currentAudio = null;

function toggleMic() {
  if (isListening) stopListening();
  else startListening();
}

function startListening() {
  if (!("webkitSpeechRecognition" in window || "SpeechRecognition" in window)) {
    alert("Voice input not supported. Please use Chrome or Edge.");
    return;
  }

  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = true;
  recognition.lang = document.getElementById("lang-select").value;

  recognition.onstart = () => {
    isListening = true;
    document.getElementById("mic-btn").classList.add("listening");
    document.getElementById("mic-dot").className = "status-dot pulse";
    document.getElementById("mic-status").textContent = "Listening...";
    document.getElementById("voice-banner").classList.remove("hidden");
  };

  recognition.onresult = (e) => {
    const transcript = Array.from(e.results)
      .map((r) => r[0].transcript)
      .join("");
    document.getElementById("chat-input").value = transcript;
    document.getElementById("voice-text").textContent = "🎤 " + transcript;
    autoResize(document.getElementById("chat-input"));
    if (e.results[e.results.length - 1].isFinal) {
      stopListening();
      sendMessage(transcript);
    }
  };

  recognition.onerror = (e) => {
    stopListening();
    if (e.error !== "aborted") alert("Mic error: " + e.error);
  };

  recognition.onend = () => stopListening();
  recognition.start();
}

function stopListening() {
  isListening = false;
  recognition?.stop();
  document.getElementById("mic-btn").classList.remove("listening");
  document.getElementById("mic-dot").className = "status-dot green";
  document.getElementById("mic-status").textContent = "Mic ready";
  document.getElementById("voice-banner").classList.add("hidden");
  document.getElementById("voice-text").textContent = "Listening...";
}

async function speakText(text, lang) {
  try {
    // Stop any currently playing audio
    if (currentAudio) {
      currentAudio.pause();
      currentAudio = null;
    }

    const token = localStorage.getItem("lingua_token");
    const res = await fetch("http://localhost:8000/api/tts/speak", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
      body: JSON.stringify({ text: text, lang: lang }),
    });

    if (!res.ok) {
      // fallback to browser TTS if gTTS fails
      fallbackSpeak(text, lang);
      return;
    }

    const audioBlob = await res.blob();
    const audioUrl = URL.createObjectURL(audioBlob);
    currentAudio = new Audio(audioUrl);
    currentAudio.play();

    // Clean up URL after playing
    currentAudio.onended = () => {
      URL.revokeObjectURL(audioUrl);
      currentAudio = null;
    };
  } catch (err) {
    // fallback to browser TTS
    fallbackSpeak(text, lang);
  }
}

// Fallback — browser TTS if gTTS fails
function fallbackSpeak(text, lang) {
  if (!window.speechSynthesis) return;
  const utt = new SpeechSynthesisUtterance(text);
  utt.lang = lang;
  utt.rate = 0.95;
  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(utt);
}
