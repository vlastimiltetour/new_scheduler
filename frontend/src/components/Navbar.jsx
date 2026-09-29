// Navbar.jsx
import React from 'react';
import { routesConfig } from '../routes';

export default function Navbar() {
  return (
    <nav style={styles.nav}>
      <div style={styles.logo}>Interview Scheduler</div>
      <ul style={styles.menu}>
        {routesConfig.map((route) => (
            <li><a href={route.path} style={styles.link}>{route.label}</a></li>
        ))}
      </ul>
    </nav>
  );
}

// Všechny styly pro Navbar jsou tady uvnitř!
const styles = {
  nav: {
    width: '100%',
    boxSizing: 'border-box',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '16px 24px',
    fontFamily: "'Playfair Display', Georgia, serif",
  },
  logo: {
    color: '#ffffff',
    fontSize: '20px',
    fontWeight: 'bold',
  },
  menu: {
    display: 'flex',
    gap: '20px',
    listStyle: 'none',
    margin: 0,
    padding: 0,
  },
  link: {
    color: '#ffffff',
    textDecoration: 'none',
    fontSize: '16px',
  },
};