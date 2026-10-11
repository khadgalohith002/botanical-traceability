/**
 * Web Speech API Service (Speech Recognition & Speech Synthesis)
 * Tailored for multilingual voice assistance in Farmer Mode.
 */

export const speechService = {
  // Check browser support
  isRecognitionSupported() {
    return 'SpeechRecognition' in window || 'webkitSpeechRecognition' in window;
  },

  isSynthesisSupported() {
    return 'speechSynthesis' in window && 'SpeechSynthesisUtterance' in window;
  },

  // Create speech recognition instance
  createRecognizer({ lang = 'en-IN', onResult, onError, onEnd }) {
    if (!this.isRecognitionSupported()) {
      return null;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = lang;

    recognition.onresult = (event) => {
      let finalTranscript = '';
      let interimTranscript = '';

      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript;
        } else {
          interimTranscript += event.results[i][0].transcript;
        }
      }

      if (onResult) {
        onResult({
          transcript: finalTranscript || interimTranscript,
          isFinal: Boolean(finalTranscript),
        });
      }
    };

    recognition.onerror = (event) => {
      if (onError) onError(event.error);
    };

    recognition.onend = () => {
      if (onEnd) onEnd();
    };

    return recognition;
  },

  // Text-to-Speech
  speak(text, lang = 'en-IN') {
    if (!this.isSynthesisSupported() || !text) return;

    window.speechSynthesis.cancel(); // Stop any pending speech

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = lang;
    utterance.rate = 0.95; // Slightly slower, clear pace for farmers
    utterance.pitch = 1.0;

    // Try finding a native voice for the given language
    const voices = window.speechSynthesis.getVoices();
    const matchingVoice = voices.find(v => v.lang.startsWith(lang.split('-')[0]));
    if (matchingVoice) {
      utterance.voice = matchingVoice;
    }

    window.speechSynthesis.speak(utterance);
  },

  stopSpeaking() {
    if (this.isSynthesisSupported()) {
      window.speechSynthesis.cancel();
    }
  },

  // Parse natural spoken phrases for harvest details
  parseHarvestSpeech(text, crops = []) {
    if (!text) return {};
    const result = {};
    const lower = text.toLowerCase();

    // 1. Extract Quantity: looks for numbers followed by kg, kilo, quintal, or standalone numbers
    const numMatch = lower.match(/(\d+)\s*(kg|kilos|kilo|kilograms|quintal)?/);
    if (numMatch) {
      let val = parseInt(numMatch[1], 10);
      if (numMatch[2] === 'quintal') val *= 100;
      if (val > 0) result.harvest_qty_kg = val;
    }

    // 2. Identify Crop
    for (const crop of crops) {
      const matchCommon = lower.includes(crop.common_name.toLowerCase());
      const matchScientific = lower.includes(crop.scientific_name.toLowerCase());
      let matchTrans = false;
      if (crop.translations) {
        matchTrans = Object.values(crop.translations).some(t => lower.includes(t.toLowerCase()));
      }
      if (matchCommon || matchScientific || matchTrans) {
        result.crop_id = crop.id;
        break;
      }
    }

    return result;
  }
};
