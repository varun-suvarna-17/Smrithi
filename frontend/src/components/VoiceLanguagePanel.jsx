import React, { useEffect, useState } from 'react';
import { Volume2 } from 'lucide-react';
import { getVoiceLanguages, speakVoicePrompt } from '../utils/voice';

const FALLBACK_LANGUAGES = [
  { code: 'en', name: 'English' },
  { code: 'as', name: 'Assamese' },
  { code: 'hi', name: 'Hindi' },
  { code: 'kn', name: 'Kannada' },
];

export default function VoiceLanguagePanel({ selectedLanguage, onLanguageChange }) {
  const [languages, setLanguages] = useState(FALLBACK_LANGUAGES);
  const [message, setMessage] = useState('');
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    let isMounted = true;

    getVoiceLanguages()
      .then((availableLanguages) => {
        if (isMounted && availableLanguages.length > 0) {
          setLanguages(availableLanguages);
        }
      })
      .catch(() => {
        if (isMounted) {
          setMessage('Voice service is unavailable. You can try again later.');
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  const selectedLanguageName = languages.find((language) => language.code === selectedLanguage)?.name || selectedLanguage;

  const handleTestVoice = async () => {
    setIsPlaying(true);
    setMessage('');
    const result = await speakVoicePrompt(selectedLanguage, 'welcome');
    setIsPlaying(false);
    setMessage(result.success ? `Playing ${selectedLanguageName} welcome message.` : result.error);
  };

  return (
    <section style={styles.card} aria-labelledby="voice-language-heading">
      <div style={styles.titleRow}>
        <div style={styles.iconCircle}><Volume2 size={22} /></div>
        <div>
          <h2 id="voice-language-heading" style={styles.title}>Voice &amp; Language</h2>
          <p style={styles.subtitle}>Smrithi will speak game instructions in your selected language.</p>
        </div>
      </div>

      <div style={styles.controls}>
        <label style={styles.label} htmlFor="voice-language">Choose your language</label>
        <select
          id="voice-language"
          value={selectedLanguage}
          onChange={(event) => onLanguageChange(event.target.value)}
          style={styles.select}
        >
          {languages.map((language) => (
            <option key={language.code} value={language.code}>{language.name}</option>
          ))}
        </select>
        <button type="button" onClick={handleTestVoice} disabled={isPlaying} style={styles.testButton}>
          <Volume2 size={19} /> {isPlaying ? 'Playing…' : 'Test Voice'}
        </button>
      </div>

      <p style={styles.currentLanguage}>Current language: <strong>{selectedLanguageName}</strong></p>
      {message && <p role="status" style={styles.message}>{message}</p>}
    </section>
  );
}

const styles = {
  card: {
    backgroundColor: 'var(--surface-color)',
    border: '1px solid var(--border-color)',
    borderRadius: 'var(--radius-lg)',
    padding: '22px 24px',
    boxShadow: 'var(--shadow-card)',
    marginBottom: '28px',
  },
  titleRow: { display: 'flex', alignItems: 'center', gap: '14px', marginBottom: '18px' },
  iconCircle: { width: '42px', height: '42px', borderRadius: '50%', backgroundColor: 'var(--secondary-green)', color: 'var(--primary-green)', display: 'flex', alignItems: 'center', justifyContent: 'center' },
  title: { color: 'var(--primary-green)', fontSize: '1.2rem', fontWeight: '800' },
  subtitle: { color: 'var(--text-muted)', fontSize: '0.92rem', marginTop: '2px' },
  controls: { display: 'flex', alignItems: 'end', gap: '14px', flexWrap: 'wrap' },
  label: { color: 'var(--text-main)', display: 'block', fontSize: '0.9rem', fontWeight: '700', width: '100%' },
  select: { minWidth: '190px', minHeight: '46px', border: '1px solid var(--border-color)', borderRadius: 'var(--radius-sm)', backgroundColor: 'var(--surface-color)', color: 'var(--text-main)', font: 'inherit', padding: '0 12px' },
  testButton: { minHeight: '46px', borderRadius: 'var(--radius-full)', backgroundColor: 'var(--primary-green)', color: 'var(--text-white)', display: 'inline-flex', alignItems: 'center', gap: '8px', fontWeight: '700', padding: '0 18px', opacity: 1 },
  currentLanguage: { color: 'var(--text-muted)', fontSize: '0.92rem', marginTop: '16px' },
  message: { color: 'var(--text-muted)', fontSize: '0.86rem', marginTop: '8px' },
};
