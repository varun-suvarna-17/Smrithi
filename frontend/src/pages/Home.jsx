import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Gamepad2, Mic, Eye, CheckCircle2, Clock, Music, Flower2, Heart, PlusCircle, ArrowRight, X } from 'lucide-react';
import { patientAPI, reminderAPI, progressAPI } from '../utils/api';

export default function Home() {
  const navigate = useNavigate();
  const [patient, setPatient] = useState(null);
  const [reminders, setReminders] = useState([]);
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [journeyCompleted, setJourneyCompleted] = useState(2);
  const [medicineTaken, setMedicineTaken] = useState(false);
  const [hydrationGlasses, setHydrationGlasses] = useState(6);
  const [activeLightbox, setActiveLightbox] = useState(null);
  const [showTalkModal, setShowTalkModal] = useState(false);
  const [talkTranscript, setTalkTranscript] = useState("Hi Asha, how are you feeling today? I am here to listen.");

  // Fetch data from backend
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        // Get patient profile
        const patientResponse = await patientAPI.getAll();
        if (patientResponse.data && patientResponse.data.length > 0) {
          const pat = patientResponse.data[0];
          setPatient(pat);
          
          // Get reminders
          const remindersResponse = await reminderAPI.getReminders(pat.id);
          setReminders(remindersResponse.data || []);
          
          // Get progress
          const progressResponse = await progressAPI.getProgress(pat.id);
          setProgress(progressResponse.data);
        }
      } catch (err) {
        console.error('Error fetching data:', err);
        setError(err.message);
        // Use dummy data if API fails
        setJourneyCompleted(2);
        setHydrationGlasses(6);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const memoriesList = [
    {
      id: 1,
      title: "Family",
      url: "https://images.unsplash.com/photo-1581579438747-1dc8d1e0ca96?auto=format&fit=crop&q=80&w=800",
      desc: "Our gathering last winter. Everyone was laughing so much!"
    },
    {
      id: 2,
      title: "Friends",
      url: "https://images.unsplash.com/photo-1516841273335-e39b37888115?auto=format&fit=crop&q=80&w=800",
      desc: "Sitting in the park on a sunny Tuesday afternoon."
    },
    {
      id: 3,
      title: "Meadow Stroll",
      url: "https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&q=80&w=800",
      desc: "Picking wild yellow flowers at sunset."
    },
    {
      id: 4,
      title: "Goldie",
      url: "https://images.unsplash.com/photo-1552053831-71594a27632d?auto=format&fit=crop&q=80&w=800",
      desc: "Our loyal companion resting his warm chin in our hands."
    }
  ];

  const handleMarkMedicine = () => {
    if (!medicineTaken) {
      setMedicineTaken(true);
      setJourneyCompleted(prev => Math.min(prev + 1, 4));
    }
  };

  const handleAddGlass = () => {
    if (hydrationGlasses < 8) {
      setHydrationGlasses(prev => prev + 1);
    }
  };

  return (
    <div style={styles.container}>
      {/* Top Welcome Title */}
      <div style={styles.header}>
        <h1 style={styles.greeting}>Good Morning, Asha</h1>
        <p style={styles.subtext}>It's a beautiful day. Let's start our journey together.</p>
      </div>

      {/* Top Widgets Row (Journey Widget & Reminder Widget) */}
      <div style={styles.widgetRow}>
        {/* Journey Widget */}
        <div style={styles.widgetCard}>
          <div style={styles.widgetLeft}>
            <div style={styles.widgetHeader}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--primary-green)" strokeWidth="2.5" style={{ marginRight: '6px' }}>
                <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 3.5 1 9.8a7 7 0 0 1-9 8.2Z" />
              </svg>
              <span style={styles.widgetTitle}>Today's Mind Journey</span>
            </div>
            <p style={styles.widgetDesc}>
              You've completed {journeyCompleted} out of 4 gentle activities today. Great progress!
            </p>
            <button style={styles.widgetBtn} onClick={() => navigate('/games')}>
              Continue Journey
            </button>
          </div>
          
          <div style={styles.radialWrapper}>
            <svg width="100" height="100" style={styles.radialSvg}>
              <circle cx="50" cy="50" r="40" stroke="#e0efe0" strokeWidth="10" fill="transparent" />
              <circle 
                cx="50" 
                cy="50" 
                r="40" 
                stroke="var(--primary-green)" 
                strokeWidth="10" 
                fill="transparent" 
                strokeDasharray="251.2" 
                strokeDashoffset={251.2 - (251.2 * (journeyCompleted / 4))}
                strokeLinecap="round"
                style={{ transition: 'stroke-dashoffset 0.5s ease' }}
              />
            </svg>
            <div style={styles.radialLabel}>{journeyCompleted}/4</div>
          </div>
        </div>

        {/* Reminder Widget */}
        <div style={styles.widgetCard}>
          <div style={{ flex: 1 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={styles.widgetHeader}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#a65e12" strokeWidth="2.5" style={{ marginRight: '6px' }}>
                  <path d="m10.5 20.5 19-12a4.95 4.95 0 1 0-7-7L3.5 13.5a4.95 4.95 0 1 0 7 7Z"/>
                  <path d="m8.5 8.5 7 7"/>
                </svg>
                <span style={{ ...styles.widgetTitle, color: '#a65e12' }}>Next Reminder</span>
              </div>
              <span style={styles.soonBadge}>Soon</span>
            </div>
            
            <div style={styles.medicineTime}>8:00 AM</div>
            <p style={styles.medicineName}>Morning Medicine</p>
            
            <button 
              style={medicineTaken ? styles.widgetBtnTaken : styles.widgetBtnAction}
              onClick={handleMarkMedicine}
              disabled={medicineTaken}
            >
              {medicineTaken ? "✓ Marked as Taken" : "✓ Mark as Taken"}
            </button>
          </div>
        </div>
      </div>

      {/* Main Big Callout Cards */}
      <div style={styles.calloutGrid}>
        <div style={{ ...styles.calloutCard, ...styles.calloutDark }} onClick={() => navigate('/games')}>
          <div style={styles.calloutIconCircle}>
            <Gamepad2 size={30} color="var(--primary-green)" />
          </div>
          <span style={styles.calloutText}>Play & Remember</span>
        </div>

        <div style={{ ...styles.calloutCard, ...styles.calloutLight }} onClick={() => setShowTalkModal(true)}>
          <div style={styles.calloutIconCircle}>
            <Mic size={30} color="var(--primary-green)" />
          </div>
          <span style={styles.calloutText}>Talk to Me</span>
        </div>
      </div>

      {/* Grid: My Memories & Today's Care */}
      <div style={styles.twoColumnGrid}>
        {/* Left Side: Memories Preview */}
        <div style={styles.cardContainer}>
          <div style={styles.cardHeaderRow}>
            <h2 style={styles.sectionHeader}>My Memories</h2>
            <button style={styles.viewAllBtn} onClick={() => navigate('/memories')}>
              View All
            </button>
          </div>
          
          <div style={styles.memoriesCarousel}>
            {memoriesList.map(mem => (
              <div key={mem.id} style={styles.memoryThumbCard} onClick={() => setActiveLightbox(mem)}>
                <img src={mem.url} alt={mem.title} style={styles.memoryThumbImg} />
                <div style={styles.memoryThumbOverlay}>{mem.title}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Right Side: Today's Care */}
        <div style={styles.cardContainer}>
          <h2 style={styles.sectionHeader}>Today's Care</h2>
          <div style={styles.careList}>
            {/* Morning Walk completed */}
            <div style={styles.careItem}>
              <div style={styles.careIconCompleted}>
                <CheckCircle2 size={24} color="var(--success-color)" />
              </div>
              <div style={styles.careDetails}>
                <div style={styles.careTitle}>Morning Walk</div>
                <div style={styles.careSub}>Completed at 7:30 AM</div>
              </div>
            </div>

            {/* Hydration check */}
            <div style={styles.careItem}>
              <div style={styles.careIconPending}>
                <Clock size={24} color="#a65e12" />
              </div>
              <div style={styles.careDetails}>
                <div style={styles.careTitle}>Hydration Check</div>
                <div style={styles.careSub}>
                  {8 - hydrationGlasses > 0 
                    ? `Pending - ${8 - hydrationGlasses} glasses left` 
                    : "Completed! Great job staying hydrated."}
                </div>
              </div>
              {hydrationGlasses < 8 && (
                <button style={styles.miniAddBtn} onClick={handleAddGlass} aria-label="Add glass of water">
                  <PlusCircle size={22} color="var(--primary-green)" />
                </button>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* SMRITHI Suggests Bottom Cards */}
      <div>
        <h2 style={{ ...styles.sectionHeader, marginBottom: '18px' }}>SMRITHI Suggests</h2>
        <div style={styles.suggestGrid}>
          <div style={styles.suggestCard}>
            <div style={styles.suggestIconBox}>
              <Music size={24} color="var(--primary-green)" />
            </div>
            <h3 style={styles.suggestTitle}>Listen to Classics</h3>
            <p style={styles.suggestDesc}>A calming playlist of your favorite 70s melodies.</p>
          </div>

          <div style={styles.suggestCard}>
            <div style={styles.suggestIconBox}>
              <Flower2 size={24} color="var(--primary-green)" />
            </div>
            <h3 style={styles.suggestTitle}>Garden Time</h3>
            <p style={styles.suggestDesc}>The weather is nice for a short walk outside.</p>
          </div>

          <div style={styles.suggestCard}>
            <div style={styles.suggestIconBox}>
              <Heart size={24} color="var(--primary-green)" />
            </div>
            <h3 style={styles.suggestTitle}>Deep Breathing</h3>
            <p style={styles.suggestDesc}>Take 5 minutes to relax and center yourself.</p>
          </div>
        </div>
      </div>

      {/* Lightbox Modal */}
      {activeLightbox && (
        <div style={styles.overlay} onClick={() => setActiveLightbox(null)}>
          <div style={styles.lightboxContent} onClick={e => e.stopPropagation()}>
            <button style={styles.closeBtn} onClick={() => setActiveLightbox(null)}>
              <X size={26} />
            </button>
            <img src={activeLightbox.url} alt={activeLightbox.title} style={styles.lightboxImg} />
            <h3 style={styles.lightboxTitle}>{activeLightbox.title}</h3>
            <p style={styles.lightboxDesc}>{activeLightbox.desc}</p>
          </div>
        </div>
      )}

      {/* Talk to Me Voice Assistant Modal */}
      {showTalkModal && (
        <div style={styles.overlay} onClick={() => setShowTalkModal(false)}>
          <div style={styles.talkModal} onClick={e => e.stopPropagation()}>
            <div style={styles.talkHeader}>
              <div style={styles.talkTitleRow}>
                <Mic size={24} color="var(--primary-green)" />
                <h3 style={{ fontSize: '1.25rem', fontWeight: '700' }}>Talk with SMRITHI</h3>
              </div>
              <button style={styles.closeBtn} onClick={() => setShowTalkModal(false)}>
                <X size={24} />
              </button>
            </div>
            
            <div style={styles.talkWaveform}>
              <div style={styles.waveBar}></div>
              <div style={{...styles.waveBar, height: '45px', animationDelay: '0.1s'}}></div>
              <div style={{...styles.waveBar, height: '60px', animationDelay: '0.2s'}}></div>
              <div style={{...styles.waveBar, height: '30px', animationDelay: '0.3s'}}></div>
              <div style={{...styles.waveBar, height: '50px', animationDelay: '0.4s'}}></div>
            </div>

            <div style={styles.talkBubble}>
              {talkTranscript}
            </div>

            <div style={styles.talkInputRow}>
              <button 
                style={styles.btnPrimary} 
                onClick={() => setTalkTranscript("I recorded your story about the garden! That's wonderful.")}
              >
                Tap to Speak / Reply
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    gap: '32px',
  },
  header: {
    marginBottom: '8px',
  },
  greeting: {
    fontSize: '2.2rem',
    fontWeight: '800',
    color: 'var(--text-main)',
  },
  subtext: {
    fontSize: '1.15rem',
    color: 'var(--text-muted)',
    fontWeight: '500',
  },
  widgetRow: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
    gap: '24px',
  },
  widgetCard: {
    backgroundColor: 'var(--surface-color)',
    border: '1px solid var(--border-color)',
    borderRadius: '24px',
    padding: '24px',
    boxShadow: 'var(--shadow-widget)',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: '16px',
    minHeight: '190px',
  },
  widgetLeft: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    height: '100%',
    gap: '10px',
  },
  widgetHeader: {
    display: 'flex',
    alignItems: 'center',
  },
  widgetTitle: {
    fontSize: '1rem',
    fontWeight: '700',
    color: 'var(--primary-green)',
  },
  widgetDesc: {
    fontSize: '0.95rem',
    color: 'var(--text-muted)',
    lineHeight: '1.4',
    fontWeight: '500',
  },
  widgetBtn: {
    alignSelf: 'flex-start',
    backgroundColor: 'var(--primary-green)',
    color: 'white',
    border: 'none',
    borderRadius: '50px',
    padding: '10px 20px',
    fontWeight: '700',
    fontSize: '0.9rem',
    marginTop: '6px',
  },
  radialWrapper: {
    position: 'relative',
    width: '100px',
    height: '100px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  radialSvg: {
    transform: 'rotate(-90deg)',
  },
  radialLabel: {
    position: 'absolute',
    fontSize: '1.25rem',
    fontWeight: '800',
    color: 'var(--primary-green)',
  },
  soonBadge: {
    backgroundColor: 'var(--warning-bg)',
    color: 'var(--warning-orange)',
    fontWeight: '700',
    fontSize: '0.8rem',
    padding: '4px 10px',
    borderRadius: '50px',
  },
  medicineTime: {
    fontSize: '2.1rem',
    fontWeight: '800',
    color: 'var(--text-main)',
    margin: '10px 0 2px 0',
  },
  medicineName: {
    fontSize: '1.05rem',
    fontWeight: '600',
    color: 'var(--text-muted)',
    marginBottom: '14px',
  },
  widgetBtnAction: {
    width: '100%',
    backgroundColor: 'var(--secondary-green)',
    color: 'var(--primary-green)',
    border: 'none',
    borderRadius: '50px',
    padding: '12px',
    fontWeight: '700',
    fontSize: '1rem',
  },
  widgetBtnTaken: {
    width: '100%',
    backgroundColor: '#e2ede4',
    color: '#4a6652',
    border: 'none',
    borderRadius: '50px',
    padding: '12px',
    fontWeight: '700',
    fontSize: '1rem',
    cursor: 'not-allowed',
  },
  calloutGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
    gap: '24px',
  },
  calloutCard: {
    borderRadius: '24px',
    padding: '28px 24px',
    display: 'flex',
    alignItems: 'center',
    gap: '20px',
    cursor: 'pointer',
    boxShadow: 'var(--shadow-card)',
  },
  calloutDark: {
    backgroundColor: 'var(--primary-green)',
    color: 'white',
  },
  calloutLight: {
    backgroundColor: 'var(--secondary-green)',
    color: 'var(--primary-green)',
    border: '1px solid var(--border-color)',
  },
  calloutIconCircle: {
    width: '56px',
    height: '56px',
    borderRadius: '50%',
    backgroundColor: 'white',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    boxShadow: '0 4px 10px rgba(0, 0, 0, 0.05)',
  },
  calloutText: {
    fontSize: '1.45rem',
    fontWeight: '800',
  },
  twoColumnGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
    gap: '24px',
  },
  cardContainer: {
    backgroundColor: 'white',
    border: '1px solid var(--border-color)',
    borderRadius: '24px',
    padding: '24px',
    boxShadow: 'var(--shadow-card)',
  },
  cardHeaderRow: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '16px',
  },
  sectionHeader: {
    fontSize: '1.4rem',
    fontWeight: '700',
    color: 'var(--text-main)',
  },
  viewAllBtn: {
    fontSize: '0.95rem',
    fontWeight: '700',
    color: 'var(--primary-green)',
  },
  memoriesCarousel: {
    display: 'grid',
    gridTemplateColumns: 'repeat(4, 1fr)',
    gap: '12px',
  },
  memoryThumbCard: {
    position: 'relative',
    height: '110px',
    borderRadius: '16px',
    overflow: 'hidden',
    cursor: 'pointer',
    boxShadow: 'var(--shadow-subtle)',
  },
  memoryThumbImg: {
    width: '100%',
    height: '100%',
    objectFit: 'cover',
    transition: 'transform 0.3s ease',
  },
  memoryThumbOverlay: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    background: 'linear-gradient(to top, rgba(0,0,0,0.6), transparent)',
    color: 'white',
    padding: '8px 4px',
    fontSize: '0.85rem',
    fontWeight: '700',
    textAlign: 'center',
  },
  careList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
  },
  careItem: {
    display: 'flex',
    alignItems: 'center',
    backgroundColor: '#f6fbf7',
    border: '1px solid #e0efe2',
    borderRadius: '18px',
    padding: '16px 20px',
    gap: '16px',
  },
  careIconCompleted: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  careIconPending: {
    width: '24px',
    height: '24px',
    borderRadius: '50%',
    backgroundColor: 'var(--warning-bg)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  careDetails: {
    flex: 1,
  },
  careTitle: {
    fontSize: '1.05rem',
    fontWeight: '700',
    color: 'var(--text-main)',
  },
  careSub: {
    fontSize: '0.88rem',
    color: 'var(--text-muted)',
    fontWeight: '500',
    marginTop: '2px',
  },
  miniAddBtn: {
    padding: '4px',
  },
  suggestGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: '20px',
  },
  suggestCard: {
    backgroundColor: 'var(--sidebar-bg)',
    border: '1px solid var(--border-color)',
    borderRadius: '20px',
    padding: '24px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-start',
    gap: '10px',
  },
  suggestIconBox: {
    width: '44px',
    height: '44px',
    borderRadius: '12px',
    backgroundColor: '#d4ebd8',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  suggestTitle: {
    fontSize: '1.15rem',
    fontWeight: '700',
    color: 'var(--text-main)',
  },
  suggestDesc: {
    fontSize: '0.95rem',
    color: 'var(--text-muted)',
    lineHeight: '1.4',
    fontWeight: '500',
  },
  overlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(20, 36, 24, 0.4)',
    backdropFilter: 'blur(4px)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 9999,
  },
  lightboxContent: {
    backgroundColor: 'white',
    borderRadius: '24px',
    padding: '32px',
    maxWidth: '560px',
    width: '90%',
    position: 'relative',
    boxShadow: '0 20px 40px rgba(0,0,0,0.15)',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '16px',
  },
  lightboxImg: {
    width: '100%',
    height: '260px',
    borderRadius: '16px',
    objectFit: 'cover',
  },
  lightboxTitle: {
    fontSize: '1.5rem',
    fontWeight: '700',
    color: 'var(--text-main)',
    width: '100%',
    textAlign: 'left',
  },
  lightboxDesc: {
    fontSize: '1.05rem',
    color: 'var(--text-muted)',
    lineHeight: '1.5',
    width: '100%',
    textAlign: 'left',
  },
  closeBtn: {
    position: 'absolute',
    top: '20px',
    right: '20px',
    color: 'var(--text-muted)',
    padding: '4px',
  },
  talkModal: {
    backgroundColor: 'white',
    borderRadius: '24px',
    padding: '28px',
    maxWidth: '440px',
    width: '90%',
    position: 'relative',
    display: 'flex',
    flexDirection: 'column',
    gap: '24px',
  },
  talkHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  talkTitleRow: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
  },
  talkWaveform: {
    height: '80px',
    backgroundColor: 'var(--sidebar-bg)',
    borderRadius: '16px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '8px',
  },
  waveBar: {
    width: '6px',
    height: '20px',
    borderRadius: '3px',
    backgroundColor: 'var(--primary-green)',
    animation: 'wave 1.2s infinite ease-in-out',
  },
  talkBubble: {
    backgroundColor: 'var(--secondary-green)',
    padding: '16px',
    borderRadius: '18px 18px 18px 4px',
    color: 'var(--primary-green)',
    fontSize: '1.05rem',
    fontWeight: '600',
    lineHeight: '1.45',
  },
  talkInputRow: {
    display: 'flex',
    justifyContent: 'center',
  },
  btnPrimary: {
    backgroundColor: 'var(--primary-green)',
    color: 'white',
    border: 'none',
    borderRadius: '50px',
    padding: '14px 28px',
    fontWeight: '700',
    fontSize: '1.05rem',
  }
};
