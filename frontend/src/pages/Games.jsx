import React, { useState, useEffect } from 'react';
import { Heart, Play, UtensilsCrossed, Music, Grid3X3, ShoppingBag, ArrowLeft, Lightbulb, CheckCircle2, RefreshCw, Volume2, Sparkles, AlertCircle } from 'lucide-react';
import { soundFx } from '../utils/audio';
import { gameAPI } from '../utils/api';

export default function Games() {
  const [activeGame, setActiveGame] = useState(null);
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch available games from backend
  useEffect(() => {
    const fetchGames = async () => {
      try {
        setLoading(true);
        const response = await gameAPI.getAvailableGames();
        setGames(response.data || []);
      } catch (err) {
        console.error('Error fetching games:', err);
        setError(err.message);
        // Use default games if backend fails
        setGames([
          {
            id: 'family_portrait',
            title: 'Family Portrait',
            description: 'Recognize family members in photos',
            icon: 'Heart',
            difficulty: 'Easy',
            color: 'var(--primary-color)'
          },
          {
            id: 'kitchen_memories',
            title: 'Kitchen Memories',
            description: 'Remember cooking ingredients and recipes',
            icon: 'UtensilsCrossed',
            difficulty: 'Medium',
            color: '#8d6e63'
          },
          {
            id: 'rhythm_match',
            title: 'Rhythm Match',
            description: 'Follow musical patterns and sequences',
            icon: 'Music',
            difficulty: 'Medium',
            color: '#e91e63'
          },
          {
            id: 'folk_motif',
            title: 'Folk Motif',
            description: 'Match traditional patterns and designs',
            icon: 'Grid3X3',
            difficulty: 'Hard',
            color: '#ff9800'
          },
          {
            id: 'weekly_bazaar',
            title: 'Weekly Bazaar',
            description: 'Shop and recall products you\'ve seen before',
            icon: 'ShoppingBag',
            difficulty: 'Medium',
            color: '#4caf50'
          }
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchGames();
  }, []);

  if (activeGame === 'family_portrait') {
    return <FamilyPortraitGame onBack={() => setActiveGame(null)} />;
  }
  if (activeGame === 'kitchen_memories') {
    return <KitchenMemoriesGame onBack={() => setActiveGame(null)} />;
  }
  if (activeGame === 'rhythm_match') {
    return <RhythmMatchGame onBack={() => setActiveGame(null)} />;
  }
  if (activeGame === 'folk_motif') {
    return <FolkMotifGame onBack={() => setActiveGame(null)} />;
  }
  if (activeGame === 'weekly_bazaar') {
    return <WeeklyBazaarGame onBack={() => setActiveGame(null)} />;
  }

  return (
    <div style={styles.container}>
      {/* Page Header */}
      <header style={styles.header}>
        <h1 style={styles.pageTitle}>Play & Remember</h1>
        <p style={styles.subtitle}>
          Take a gentle journey through familiar memories and activities.
        </p>
      </header>

      {/* Grid of 5 games matching the new screenshot */}
      <div style={styles.playGrid}>
        {/* Game 1: Memory Match */}
        <div style={styles.playCard}>
          <div style={styles.iconCircleBig}>
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="var(--primary-green)" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
              <rect width="10" height="14" x="3" y="3" rx="2" />
              <rect width="10" height="14" x="11" y="7" rx="2" />
            </svg>
          </div>
          <h2 style={styles.cardHeaderTitle}>Memory Match</h2>
          <p style={styles.cardHeaderDesc}>Remember, find and match.</p>
          <button 
            className="btn-primary" 
            style={styles.cardStartBtn}
            onClick={() => {
              soundFx.playSoftTap();
              setActiveGame('weekly_bazaar'); // Bazaar is memorizing and matching items
            }}
          >
            Start <span style={{ marginLeft: '6px' }}>→</span>
          </button>
        </div>

        {/* Game 2: Recognition */}
        <div style={styles.playCard}>
          <div style={styles.iconCircleBig}>
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="var(--primary-green)" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10" />
              <path d="M8 14s1.5 2 4 2 4-2 4-2" />
              <line x1="9" x2="9.01" y1="9" y2="9" />
              <line x1="15" x2="15.01" y1="9" y2="9" />
            </svg>
          </div>
          <h2 style={styles.cardHeaderTitle}>Recognition</h2>
          <p style={styles.cardHeaderDesc}>Recognize familiar people and places.</p>
          <button 
            className="btn-primary" 
            style={styles.cardStartBtn}
            onClick={() => {
              soundFx.playSoftTap();
              setActiveGame('family_portrait');
            }}
          >
            Start <span style={{ marginLeft: '6px' }}>→</span>
          </button>
        </div>

        {/* Game 3: Sequence Recall */}
        <div style={styles.playCard}>
          <div style={styles.iconCircleBig}>
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="var(--primary-green)" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
              <path d="m17 2 4 4-4 4" />
              <path d="M3 11v-1a4 4 0 0 1 4-4h14" />
              <path d="m7 22-4-4 4-4" />
              <path d="M21 13v1a4 4 0 0 1-4 4H3" />
            </svg>
          </div>
          <h2 style={styles.cardHeaderTitle}>Sequence Recall</h2>
          <p style={styles.cardHeaderDesc}>Watch, remember and repeat.</p>
          <button 
            className="btn-primary" 
            style={styles.cardStartBtn}
            onClick={() => {
              soundFx.playSoftTap();
              setActiveGame('rhythm_match');
            }}
          >
            Start <span style={{ marginLeft: '6px' }}>→</span>
          </button>
        </div>

        {/* Game 4: Folk Motif */}
        <div style={styles.playCard}>
          <div style={styles.iconCircleBig}>
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="var(--primary-green)" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
              <rect width="18" height="18" x="3" y="3" rx="2" />
              <path d="M3 9h18" />
              <path d="M3 15h18" />
              <path d="M9 3v18" />
              <path d="M15 3v18" />
            </svg>
          </div>
          <h2 style={styles.cardHeaderTitle}>Folk Motif</h2>
          <p style={styles.cardHeaderDesc}>Complete a beautiful traditional pattern.</p>
          <button 
            className="btn-primary" 
            style={styles.cardStartBtn}
            onClick={() => {
              soundFx.playSoftTap();
              setActiveGame('folk_motif');
            }}
          >
            Start <span style={{ marginLeft: '6px' }}>→</span>
          </button>
        </div>

        {/* Game 5: Regional Kitchen */}
        <div style={styles.playCard}>
          <div style={styles.iconCircleBig}>
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="var(--primary-green)" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 2v9" />
              <path d="M4 11h16a2 2 0 0 1 2 2v2a6 6 0 0 1-6 6H8a6 6 0 0 1-6-6v-2a2 2 0 0 1 2-2Z" />
              <path d="M8 7V3" />
              <path d="M16 7V3" />
            </svg>
          </div>
          <h2 style={styles.cardHeaderTitle}>Regional Kitchen</h2>
          <p style={styles.cardHeaderDesc}>Remember the order and prepare the dish.</p>
          <button 
            className="btn-primary" 
            style={styles.cardStartBtn}
            onClick={() => {
              soundFx.playSoftTap();
              setActiveGame('kitchen_memories');
            }}
          >
            Start <span style={{ marginLeft: '6px' }}>→</span>
          </button>
        </div>
      </div>
    </div>
  );
}

/* We preserve all inner helper components and override outer classes inside css/inline styles */


/* ========================================================================== */
/* GAME 1: FAMILY PORTRAIT INTERACTIVE COMPONENT                             */
/* ========================================================================== */
function FamilyPortraitGame({ onBack }) {
  const [showHint, setShowHint] = useState(false);
  const [completed, setCompleted] = useState(false);
  const [currentPromptIndex, setCurrentPromptIndex] = useState(0);

  const prompts = [
    { name: 'Priya', role: 'your daughter', hint: 'Priya is standing on the right wearing the dark woven Mekhela Chador.' },
    { name: 'Biren', role: 'your husband', hint: 'Biren is sitting in the center with a warm smile.' },
    { name: 'Mina', role: 'your sister', hint: 'Mina is sitting on the left with a traditional Mekhela Chador.' }
  ];

  const currentPrompt = prompts[currentPromptIndex];

  const handleTapTarget = () => {
    soundFx.playSuccess();
    setCompleted(true);
  };

  const handleNext = () => {
    soundFx.playSoftTap();
    setCompleted(false);
    setShowHint(false);
    setCurrentPromptIndex((prev) => (prev + 1) % prompts.length);
  };

  return (
    <div style={gameStyles.gameContainer}>
      <div style={gameStyles.topBar}>
        <button onClick={onBack} style={gameStyles.backBtn} aria-label="Go back to games list">
          <ArrowLeft size={24} /> <span style={{ marginLeft: '8px', fontWeight: '600' }}>Back</span>
        </button>
      </div>

      <div style={gameStyles.headerSection}>
        <h1 style={gameStyles.gameTitle}>Family Portrait</h1>
        <p style={gameStyles.gameSubtitle}>Who is {currentPrompt.name}?</p>
      </div>

      <div style={gameStyles.cardBox}>
        <div style={gameStyles.imageContainer}>
          <img 
            src="/images/family_portrait.png" 
            alt="Family in tea garden" 
            style={gameStyles.mainPhoto} 
          />

          {/* Dotted highlight ring around Priya (as depicted in design mockup Image 2) */}
          <div 
            style={{
              ...gameStyles.targetOverlay,
              border: completed ? '4px solid #2e7d32' : '3px dashed rgba(255, 255, 255, 0.9)',
              backgroundColor: completed ? 'rgba(46, 125, 50, 0.15)' : 'rgba(255, 255, 255, 0.1)',
            }}
            onClick={handleTapTarget}
          >
            {!completed && (
              <div style={gameStyles.tapBadge}>
                Tap on {currentPrompt.name} 👆
              </div>
            )}
          </div>
        </div>

        {/* Feedback message when completed */}
        {completed ? (
          <div style={gameStyles.successBox}>
            <CheckCircle2 size={36} color="#175e24" />
            <div>
              <h3 style={{ fontSize: '1.25rem', color: '#175e24', fontWeight: '700' }}>
                Wonderful! That is {currentPrompt.name}!
              </h3>
              <p style={{ fontSize: '1.05rem', color: '#4a5c50', marginTop: '4px' }}>
                {currentPrompt.name} is {currentPrompt.role}. She loves visiting you and sharing sweet stories.
              </p>
            </div>
            <button style={gameStyles.nextBtn} onClick={handleNext}>
              Next Photo →
            </button>
          </div>
        ) : (
          <div style={{ marginTop: '20px', textAlign: 'center' }}>
            <button 
              style={gameStyles.hintBtn} 
              onClick={() => setShowHint(!showHint)}
              aria-label="Show hint"
            >
              <Lightbulb size={20} color="#175e24" style={{ marginRight: '8px' }} />
              Hint
            </button>

            {showHint && (
              <div style={gameStyles.hintCard}>
                💡 {currentPrompt.hint}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

/* ========================================================================== */
/* GAME 2: KITCHEN MEMORIES INTERACTIVE COMPONENT                             */
/* ========================================================================== */
function KitchenMemoriesGame({ onBack }) {
  const stepsTarget = [
    { id: 'kolakhar', name: 'Kolakhar Water', desc: 'Banana ash alkali extract' },
    { id: 'papaya', name: 'Raw Papaya', desc: 'Grated green omita' },
    { id: 'panchphoran', name: 'Mustard Oil & Panch Phoran', desc: 'Sizzled spices' },
    { id: 'coriander', name: 'Fresh Coriander', desc: 'Aromatic green garnish' },
  ];

  const [selectedSteps, setSelectedSteps] = useState([]);
  const [dishCompleted, setDishCompleted] = useState(false);

  const availableIngredients = [
    { id: 'kolakhar', name: 'Filtered Kolakhar Water', icon: '🍶' },
    { id: 'papaya', name: 'Grated Raw Papaya', icon: '🍈' },
    { id: 'panchphoran', name: 'Mustard Oil & Panch Phoran', icon: '🫒' },
    { id: 'coriander', name: 'Fresh Coriander', icon: '🌿' },
  ];

  const handleSelect = (item) => {
    if (selectedSteps.find((s) => s.id === item.id)) return;
    soundFx.playSoftTap();
    const updated = [...selectedSteps, item];
    setSelectedSteps(updated);

    if (updated.length === 4) {
      soundFx.playSuccess();
      setDishCompleted(true);
    }
  };

  const handleReset = () => {
    soundFx.playSoftTap();
    setSelectedSteps([]);
    setDishCompleted(false);
  };

  return (
    <div style={gameStyles.gameContainer}>
      <div style={gameStyles.topBar}>
        <button onClick={onBack} style={gameStyles.backBtn}>
          <ArrowLeft size={24} /> <span style={{ marginLeft: '8px', fontWeight: '600' }}>Back</span>
        </button>
      </div>

      <div style={gameStyles.headerSection}>
        <h1 style={gameStyles.gameTitle}>Kitchen Memories</h1>
        <p style={gameStyles.gameSubtitle}>
          Put the ingredients in order to make comforting <strong>Assamese Khar</strong>.
        </p>
      </div>

      <div style={gameStyles.cardBox}>
        <div style={{ textAlign: 'center', marginBottom: '24px' }}>
          <img 
            src="/images/kitchen_memories.png" 
            alt="Assamese Khar dish in brass bowl" 
            style={{ width: '100%', maxHeight: '240px', objectFit: 'cover', borderRadius: '16px' }}
          />
        </div>

        {/* Selected steps progress slots */}
        <div style={kitchenStyles.slotContainer}>
          {stepsTarget.map((target, idx) => {
            const selected = selectedSteps[idx];
            return (
              <div key={target.id} style={kitchenStyles.slotCard}>
                <div style={kitchenStyles.slotNum}>Step {idx + 1}</div>
                <div style={kitchenStyles.slotContent}>
                  {selected ? (
                    <span style={{ fontWeight: '700', color: '#175e24' }}>
                      {selected.icon} {selected.name}
                    </span>
                  ) : (
                    <span style={{ color: '#8aa090', fontStyle: 'italic' }}>Tap ingredient below</span>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {dishCompleted ? (
          <div style={gameStyles.successBox}>
            <CheckCircle2 size={36} color="#175e24" />
            <div>
              <h3 style={{ fontSize: '1.25rem', color: '#175e24', fontWeight: '700' }}>
                Wonderful! Your Assamese Khar is ready!
              </h3>
              <p style={{ fontSize: '1.05rem', color: '#4a5c50', marginTop: '4px' }}>
                It smells delightful and brings warm memories of cozy family meals around the kitchen table.
              </p>
            </div>
            <button style={gameStyles.nextBtn} onClick={handleReset}>
              <RefreshCw size={20} style={{ marginRight: '8px' }} /> Prepare Dish Again
            </button>
          </div>
        ) : (
          <div>
            <h3 style={{ fontSize: '1.15rem', color: '#1c2b20', marginBottom: '16px', textAlign: 'center' }}>
              Tap ingredients to add to cooking pot:
            </h3>
            <div style={kitchenStyles.ingGrid}>
              {availableIngredients.map((item) => {
                const isUsed = selectedSteps.some((s) => s.id === item.id);
                return (
                  <button
                    key={item.id}
                    disabled={isUsed}
                    onClick={() => handleSelect(item)}
                    style={{
                      ...kitchenStyles.ingCard,
                      opacity: isUsed ? 0.4 : 1,
                      border: isUsed ? '2px solid #ccc' : '2px solid #d4e8d6',
                    }}
                  >
                    <span style={{ fontSize: '2rem' }}>{item.icon}</span>
                    <span style={{ fontSize: '1.05rem', fontWeight: '600', color: '#175e24' }}>
                      {item.name}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

/* ========================================================================== */
/* GAME 3: RHYTM MATCH INTERACTIVE COMPONENT                                  */
/* ========================================================================== */
function RhythmMatchGame({ onBack }) {
  const [userTaps, setUserTaps] = useState(0);
  const [isPlayingDemo, setIsPlayingDemo] = useState(false);
  const [completed, setCompleted] = useState(false);

  const targetBeats = 3;

  const playBihuPattern = () => {
    setIsPlayingDemo(true);
    setUserTaps(0);
    setCompleted(false);

    // Play 3 rhythm beats with delay
    soundFx.playDrumBeat(1.0);
    setTimeout(() => soundFx.playDrumBeat(1.2), 350);
    setTimeout(() => soundFx.playDrumBeat(1.0), 700);

    setTimeout(() => {
      setIsPlayingDemo(false);
    }, 1000);
  };

  const handleDrumTap = () => {
    if (completed) return;
    soundFx.playDrumBeat(1.1);
    const nextCount = userTaps + 1;
    setUserTaps(nextCount);

    if (nextCount === targetBeats) {
      setTimeout(() => {
        soundFx.playSuccess();
        setCompleted(true);
      }, 300);
    }
  };

  return (
    <div style={gameStyles.gameContainer}>
      <div style={gameStyles.topBar}>
        <button onClick={onBack} style={gameStyles.backBtn}>
          <ArrowLeft size={24} /> <span style={{ marginLeft: '8px', fontWeight: '600' }}>Back</span>
        </button>
      </div>

      <div style={gameStyles.headerSection}>
        <h1 style={gameStyles.gameTitle}>Rhythm Match</h1>
        <p style={gameStyles.gameSubtitle}>
          Listen carefully and tap the rhythm of traditional Bihu drum beats.
        </p>
      </div>

      <div style={gameStyles.cardBox}>
        <div style={{ textAlign: 'center', marginBottom: '24px' }}>
          <button 
            style={rhythmStyles.listenBtn}
            onClick={playBihuPattern}
            disabled={isPlayingDemo}
          >
            <Volume2 size={24} style={{ marginRight: '8px' }} />
            {isPlayingDemo ? 'Listening to Bihu Rhythm...' : 'Tap to Listen to Beat ♪'}
          </button>
        </div>

        {/* Big Interactive Dhol Drum Pad */}
        <div 
          onClick={handleDrumTap}
          style={rhythmStyles.drumPad}
        >
          <img 
            src="/images/rhythm_match.png" 
            alt="Traditional Bihu Dhol Drum" 
            style={rhythmStyles.drumImg}
          />
          <div style={rhythmStyles.drumOverlay}>
            <span style={{ fontSize: '3rem', marginBottom: '8px' }}>🥁</span>
            <span style={{ fontSize: '1.25rem', fontWeight: '700', color: '#ffffff', textShadow: '0 2px 4px rgba(0,0,0,0.6)' }}>
              Tap Bihu Drum ({userTaps} / {targetBeats})
            </span>
          </div>
        </div>

        {completed ? (
          <div style={{ ...gameStyles.successBox, marginTop: '24px' }}>
            <CheckCircle2 size={36} color="#175e24" />
            <div>
              <h3 style={{ fontSize: '1.25rem', color: '#175e24', fontWeight: '700' }}>
                Joyful rhythm! You matched the Bihu drum beat!
              </h3>
              <p style={{ fontSize: '1.05rem', color: '#4a5c50', marginTop: '4px' }}>
                Your sense of music and traditional beats is wonderful.
              </p>
            </div>
            <button style={gameStyles.nextBtn} onClick={playBihuPattern}>
              Play Another Rhythm ♪
            </button>
          </div>
        ) : (
          <div style={{ textAlign: 'center', marginTop: '20px', color: '#4a5c50', fontSize: '1.05rem' }}>
            Tap the drum 3 times to match the Bihu rhythm!
          </div>
        )}
      </div>
    </div>
  );
}

/* ========================================================================== */
/* GAME 4: FOLK MOTIF WEAVER INTERACTIVE COMPONENT                             */
/* ========================================================================== */
function FolkMotifGame({ onBack }) {
  const [selectedMotif, setSelectedMotif] = useState(null);
  const [isCorrect, setIsCorrect] = useState(false);

  const options = [
    { id: 'rhino', name: 'Kaziranga Rhino', icon: '🦏', desc: 'Symbol of strength & heritage', correct: true },
    { id: 'lotus', name: 'Lotus Flower', icon: '🪷', desc: 'Traditional floral weave', correct: false },
    { id: 'bamboo', name: 'Bamboo Basket', icon: '🧺', desc: 'Geometric lattice weave', correct: false },
  ];

  const handleSelectMotif = (opt) => {
    setSelectedMotif(opt.id);
    if (opt.correct) {
      soundFx.playSuccess();
      setIsCorrect(true);
    } else {
      soundFx.playSoftTap();
      setIsCorrect(false);
    }
  };

  const handleReset = () => {
    soundFx.playSoftTap();
    setSelectedMotif(null);
    setIsCorrect(false);
  };

  return (
    <div style={gameStyles.gameContainer}>
      <div style={gameStyles.topBar}>
        <button onClick={onBack} style={gameStyles.backBtn}>
          <ArrowLeft size={24} /> <span style={{ marginLeft: '8px', fontWeight: '600' }}>Back</span>
        </button>
      </div>

      <div style={gameStyles.headerSection}>
        <h1 style={gameStyles.gameTitle}>Folk Motif Weaver</h1>
        <p style={gameStyles.gameSubtitle}>
          Find the regional textile pattern that comes next to complete the silk Mekhela Chador.
        </p>
      </div>

      <div style={gameStyles.cardBox}>
        <div style={{ textAlign: 'center', marginBottom: '24px' }}>
          <img 
            src="/images/folk_motif.png" 
            alt="Assamese Mekhela Chador woven motif" 
            style={{ width: '100%', maxHeight: '200px', objectFit: 'cover', borderRadius: '16px' }}
          />
        </div>

        {/* Pattern Strip */}
        <div style={motifStyles.stripContainer}>
          <div style={motifStyles.patternCell}>🦏 Rhino</div>
          <div style={motifStyles.arrow}>→</div>
          <div style={motifStyles.patternCell}>🦚 Peacock</div>
          <div style={motifStyles.arrow}>→</div>
          <div style={motifStyles.patternCell}>
            {isCorrect ? '🦏 Rhino' : '?'}
          </div>
        </div>

        {isCorrect ? (
          <div style={gameStyles.successBox}>
            <CheckCircle2 size={36} color="#175e24" />
            <div>
              <h3 style={{ fontSize: '1.25rem', color: '#175e24', fontWeight: '700' }}>
                Beautiful Weave!
              </h3>
              <p style={{ fontSize: '1.05rem', color: '#4a5c50', marginTop: '4px' }}>
                You completed the traditional Kaziranga Rhino motif pattern gracefully.
              </p>
            </div>
            <button style={gameStyles.nextBtn} onClick={handleReset}>
              Weave Next Pattern 🌸
            </button>
          </div>
        ) : (
          <div>
            <h3 style={{ fontSize: '1.15rem', color: '#1c2b20', marginBottom: '16px', textAlign: 'center' }}>
              Which motif comes next in the row?
            </h3>
            <div style={motifStyles.optionsGrid}>
              {options.map((opt) => (
                <button
                  key={opt.id}
                  onClick={() => handleSelectMotif(opt)}
                  style={motifStyles.optionCard}
                >
                  <span style={{ fontSize: '2.5rem', marginBottom: '8px' }}>{opt.icon}</span>
                  <span style={{ fontSize: '1.1rem', fontWeight: '700', color: '#175e24' }}>
                    {opt.name}
                  </span>
                  <span style={{ fontSize: '0.9rem', color: '#4a5c50', marginTop: '4px' }}>
                    {opt.desc}
                  </span>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

/* ========================================================================== */
/* GAME 5: WEEKLY BAZAAR INTERACTIVE COMPONENT                               */
/* ========================================================================== */
function WeeklyBazaarGame({ onBack }) {
  const [phase, setPhase] = useState('memorize'); // 'memorize' | 'select' | 'done'
  const [selectedItems, setSelectedItems] = useState([]);

  const targetItems = [
    { id: 'tea', name: 'Assam Tea Leaves', icon: '🍃' },
    { id: 'bamboo', name: 'Tender Bamboo Shoots', icon: '🎍' },
    { id: 'ginger', name: 'Fresh Ginger Root', icon: '🫚' },
  ];

  const allMarketItems = [
    { id: 'tea', name: 'Assam Tea Leaves', icon: '🍃' },
    { id: 'bamboo', name: 'Tender Bamboo Shoots', icon: '🎍' },
    { id: 'ginger', name: 'Fresh Ginger Root', icon: '🫚' },
    { id: 'pineapple', name: 'Local Assam Pineapple', icon: '🍍' },
    { id: 'chilli', name: 'Bhut Jolokia Chilli', icon: '🌶️' },
  ];

  const handleStartShopping = () => {
    soundFx.playSoftTap();
    setPhase('select');
  };

  const handleSelectItem = (item) => {
    soundFx.playSoftTap();
    const isSelected = selectedItems.find((i) => i.id === item.id);
    let updated;
    if (isSelected) {
      updated = selectedItems.filter((i) => i.id !== item.id);
    } else {
      updated = [...selectedItems, item];
    }
    setSelectedItems(updated);

    // Check if user selected all 3 target items
    if (updated.length === 3) {
      const matchAll = targetItems.every((t) => updated.some((u) => u.id === t.id));
      if (matchAll) {
        soundFx.playSuccess();
        setPhase('done');
      }
    }
  };

  const handleRestart = () => {
    soundFx.playSoftTap();
    setSelectedItems([]);
    setPhase('memorize');
  };

  return (
    <div style={gameStyles.gameContainer}>
      <div style={gameStyles.topBar}>
        <button onClick={onBack} style={gameStyles.backBtn}>
          <ArrowLeft size={24} /> <span style={{ marginLeft: '8px', fontWeight: '600' }}>Back</span>
        </button>
      </div>

      <div style={gameStyles.headerSection}>
        <h1 style={gameStyles.gameTitle}>Weekly Bazaar</h1>
        <p style={gameStyles.gameSubtitle}>
          Remember what we need from the local market to prepare for the week.
        </p>
      </div>

      <div style={gameStyles.cardBox}>
        <div style={{ textAlign: 'center', marginBottom: '20px' }}>
          <img 
            src="/images/weekly_bazaar.png" 
            alt="Handwoven basket with fresh local market items" 
            style={{ width: '100%', maxHeight: '200px', objectFit: 'cover', borderRadius: '16px' }}
          />
        </div>

        {phase === 'memorize' && (
          <div style={{ textAlign: 'center' }}>
            <h3 style={{ fontSize: '1.2rem', color: '#175e24', fontWeight: '700', marginBottom: '16px' }}>
              🧺 Shopping List for Sunday Haat:
            </h3>
            <div style={bazaarStyles.itemList}>
              {targetItems.map((item) => (
                <div key={item.id} style={bazaarStyles.itemPill}>
                  <span style={{ fontSize: '1.8rem' }}>{item.icon}</span>
                  <span style={{ fontSize: '1.1rem', fontWeight: '600', color: '#175e24' }}>{item.name}</span>
                </div>
              ))}
            </div>
            <button style={gameStyles.nextBtn} onClick={handleStartShopping}>
              I'm Ready to Shop 🛒
            </button>
          </div>
        )}

        {phase === 'select' && (
          <div>
            <h3 style={{ fontSize: '1.15rem', color: '#1c2b20', marginBottom: '16px', textAlign: 'center' }}>
              Which 3 items were on our shopping list?
            </h3>
            <div style={bazaarStyles.grid}>
              {allMarketItems.map((item) => {
                const isPicked = selectedItems.some((s) => s.id === item.id);
                return (
                  <button
                    key={item.id}
                    onClick={() => handleSelectItem(item)}
                    style={{
                      ...bazaarStyles.marketCard,
                      border: isPicked ? '3px solid #175e24' : '2px solid #d4e8d6',
                      backgroundColor: isPicked ? '#eaf5eb' : '#ffffff',
                    }}
                  >
                    <span style={{ fontSize: '2.2rem' }}>{item.icon}</span>
                    <span style={{ fontSize: '1.05rem', fontWeight: '600', color: '#175e24', marginTop: '6px' }}>
                      {item.name}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {phase === 'done' && (
          <div style={gameStyles.successBox}>
            <CheckCircle2 size={36} color="#175e24" />
            <div>
              <h3 style={{ fontSize: '1.25rem', color: '#175e24', fontWeight: '700' }}>
                Wonderful Shopping!
              </h3>
              <p style={{ fontSize: '1.05rem', color: '#4a5c50', marginTop: '4px' }}>
                You remembered all the fresh items from the bazaar perfectly.
              </p>
            </div>
            <button style={gameStyles.nextBtn} onClick={handleRestart}>
              Visit Bazaar Again 🛍️
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

/* ========================================================================== */
/* STYLES                                                                     */
/* ========================================================================== */
const styles = {
  playGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: '24px',
    marginTop: '12px',
  },
  playCard: {
    backgroundColor: 'white',
    border: '1px solid var(--border-color)',
    borderRadius: '24px',
    padding: '36px 32px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    textAlign: 'center',
    boxShadow: 'var(--shadow-card)',
    gap: '16px',
    transition: 'transform 0.2s ease, box-shadow 0.2s ease',
  },
  iconCircleBig: {
    width: '64px',
    height: '64px',
    borderRadius: '50%',
    backgroundColor: '#e2f5e4',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    color: 'var(--primary-green)',
    marginBottom: '8px',
  },
  cardHeaderTitle: {
    fontSize: '1.45rem',
    fontWeight: '800',
    color: 'var(--text-main)',
  },
  cardHeaderDesc: {
    fontSize: '0.98rem',
    color: 'var(--text-muted)',
    lineHeight: '1.4',
    fontWeight: '500',
    minHeight: '44px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  cardStartBtn: {
    width: '100%',
    marginTop: '8px',
    backgroundColor: 'var(--primary-green)',
    color: 'white',
    borderRadius: '50px',
    padding: '12px 24px',
    fontWeight: '700',
    fontSize: '1rem',
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '8px',
  },
  pageTitle: {
    fontSize: '2.1rem',
    fontWeight: '800',
    color: 'var(--text-main)',
  },
  gamesGridLayout: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: '24px',
  },
  largeGameCard: {
    gridColumn: 'span 2',
    backgroundColor: 'white',
    border: '1px solid var(--border-color)',
    borderRadius: '24px',
    overflow: 'hidden',
    display: 'flex',
    boxShadow: 'var(--shadow-card)',
    minHeight: '320px',
  },
  largeCardImageCol: {
    flex: 1,
    height: '100%',
    minWidth: '220px',
  },
  largeCardImg: {
    width: '100%',
    height: '100%',
    objectFit: 'cover',
  },
  largeCardContentCol: {
    flex: 1,
    padding: '32px',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'flex-start',
    gap: '14px',
  },
  gameCardTitle: {
    fontSize: '1.75rem',
    fontWeight: '800',
    color: 'var(--text-main)',
  },
  gameCardDesc: {
    fontSize: '1.05rem',
    color: 'var(--text-muted)',
    lineHeight: '1.5',
    fontWeight: '500',
  },
  smallGameCard: {
    backgroundColor: 'white',
    border: '1px solid var(--border-color)',
    borderRadius: '24px',
    overflow: 'hidden',
    boxShadow: 'var(--shadow-card)',
    display: 'flex',
    flexDirection: 'column',
    minHeight: '340px',
  },
  smallCardImageWrapper: {
    height: '140px',
    width: '100%',
    overflow: 'hidden',
  },
  smallCardImg: {
    width: '100%',
    height: '100%',
    objectFit: 'cover',
  },
  smallCardIconWrapper: {
    height: '140px',
    backgroundColor: 'var(--secondary-green)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  musicNoteGraphic: {
    fontSize: '3.5rem',
  },
  smallCardContent: {
    padding: '20px',
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
    flex: 1,
  },
  smallCardTitle: {
    fontSize: '1.25rem',
    fontWeight: '800',
    color: 'var(--text-main)',
  },
  smallCardDesc: {
    fontSize: '0.95rem',
    color: 'var(--text-muted)',
    lineHeight: '1.4',
    fontWeight: '500',
  },
  container: {
    display: 'flex',
    flexDirection: 'column',
    gap: 'var(--spacing-xl)',
    paddingBottom: '100px',
  },
  header: {
    marginBottom: 'var(--spacing-sm)',
  },
  greetingTitle: {
    display: 'flex',
    alignItems: 'center',
    gap: 'var(--spacing-sm)',
    fontSize: 'var(--text-2xl)',
    color: 'var(--text-primary)',
    marginBottom: '4px',
  },
  leafIcon: {
    fontSize: '1.8rem',
  },
  subtitle: {
    fontSize: 'var(--text-lg)',
    color: 'var(--text-secondary)',
  },
  recommendBanner: {
    backgroundColor: '#d8f3dc',
    borderRadius: 'var(--radius-full)',
    padding: '12px 24px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    flexWrap: 'wrap',
    gap: '16px',
    boxShadow: 'var(--shadow-sm)',
  },
  recommendLeft: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
  },
  heartCircle: {
    width: '40px',
    height: '40px',
    borderRadius: '50%',
    backgroundColor: '#ffffff',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  recommendTag: {
    fontSize: '1rem',
    fontWeight: '700',
    color: '#175e24',
  },
  recommendText: {
    fontSize: '0.95rem',
    color: '#2d6a4f',
  },
  recommendBtn: {
    backgroundColor: '#175e24',
    color: '#ffffff',
    padding: '10px 24px',
    borderRadius: 'var(--radius-full)',
    fontSize: '0.95rem',
    fontWeight: '600',
    display: 'inline-flex',
    alignItems: 'center',
    minHeight: '44px',
  },
  featuredSection: {
    marginTop: 'var(--spacing-sm)',
  },
  featuredCard: {
    backgroundColor: 'var(--surface-color)',
    borderRadius: 'var(--radius-lg)',
    padding: 'var(--spacing-xl)',
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: 'var(--spacing-xl)',
    alignItems: 'center',
    boxShadow: 'var(--shadow-sm)',
  },
  featuredImageWrapper: {
    width: '100%',
    height: '280px',
    borderRadius: '16px',
    overflow: 'hidden',
  },
  featuredImage: {
    width: '100%',
    height: '100%',
    objectFit: 'cover',
  },
  featuredContent: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-start',
    gap: 'var(--spacing-md)',
  },
  featuredBadge: {
    backgroundColor: '#e8f5e9',
    color: '#175e24',
    fontSize: '0.9rem',
    fontWeight: '600',
    padding: '6px 16px',
    borderRadius: 'var(--radius-full)',
    display: 'inline-flex',
    alignItems: 'center',
    gap: '4px',
  },
  featuredTitle: {
    fontSize: '2rem',
    fontWeight: '700',
    color: 'var(--text-primary)',
  },
  featuredDesc: {
    fontSize: 'var(--text-base)',
    color: 'var(--text-secondary)',
    lineHeight: '1.6',
  },
  startFeaturedBtn: {
    backgroundColor: '#175e24',
    color: '#ffffff',
    padding: '14px 28px',
    borderRadius: 'var(--radius-full)',
    fontSize: '1.1rem',
    fontWeight: '600',
    minHeight: '52px',
    display: 'inline-flex',
    alignItems: 'center',
    cursor: 'pointer',
  },
  sectionTitle: {
    fontSize: '1.5rem',
    fontWeight: '700',
    color: 'var(--text-primary)',
    marginBottom: 'var(--spacing-lg)',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
    gap: 'var(--spacing-lg)',
  },
  card: {
    backgroundColor: 'var(--surface-color)',
    borderRadius: 'var(--radius-lg)',
    padding: 'var(--spacing-xl)',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-start',
    boxShadow: 'var(--shadow-sm)',
    gap: 'var(--spacing-md)',
  },
  iconCircle: {
    width: '64px',
    height: '64px',
    borderRadius: '50%',
    backgroundColor: '#d8eed6',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  cardTitle: {
    fontSize: '1.35rem',
    fontWeight: '700',
    color: 'var(--text-primary)',
  },
  cardDesc: {
    fontSize: '1rem',
    color: 'var(--text-secondary)',
    lineHeight: '1.5',
    flexGrow: 1,
  },
  cardBtn: {
    backgroundColor: '#d8eed6',
    color: '#175e24',
    padding: '14px 24px',
    borderRadius: 'var(--radius-full)',
    fontSize: '1.05rem',
    fontWeight: '700',
    width: '100%',
    minHeight: '52px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    cursor: 'pointer',
  },
  footer: {
    marginTop: 'var(--spacing-2xl)',
    borderTop: '1px solid #d4e8d6',
    paddingTop: 'var(--spacing-xl)',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    flexWrap: 'wrap',
    gap: 'var(--spacing-md)',
  },
  footerTop: {
    display: 'flex',
    flexDirection: 'column',
    gap: '4px',
  },
  footerLogo: {
    fontSize: '1.25rem',
    fontWeight: '800',
    color: '#175e24',
    letterSpacing: '1px',
  },
  footerCopy: {
    fontSize: '0.9rem',
    color: 'var(--text-secondary)',
  },
  footerLinks: {
    display: 'flex',
    gap: 'var(--spacing-md)',
    fontSize: '0.9rem',
    color: 'var(--text-secondary)',
    flexWrap: 'wrap',
  },
};

const gameStyles = {
  gameContainer: {
    maxWidth: '800px',
    margin: '0 auto',
    paddingBottom: '100px',
  },
  topBar: {
    marginBottom: '16px',
  },
  backBtn: {
    display: 'inline-flex',
    alignItems: 'center',
    color: '#175e24',
    fontSize: '1.1rem',
    padding: '8px 16px',
    borderRadius: '9999px',
    backgroundColor: '#eaf5eb',
  },
  headerSection: {
    textAlign: 'center',
    marginBottom: '24px',
  },
  gameTitle: {
    fontSize: '2.25rem',
    fontWeight: '700',
    color: '#1c2b20',
  },
  gameSubtitle: {
    fontSize: '1.25rem',
    color: '#4a5c50',
    marginTop: '6px',
  },
  cardBox: {
    backgroundColor: '#ffffff',
    borderRadius: '24px',
    padding: '32px',
    boxShadow: '0 4px 16px rgba(23, 94, 36, 0.08)',
  },
  imageContainer: {
    position: 'relative',
    borderRadius: '16px',
    overflow: 'hidden',
  },
  mainPhoto: {
    width: '100%',
    maxHeight: '450px',
    objectFit: 'cover',
    display: 'block',
  },
  targetOverlay: {
    position: 'absolute',
    right: '18%',
    top: '25%',
    width: '160px',
    height: '240px',
    borderRadius: '50%',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'flex-end',
    justifyContent: 'center',
    paddingBottom: '16px',
    transition: 'all 0.2s ease',
  },
  tapBadge: {
    backgroundColor: '#ffffff',
    color: '#175e24',
    padding: '8px 16px',
    borderRadius: '9999px',
    fontSize: '0.95rem',
    fontWeight: '700',
    boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
  },
  hintBtn: {
    display: 'inline-flex',
    alignItems: 'center',
    padding: '12px 28px',
    borderRadius: '9999px',
    border: '2px solid #d4e8d6',
    backgroundColor: '#ffffff',
    color: '#175e24',
    fontSize: '1.05rem',
    fontWeight: '600',
  },
  hintCard: {
    backgroundColor: '#f0f9ee',
    color: '#175e24',
    padding: '16px 24px',
    borderRadius: '16px',
    marginTop: '16px',
    fontSize: '1.05rem',
  },
  successBox: {
    backgroundColor: '#e8f5e9',
    borderRadius: '20px',
    padding: '24px',
    marginTop: '24px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    textAlign: 'center',
    gap: '16px',
  },
  nextBtn: {
    backgroundColor: '#175e24',
    color: '#ffffff',
    padding: '14px 28px',
    borderRadius: '9999px',
    fontSize: '1.1rem',
    fontWeight: '600',
    minHeight: '52px',
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '100%',
    maxWidth: '300px',
  },
};

const kitchenStyles = {
  slotContainer: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))',
    gap: '12px',
    marginBottom: '24px',
  },
  slotCard: {
    backgroundColor: '#f4fbf5',
    border: '1.5px dashed #a8d5af',
    borderRadius: '16px',
    padding: '12px',
    minHeight: '80px',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    textAlign: 'center',
  },
  slotNum: {
    fontSize: '0.85rem',
    color: '#4a5c50',
    fontWeight: '600',
    marginBottom: '4px',
  },
  slotContent: {
    fontSize: '0.95rem',
  },
  ingGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
    gap: '16px',
  },
  ingCard: {
    backgroundColor: '#ffffff',
    borderRadius: '16px',
    padding: '16px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '8px',
    cursor: 'pointer',
    minHeight: '110px',
  },
};

const rhythmStyles = {
  listenBtn: {
    backgroundColor: '#175e24',
    color: '#ffffff',
    padding: '16px 32px',
    borderRadius: '9999px',
    fontSize: '1.15rem',
    fontWeight: '700',
    display: 'inline-flex',
    alignItems: 'center',
  },
  drumPad: {
    position: 'relative',
    borderRadius: '24px',
    overflow: 'hidden',
    cursor: 'pointer',
    height: '280px',
    boxShadow: '0 6px 20px rgba(23, 94, 36, 0.15)',
  },
  drumImg: {
    width: '100%',
    height: '100%',
    objectFit: 'cover',
  },
  drumOverlay: {
    position: 'absolute',
    inset: 0,
    backgroundColor: 'rgba(23, 94, 36, 0.45)',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
  },
};

const motifStyles = {
  stripContainer: {
    backgroundColor: '#f0f9ee',
    borderRadius: '16px',
    padding: '20px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '16px',
    marginBottom: '28px',
  },
  patternCell: {
    backgroundColor: '#ffffff',
    border: '2px solid #175e24',
    borderRadius: '12px',
    padding: '12px 20px',
    fontSize: '1.1rem',
    fontWeight: '700',
    color: '#175e24',
  },
  arrow: {
    fontSize: '1.5rem',
    color: '#175e24',
    fontWeight: 'bold',
  },
  optionsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '16px',
  },
  optionCard: {
    backgroundColor: '#ffffff',
    border: '2px solid #d4e8d6',
    borderRadius: '16px',
    padding: '20px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    textAlign: 'center',
    cursor: 'pointer',
  },
};

const bazaarStyles = {
  itemList: {
    display: 'flex',
    justifyContent: 'center',
    gap: '16px',
    flexWrap: 'wrap',
    marginBottom: '28px',
  },
  itemPill: {
    backgroundColor: '#eaf5eb',
    border: '2px solid #175e24',
    borderRadius: '9999px',
    padding: '10px 24px',
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))',
    gap: '16px',
  },
  marketCard: {
    borderRadius: '16px',
    padding: '16px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    textAlign: 'center',
    cursor: 'pointer',
    minHeight: '120px',
  },
};
