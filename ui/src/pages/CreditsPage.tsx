import React from 'react';
import Navbar from '../components/Navbar';
import Layout from '../components/Layout';

export default function CreditsPage() {
  const creditsData = [
    {
      title: 'People',
      items: ['Author: Vlastimil Tetour', 'Mentoring: Vojtěch Brom']
    },
    {
      title: 'Backend',
      items: ['Python 3', 'FastAPI', 'Uvicorn', 'SQLAlchemy 2.0', 'Pydantic v2']
    },
    {
      title: 'Database',
      items: ['PostgreSQL', 'Psycopg 3']
    },
    {
      title: 'Frontend',
      items: ['React', 'Tailwind CSS v4', 'PostCSS', 'Autoprefixer']
    },
    {
      title: 'Testing & Tools',
      items: ['Pytest', 'Testcontainers', 'Docker', 'HTTPX']
    }
  ];

  return (
    <>
    
    <div
      style={{
        padding: '30px',
        color: '#ffffff',
        fontFamily: 'Inter, system-ui, sans-serif',
        maxWidth: '800px',
        margin: '0 auto'
      }}
    >
      <h2
        style={{
          fontSize: '2rem',
          marginBottom: '32px',
          
          paddingBottom: '12px'
        }}
      >
        Credits 
      </h2>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '180px 1fr', // Nadpis vlevo (180px), obsah vpravo
          rowGap: '28px',
          columnGap: '20px',
          alignItems: 'start'
        }}
      >
        {creditsData.map((section, idx) => (
          <React.Fragment key={idx}>
            {/* Nadpis sekce (vlevo) */}
            <h3
              style={{
                margin: 0,
                fontSize: '1.1rem',
                fontWeight: 600,
                color: '#fafafa',
                letterSpacing: '0.05em'
              }}
            >
              {section.title}
            </h3>

            {/* Seznam prvků (vpravo ve stejné úrovni) */}
            <ul
              style={{
                margin: 0,
                padding: 0,
                listStyle: 'none',
                display: 'flex',
                flexDirection: 'column',
                gap: '6px'
              }}
            >
              {section.items.map((item, itemIdx) => (
                <li
                  key={itemIdx}
                  style={{
                    fontSize: '1rem',
                    color: '#fefeff'
                  }}
                >
                  {item}
                </li>
              ))}
            </ul>
          </React.Fragment>
        ))}
      </div>
    </div>
  </>
  );
}