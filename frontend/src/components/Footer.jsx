import React from 'react';
import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer style={styles.footer} role="contentinfo" aria-label="Page Footer">
      <div style={styles.container}>
        {/* Left Side: Brand Logo and Copyright */}
        <div style={styles.leftCol}>
          <span style={styles.logoText}>SMRITHI</span>
          <span style={styles.copyrightText}>
            © 2026 SMRITHI. Your caring cognitive companion.
          </span>
        </div>

        {/* Right Side: Links */}
        <nav style={styles.navLinks} aria-label="Footer Links">
          <Link to="/" style={styles.link}>Home</Link>
          <Link to="/library" style={styles.link}>Library</Link>
          <Link to="/gallery" style={styles.link}>Gallery</Link>
          <Link to="/schedule" style={styles.linkActive}>Schedule</Link>
          <Link to="/privacy" style={styles.link}>Privacy Policy</Link>
          <Link to="/help" style={styles.link}>Help Center</Link>
          <Link to="/caregiver" style={styles.link}>Caregiver Access</Link>
        </nav>
      </div>
    </footer>
  );
}

const styles = {
  footer: {
    backgroundColor: '#eaf5ea',
    borderTop: '1px solid #d2ebd4',
    padding: '32px 48px',
    marginTop: '64px',
    width: '100%',
  },
  container: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    maxWidth: '1300px',
    margin: '0 auto',
    flexWrap: 'wrap',
    gap: '24px',
  },
  leftCol: {
    display: 'flex',
    flexDirection: 'column',
    gap: '6px',
  },
  logoText: {
    fontSize: '1.25rem',
    fontWeight: '800',
    color: 'var(--primary-green)',
    letterSpacing: '0.8px',
  },
  copyrightText: {
    fontSize: '0.9rem',
    color: 'var(--text-muted)',
    fontWeight: '500',
  },
  navLinks: {
    display: 'flex',
    gap: '24px',
    flexWrap: 'wrap',
  },
  link: {
    fontSize: '0.95rem',
    fontWeight: '600',
    color: 'var(--text-muted)',
    transition: 'color 0.2s ease',
  },
  linkActive: {
    fontSize: '0.95rem',
    fontWeight: '600',
    color: 'var(--primary-green)',
    textDecoration: 'underline',
    textUnderlineOffset: '4px',
  }
};
