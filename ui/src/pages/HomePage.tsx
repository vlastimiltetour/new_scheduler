import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';


export default function HomePage() {
  return (
    <>
     <h1
        style={{
          color: '#ffffff',
          fontFamily: "'Playfair Display', Georgia, serif",
          fontSize: 'clamp(2.5rem, 6vw, 5.5rem)',
          fontWeight: 600,
          textAlign: 'center',
          textShadow: '2px 4px 20px rgba(0, 0, 0, 0.7)',
          margin: 0,
          padding: '0 20px'
        }}
      >
        Interview Scheduler
      </h1>

      {/* Tlačítko přesměrovávající na /persons */}
      <Link to="/persons" style={{ textDecoration: 'none' }}>
        <button
          style={{
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
            gap: '8px'
          }}
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
       {/* Tlačítko přesměrovávající na /Credits */}
      <Link to="/Credits" style={{ textDecoration: 'none' }}>
        <button
          style={{
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
            gap: '8px'
          }}
          onMouseOver={(e) => {
            e.currentTarget.style.transform = 'translateY(-2px)';
            e.currentTarget.style.backgroundColor = '#f3f4f6';
          }}
          onMouseOut={(e) => {
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.backgroundColor = '#ffffff';
          }}
        >
          Credits
        </button>
      </Link>
      </>
  );
}
      