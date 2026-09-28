import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './Navbar'; // Uprav cestu k tvému Navbaru

export default function Layout() {
  return (
    <div style={styles.layoutContainer}>
      {/* 1. Navbar je tady jen JEDNOU pro celou aplikaci */}
      <Navbar />

      {/* 2. Obal pro stránky načítané přes Outlet */}
      <main style={styles.mainContent}>
        <Outlet />
      </main>
    </div>
  );
}

const styles = {
  layoutContainer: {
    width: '100vw',
    minHeight: '100vh', // Přesně 100 % výšky obrazovky
    display: 'flex',
    flexDirection: 'column',
    backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url('/bg.jpg')`,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    backgroundRepeat: 'no-repeat',
    backgroundAttachment: 'fixed', // 🔥 TENTO ŘÁDEK VYŘEŠÍ PROBLÉM
    boxSizing: 'border-box',
    
  },
  mainContent: {
    flex: 1, // Vyplní veškeré zbývající místo pod Navbarem
    padding: '0px',
    boxSizing: 'border-box',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
};