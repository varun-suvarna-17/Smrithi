import React, { useState, useEffect } from 'react';
import { User, Activity, Brain, FileText, CheckCircle, Droplet, ChevronDown, ArrowRight, AlertCircle } from 'lucide-react';
import { caregiverAPI, patientAPI, progressAPI } from '../utils/api';

export default function CaregiverDashboard() {
  const [patients, setPatients] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch caregiver's assigned patients and data
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Get assigned patients
        const patientsResponse = await caregiverAPI.getAssignedPatients();
        const pats = patientsResponse.data || [];
        setPatients(pats);
        
        // Select first patient by default
        if (pats.length > 0) {
          setSelectedPatient(pats[0]);
          
          // Get their progress
          const progressResponse = await progressAPI.getProgress(pats[0].id);
          setProgress(progressResponse.data);
        }
      } catch (err) {
        console.error('Error fetching dashboard:', err);
        setError(err.message);
        // Use dummy data
        setPatients([{
          id: 'dummy_1',
          name: 'Asha Devi',
          age: 72,
          patientId: 'ASH1023',
          profileImg: 'https://i.pravatar.cc/150?u=asha'
        }]);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Fetch progress when patient changes
  useEffect(() => {
    if (selectedPatient) {
      const fetchProgress = async () => {
        try {
          const progressResponse = await progressAPI.getProgress(selectedPatient.id);
          setProgress(progressResponse.data);
        } catch (err) {
          console.error('Error fetching progress:', err);
        }
      };
      fetchProgress();
    }
  }, [selectedPatient]);

  if (loading) {
    return (
      <div style={styles.container}>
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <p>Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error && patients.length === 0) {
    return (
      <div style={styles.container}>
        <div style={{ ...styles.card, color: 'red', padding: '20px' }}>
          <AlertCircle size={24} />
          <p>Error loading dashboard: {error}</p>
        </div>
      </div>
    );
  }

  const patient = selectedPatient || patients[0];
  return (
    <div style={styles.container}>
      {/* Patient Header */}
      <section style={styles.patientHeader}>
        <div style={styles.patientInfo}>
          <img src="https://i.pravatar.cc/150?u=asha" alt="Asha Devi" style={styles.profileImg} />
          <div>
            <h2 style={{ fontSize: 'var(--text-xl)', fontWeight: '700' }}>Asha Devi</h2>
            <div style={{ display: 'flex', gap: 'var(--spacing-md)', marginTop: '4px' }}>
              <span style={styles.badge}><User size={16} /> Age: 72</span>
              <span style={styles.badge}><FileText size={16} /> Patient ID: ASH1023</span>
            </div>
          </div>
        </div>
        <button style={styles.filterBtn}>
          This Week <ChevronDown size={20} />
        </button>
      </section>

      {/* Stats Grid */}
      <section style={styles.statsGrid}>
        <StatCard title="Overall Score" value="72%" sub="Good status" type="score" />
        <StatCard title="Games Completed" value="14 / 20" sub="" type="progress" progress={70} color="#8d6e63" />
        <StatCard title="Reminders Taken" value="18 / 22" sub="" type="progress" progress={81} color="var(--primary-color)" />
        <StatCard title="Engagement" value="80%" sub="Active Status" type="engagement" />
      </section>

      {/* Main Content Area */}
      <section style={styles.mainContent}>
        {/* Cognitive Assessment */}
        <div style={{ ...styles.card, flex: 2 }}>
          <h3 style={styles.sectionTitle}><Brain size={24} /> Cognitive Assessment</h3>
          <div style={styles.chartPlaceholder}>
            {/* Simple CSS representation of a radar chart placeholder */}
            <div style={styles.radarGraphic}>
              <div style={styles.radarWeb}></div>
              <div style={styles.radarFill}></div>
              <span style={{...styles.radarLabel, top: '0', left: '50%', transform: 'translateX(-50%)'}}>Memory</span>
              <span style={{...styles.radarLabel, top: '40%', right: '-20px'}}>Attention</span>
              <span style={{...styles.radarLabel, bottom: '0', right: '10%'}}>Recall</span>
              <span style={{...styles.radarLabel, bottom: '0', left: '10%'}}>Pattern</span>
              <span style={{...styles.radarLabel, top: '40%', left: '-20px'}}>Orientation</span>
            </div>
          </div>
        </div>

        {/* Insights */}
        <div style={{ ...styles.card, flex: 1, backgroundColor: 'var(--primary-color)', color: 'white', display: 'flex', flexDirection: 'column' }}>
          <h3 style={{ ...styles.sectionTitle, color: 'white' }}>✨ Insights</h3>
          <p style={{ fontSize: 'var(--text-lg)', lineHeight: '1.4', flex: 1 }}>
            "Great progress in <strong>Attention!</strong> Try more Memory Recall activities this week to maintain cognitive balance."
          </p>
          <button style={styles.whiteBtn}>View Activities <ArrowRight size={20} /></button>
        </div>
      </section>

      {/* Recent Activity */}
      <section style={styles.card}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--spacing-lg)' }}>
          <h3 style={styles.sectionTitle}>Recent Activity</h3>
          <button style={{ color: 'var(--text-secondary)', fontWeight: '600' }}>View All &gt;</button>
        </div>
        
        <div style={styles.activityList}>
          <ActivityItem icon={<Brain size={20} color="var(--primary-color)" />} title="Memory Match Game" desc="Completed level 4" time="2:30 PM" extra={<span style={styles.scoreBadge}>Score: 80%</span>} />
          <ActivityItem icon={<PillIcon />} title="Medicine Taken" desc="Afternoon dosage confirmed via app." time="1:00 PM" extra={<span style={styles.verifiedText}><CheckCircle size={16} /> Verified</span>} />
          <ActivityItem icon={<Droplet size={20} color="var(--primary-color)" />} title="Water Reminder" desc="Drank 1 glass of water." time="11:00 AM" />
        </div>
      </section>
    </div>
  );
}

function PillIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--primary-color)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M10.5 20.5 19 12a4.95 4.95 0 1 0-7-7L3.5 13.5a4.95 4.95 0 1 0 7 7Z"/>
      <path d="m8.5 8.5 7 7"/>
    </svg>
  );
}

function StatCard({ title, value, sub, type, progress, color }) {
  return (
    <div style={styles.statCard}>
      <h4 style={styles.statTitle}>{title}</h4>
      <div style={styles.statValueRow}>
        <span style={styles.statValue}>{value}</span>
        {type === 'score' && <Activity color="var(--primary-color)" size={28} />}
        {type === 'engagement' && <span style={styles.heartIcon}>♡</span>}
      </div>
      {type === 'progress' && (
        <div style={styles.progressBar}>
          <div style={{ width: `${progress}%`, backgroundColor: color, height: '100%', borderRadius: '4px' }}></div>
        </div>
      )}
      {sub && <div style={styles.statSub}>{sub}</div>}
    </div>
  );
}

function ActivityItem({ icon, title, desc, time, extra }) {
  return (
    <div style={styles.activityItem}>
      <div style={styles.activityIcon}>{icon}</div>
      <div style={styles.activityContent}>
        <h4 style={styles.activityTitle}>{title}</h4>
        <p style={styles.activityDesc}>{desc}</p>
        {extra && <div style={{ marginTop: '8px' }}>{extra}</div>}
      </div>
      <div style={styles.activityTime}>{time}</div>
    </div>
  );
}

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    gap: 'var(--spacing-xl)',
    paddingBottom: '100px',
  },
  patientHeader: {
    backgroundColor: 'var(--surface-color)',
    padding: 'var(--spacing-lg) var(--spacing-xl)',
    borderRadius: 'var(--radius-lg)',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    boxShadow: 'var(--shadow-sm)',
  },
  patientInfo: {
    display: 'flex',
    alignItems: 'center',
    gap: 'var(--spacing-lg)',
  },
  profileImg: {
    width: '64px',
    height: '64px',
    borderRadius: '50%',
    objectFit: 'cover',
  },
  badge: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '4px',
    backgroundColor: 'var(--bg-color)',
    color: 'var(--text-secondary)',
    padding: '4px 12px',
    borderRadius: 'var(--radius-full)',
    fontSize: 'var(--text-sm)',
    fontWeight: '500',
  },
  filterBtn: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    backgroundColor: 'var(--bg-color)',
    padding: '12px 20px',
    borderRadius: 'var(--radius-full)',
    fontWeight: '600',
    fontSize: 'var(--text-base)',
  },
  statsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(4, 1fr)',
    gap: 'var(--spacing-md)',
  },
  statCard: {
    backgroundColor: 'var(--surface-color)',
    padding: 'var(--spacing-lg)',
    borderRadius: 'var(--radius-lg)',
    boxShadow: 'var(--shadow-sm)',
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
  },
  statTitle: {
    fontSize: 'var(--text-sm)',
    color: 'var(--text-secondary)',
    fontWeight: '600',
  },
  statValueRow: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  statValue: {
    fontSize: 'var(--text-2xl)',
    fontWeight: '700',
  },
  statSub: {
    fontSize: 'var(--text-sm)',
    color: 'var(--text-secondary)',
    marginTop: 'auto',
  },
  progressBar: {
    height: '8px',
    backgroundColor: 'var(--bg-color)',
    borderRadius: '4px',
    marginTop: 'auto',
    overflow: 'hidden',
  },
  heartIcon: {
    backgroundColor: '#e8f5e9',
    color: 'var(--success-color)',
    width: '32px',
    height: '32px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: '50%',
    fontSize: '18px',
  },
  mainContent: {
    display: 'flex',
    gap: 'var(--spacing-lg)',
  },
  card: {
    backgroundColor: 'var(--surface-color)',
    padding: 'var(--spacing-xl)',
    borderRadius: 'var(--radius-lg)',
    boxShadow: 'var(--shadow-sm)',
  },
  sectionTitle: {
    fontSize: 'var(--text-lg)',
    fontWeight: '600',
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    marginBottom: 'var(--spacing-lg)',
  },
  chartPlaceholder: {
    height: '250px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    position: 'relative',
  },
  radarGraphic: {
    width: '180px',
    height: '180px',
    position: 'relative',
  },
  radarWeb: {
    position: 'absolute',
    inset: 0,
    border: '2px solid #e0e0e0',
    borderRadius: '50%', // Simple representation
  },
  radarFill: {
    position: 'absolute',
    inset: '20px',
    backgroundColor: 'rgba(23, 94, 36, 0.2)',
    border: '2px solid var(--primary-color)',
    clipPath: 'polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%)', // Pentagon
  },
  radarLabel: {
    position: 'absolute',
    fontSize: 'var(--text-sm)',
    color: 'var(--text-secondary)',
    backgroundColor: 'var(--surface-color)',
    padding: '2px 8px',
    borderRadius: '12px',
    border: '1px solid #eee',
  },
  whiteBtn: {
    backgroundColor: 'white',
    color: 'var(--primary-color)',
    padding: '16px',
    borderRadius: 'var(--radius-md)',
    fontWeight: '600',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    gap: '8px',
    fontSize: 'var(--text-base)',
    marginTop: 'var(--spacing-lg)',
  },
  activityList: {
    display: 'flex',
    flexDirection: 'column',
    gap: 'var(--spacing-md)',
  },
  activityItem: {
    display: 'flex',
    gap: 'var(--spacing-lg)',
    padding: 'var(--spacing-md) 0',
    borderBottom: '1px solid #f0f0f0',
  },
  activityIcon: {
    width: '48px',
    height: '48px',
    backgroundColor: 'var(--bg-color)',
    borderRadius: 'var(--radius-md)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  activityContent: {
    flex: 1,
  },
  activityTitle: {
    fontSize: 'var(--text-base)',
    fontWeight: '600',
  },
  activityDesc: {
    fontSize: 'var(--text-sm)',
    color: 'var(--text-secondary)',
  },
  activityTime: {
    fontSize: 'var(--text-sm)',
    color: 'var(--text-secondary)',
    fontWeight: '500',
  },
  scoreBadge: {
    backgroundColor: '#e8f5e9',
    color: 'var(--success-color)',
    padding: '4px 12px',
    borderRadius: 'var(--radius-full)',
    fontSize: 'var(--text-sm)',
    fontWeight: '500',
  },
  verifiedText: {
    color: 'var(--success-color)',
    fontSize: 'var(--text-sm)',
    fontWeight: '500',
    display: 'inline-flex',
    alignItems: 'center',
    gap: '4px',
  }
};
