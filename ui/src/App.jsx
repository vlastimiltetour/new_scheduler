import React, { useEffect } from 'react';
import.meta.env.VITE_API_URL

export default function App() {
  
  useEffect(() => {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8080';

    fetch(`${apiUrl}`)
      .then((res) => res.json())
      .then((data) => console.log('Odpověď z FastAPI:', data))
      .catch((err) => console.error('Chyba při připojení k FastAPI:', err));
  }, []);

  return (
    <>
      <link
        href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;1,400&display=swap"
        rel="stylesheet"
      />

      {/* Vynulování okrajů prohlížeče a vynucení plné šířky/výšky */}
      <style>{`
        * {
          box-sizing: border-box;
        }
        html, body {
          margin: 0 !important;
          padding: 0 !important;
          width: 100% !important;
          height: 100% !important;
          overflow-x: hidden;
        }
      `}</style>

      <div
        style={{
          // Načtení lokálního obrázku
          backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url('/bg.jpg')`,
          
          // Klíčové vlastnosti pro plné pokrytí
          backgroundSize: 'cover',       // Roztáhne obrázek tak, aby VŽDY pokryl celou plochu
          backgroundPosition: 'center',  // Vycentruje ho
          backgroundRepeat: 'no-repeat',
          
          // Rozměry
          width: '100vw',
          minHeight: '100vh',
          
          // Vycentrování textu doprostřed
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center'
        }}
      >
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
      </div>
    </>
  );
}