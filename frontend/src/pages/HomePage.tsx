import React from 'react';
import { Link } from 'react-router-dom';

export default function HomePage() {
  return (
    <div style={styles.container}>
      <h1
        style={{
          color: '#ffffff',
          fontFamily: "'Playfair Display', Georgia, serif",
          fontSize: 'clamp(2.5rem, 6vw, 5.5rem)',
          fontWeight: 600,
          textAlign: 'center',
          textShadow: '2px 4px 20px rgba(0, 0, 0, 0.7)',
          margin: 0,
          padding: '0 20px',
          marginBottom: '20px'
        }}
      >
        Schedulin' Beast
      </h1>

      {/* Skupina tlačítek zarovnaná vedle sebe */}
      <div style={styles.buttonGroup}>
        {/* Tlačítko přesměrovávající na /persons */}
        <Link to="/persons" style={{ textDecoration: 'none' }}>
          <button
            style={styles.button}
            onMouseOver={(e) => {
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.backgroundColor = '#f3f4f6';
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.backgroundColor = '#ffffff';
            }}
          >
            Let's do some schedulin' &rarr;
          </button>
        </Link>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center', // Svislé vycentrování
    alignItems: 'center',     // Vodorovné vycentrování
    minHeight: 'calc(100vh - 60px)',
    width: '100vw',
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    backgroundRepeat: 'no-repeat',
    boxSizing: 'border-box',
    overflow: 'hidden',
    padding: '0px',

  },
  buttonGroup: {
    display: 'flex',
    flexDirection: 'row',     // Dává tlačítka vedle sebe
    gap: '16px',              // Mezera mezi tlačítky
    flexWrap: 'wrap',         // Ošetření pro mobilní displeje
    justifyContent: 'center',
  },
  button: {
    backgroundColor: '#ffffff',
    color: '#111827',
    border: 'none',
    padding: '14px 28px',
    fontSize: '1.1rem',
    fontWeight: 600,
    fontFamily: "'Inter', sans-serif",
    borderRadius: '50px',
    cursor: 'pointer',
    boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.3)',
    transition: 'all 0.2s ease',
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  },
};