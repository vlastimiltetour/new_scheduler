import React, { useEffect, useState } from 'react';

export default function PersonsPage() {
  const [persons, setPersons] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8080/api/v1/persons/')
      .then((res) => res.json())
      .then((data) => setPersons(data))
      .catch((err) => console.error('Error fetching data:', err));
  }, []);

  return (
    <div style={styles.container}>
      <h2 style={styles.heading}>Users</h2>

      <div style={styles.tableWrapper}>
        <table style={styles.table}>
          <thead>
            <tr style={styles.headerRow}>
              <th style={styles.th}>Name</th>
              <th style={styles.th}>Role</th>
              <th style={styles.th}>Email</th>
              <th style={{ ...styles.th, textAlign: 'center' }}>Detail</th>
              <th style={{ ...styles.th, textAlign: 'center' }}>Update</th>
              <th style={{ ...styles.th, textAlign: 'center' }}>Delete</th>
            </tr>
          </thead>
          <tbody>
            {persons.length === 0 ? (
              <tr>
                <td colSpan={6} style={styles.emptyTd}>
                  Žádná data k zobrazení
                </td>
              </tr>
            ) : (
              persons.map((p, index) => (
                <tr 
                  key={p.id || index} 
                  style={index % 2 === 0 ? styles.trEven : styles.trOdd}
                >
                  <td style={{ ...styles.td, fontWeight: 'bold' }}>{p.name}</td>
                  <td style={styles.td}>{p.person_type}</td>
                  <td style={styles.td}>{p.email}</td>
                  <td style={{ ...styles.td, textAlign: 'center', cursor: 'pointer' }}>🔍</td>
                  <td style={{ ...styles.td, textAlign: 'center', cursor: 'pointer' }}>📝</td>
                  <td style={{ ...styles.td, textAlign: 'center', cursor: 'pointer' }}>❌</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// Čisté CSS styly přímo v JS (funguje všude)
const styles = {
  container: {
    padding: '24px',
    fontFamily: 'system-ui, -apple-system, sans-serif',
    width: '100%',
    margin: '0 auto',
    minHeight: '100vh',
    boxSizing: 'border-box'
  },
  heading: {
    fontSize: '24px',
    fontWeight: '600',
    marginBottom: '16px',
    color: '#ffffff',
  },
  tableWrapper: {
    border: '1px solid #e5e7eb',
    borderRadius: '8px',
    overflow: 'hidden',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    fontSize: '14px',
  },
  headerRow: {
    backgroundColor: '#f3f4f6',
    borderBottom: '2px solid #e5e7eb',
  },
  th: {
    padding: '12px 16px',
    textAlign: 'left',
    color: '#374151',
    fontWeight: '600',
  },
  td: {
    padding: '12px 16px',
    color: 'rgb(255, 255, 255)',
  },
 
  emptyTd: {
    padding: '24px',
    textAlign: 'center',
    color: '#9ca3af',
    fontStyle: 'italic',
  },
};