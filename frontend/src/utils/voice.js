const VOICE_API_BASE_URL = (import.meta.env.VITE_VOICE_API_BASE_URL || '').replace(/\/$/, '');

const VOICE_PREFERENCES = {
  en: { name: 'English', exact: ['en-in', 'en-us'], prefix: 'en' },
  as: { name: 'Assamese', exact: ['as-in'], prefix: 'as' },
  hi: { name: 'Hindi', exact: ['hi-in'], prefix: 'hi' },
  kn: { name: 'Kannada', exact: ['kn-in'], prefix: 'kn' },
};

let activeAudio = null;
let activePlayback = null;
let voiceRequestId = 0;

function voiceApiUrl(path) {
  return `${VOICE_API_BASE_URL}${path}`;
}

function getSpeechSynthesis() {
  return typeof window !== 'undefined' && 'speechSynthesis' in window
    ? window.speechSynthesis
    : null;
}

function stopActivePlayback() {
  if (activeAudio) {
    activeAudio.pause();
    activeAudio.currentTime = 0;
    activeAudio = null;
  }

  const speechSynthesis = getSpeechSynthesis();
  speechSynthesis?.cancel();

  if (activePlayback) {
    activePlayback.finish({ success: false, cancelled: true });
  }
}

export function stopVoicePlayback() {
  voiceRequestId += 1;
  stopActivePlayback();
}

export async function getVoiceLanguages() {
  const response = await fetch(voiceApiUrl('/voice/languages'));
  if (!response.ok) {
    throw new Error('Voice languages could not be loaded.');
  }

  const data = await response.json();
  return Array.isArray(data.languages) ? data.languages : [];
}

async function getAvailableSpeechVoices(speechSynthesis) {
  let voices = speechSynthesis.getVoices();
  if (voices.length > 0) {
    return voices;
  }

  await new Promise((resolve) => {
    const timeout = window.setTimeout(done, 1500);

    function done() {
      window.clearTimeout(timeout);
      speechSynthesis.removeEventListener?.('voiceschanged', done);
      resolve();
    }

    speechSynthesis.addEventListener?.('voiceschanged', done, { once: true });
  });

  voices = speechSynthesis.getVoices();
  return voices;
}

function selectSpeechVoice(voices, language) {
  const preference = VOICE_PREFERENCES[language];
  if (!preference) {
    return null;
  }

  const normalized = voices.map((voice) => ({ voice, locale: voice.lang.toLowerCase() }));
  for (const locale of preference.exact) {
    const match = normalized.find((item) => item.locale === locale);
    if (match) {
      return match.voice;
    }
  }

  return normalized.find((item) => item.locale === preference.prefix || item.locale.startsWith(`${preference.prefix}-`))?.voice || null;
}

function createPlayback(resolve) {
  const playback = {
    settled: false,
    finish(result) {
      if (playback.settled) {
        return;
      }

      playback.settled = true;
      if (activePlayback === playback) {
        activePlayback = null;
      }
      resolve(result);
    },
  };
  activePlayback = playback;
  return playback;
}

function playRecordedAudio(audioUrl) {
  return new Promise((resolve) => {
    const playback = createPlayback(resolve);
    const audio = new Audio(voiceApiUrl(audioUrl));
    activeAudio = audio;

    audio.onended = () => playback.finish({ success: true, mode: 'recorded_audio' });
    audio.onerror = () => playback.finish({ success: false, error: 'Recorded audio could not be played.' });
    audio.play().catch(() => playback.finish({ success: false, error: 'Recorded audio could not be played.' }));
  });
}

async function speakWithBrowserTts(text, language, requestId) {
  const speechSynthesis = getSpeechSynthesis();
  if (!speechSynthesis) {
    return { success: false, error: 'Browser text-to-speech is unavailable.' };
  }

  const voice = selectSpeechVoice(await getAvailableSpeechVoices(speechSynthesis), language);
  if (requestId !== voiceRequestId) {
    return { success: false, cancelled: true };
  }
  if (!voice) {
    const languageName = VOICE_PREFERENCES[language]?.name || language;
    return { success: false, error: `${languageName} speech is not installed in this browser.` };
  }

  return new Promise((resolve) => {
    const playback = createPlayback(resolve);
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.voice = voice;
    utterance.lang = voice.lang;
    utterance.rate = 0.85;
    utterance.pitch = 1;
    utterance.onend = () => playback.finish({ success: true, mode: 'browser_tts' });
    utterance.onerror = () => playback.finish({ success: false, error: 'Browser text-to-speech could not play.' });
    speechSynthesis.resume();
    speechSynthesis.speak(utterance);
  });
}

export async function speakVoicePrompt(language, key) {
  const requestId = ++voiceRequestId;
  stopActivePlayback();

  let prompt;
  try {
    const response = await fetch(voiceApiUrl(`/voice/prompt/${language}/${key}`));
    prompt = await response.json();
  } catch {
    return { success: false, error: 'Voice service is unavailable.' };
  }

  if (requestId !== voiceRequestId) {
    return { success: false, cancelled: true };
  }

  if (!prompt.success || !prompt.text) {
    return { success: false, error: prompt.error || 'Voice prompt is unavailable.' };
  }

  if (prompt.audio_available && prompt.audio_url) {
    const audioResult = await playRecordedAudio(prompt.audio_url);
    if (audioResult.success || audioResult.cancelled || requestId !== voiceRequestId) {
      return audioResult;
    }
  }

  return speakWithBrowserTts(prompt.text, language, requestId);
}
