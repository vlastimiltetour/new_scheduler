import React, { useEffect, useState } from 'react';
import UserModal from '../components/UserModal';


export default function PersonsPage() {
  const [persons, setPersons] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalMode, setModalMode] = useState('ADD');
  const [selectedPerson, setSelectedPerson] = useState(null);

  const fetchPersons = () => {
    fetch('http://localhost:8080/api/v1/persons/')
      .then((res) => res.json())
      .then((data) => setPersons(data))
      .catch((err) => console.error('Error fetching data:', err));
  }

  useEffect(() => {
    fetchPersons();
  }, []);
  
  // Read
  const openModal = (mode, person = null) => {
    setModalMode(mode);
    setIsModalOpen(true);

    if ((mode === 'DETAIL') && person?.id) {
       fetch(`http://localhost:8080/api/v1/persons/${person.id}`)
      .then((res) => res.json())
      .then((data) => setSelectedPerson(data))
      .catch((err) => {
        console.error('Error fetching data:', err);
        setSelectedPerson(person);
      });
      } else {
        setSelectedPerson(person);
      } 
    };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedPerson(null);
  };


  // Create & Update & Delete (CUD)
  const handleConfirm = (formData) => {
    console.log('Confirm action:', modalMode, formData);

     if (modalMode === 'DELETE') {
      // 1. Správná URL s formData.id a opravená metoda DELETE
      fetch(`http://localhost:8080/api/v1/persons/${formData.id}`, {
        method: 'DELETE',
      })
        .then((res) => {
          if (!res.ok) {
            throw new Error('An error occurred while deleting user');
          }
          // Bezpečné ošetření, pokud API nevrací JSON (např. HTTP 204)
          return res.status !== 204 ? res.json() : null;
        })
        .then(() => {
          fetchPersons(); // 2. Obnovení seznamu v tabulce po smazání
        })
        .catch((err) => console.error('Error deleting user:', err));
      }

      else if (modalMode === 'UPDATE') {

      const newPersonData = {
        id: formData.id,
        name: formData.name,
        email: formData.email,
        person_type: formData.person_type,
      };

      fetch(`http://localhost:8080/api/v1/persons/${formData.id}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newPersonData),
    }).then((res) => {
        if (!res.ok) {
          throw Error('An error during user input')
        }
          return res.json();
        })
      .then(() => {
        fetchPersons();
      })
      .catch((err) => 
        console.error('Error adding user data:', err, newPersonData));

      } 
    
     else if (modalMode === 'ADD') {

      const newPersonData = {
        name: formData.name,
        email: formData.email,
        person_type: formData.person_type,
       
      };

      fetch('http://localhost:8080/api/v1/persons/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newPersonData),
    }).then((res) => {
        if (!res.ok) {
          throw Error('An error during user input')
        }
          return res.json();
        })
      .then(() => {
        fetchPersons();
      })
      .catch((err) => 
        console.error('Error adding user data:', err, newPersonData));

      } 
    closeModal();
  };


    
  

  return (
    
    <div style={styles.page}>
    <div style={styles.container}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', margin: '16px'}}>
      <h2 style={styles.heading}>Users</h2>

      <button style={styles.addBtn} onClick={() => openModal('ADD')}>Add | +</button>
        {/* Samotné Modal / Popup okno (zobrazí se jen když isModalOpen === true) */}
      </div>

    

      <div style={styles.tableWrapper}>
        <table style={styles.table}>
          <thead>
            <tr style={styles.headerRow}>
              <th style={styles.th}>Name</th>
              <th style={{ ...styles.th, textAlign: 'center' }}></th>
              <th style={{ ...styles.th, textAlign: 'center' }}></th>
              <th style={styles.th}>Role</th>
              <th style={styles.th}>Email</th>
             
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
                  <td style={{ ...styles.td, fontWeight: 'bold' }}>
                    <button style={styles.detailBtn} onClick={() => openModal('DETAIL', p)}>{p.name}
                    </button>
                      <div style={{ display: 'flex', gap: '6px' , alignItems: 'center'}}>
                    
                        
                      </div>
                    </td>
                  <td style={{ ...styles.td, textAlign: 'center', cursor: 'pointer' }}>
                        <button style={styles.detailBtn} onClick={() => openModal('UPDATE', p)}>✏️</button>
                  </td>
                  <td style={{ ...styles.td, textAlign: 'center', cursor: 'pointer' }}>
                    <button style={styles.detailBtn} onClick={() => openModal('DELETE', p)}>❌</button>
                  </td>
                  <td style={styles.td}>{p.person_type}</td>
                  <td style={styles.td}>{p.email}</td>
                 
               
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    
    
    </div>
  
    <UserModal 
      isOpen={isModalOpen}
      onClose={closeModal}
      onConfirm={handleConfirm}
      mode={modalMode}
      initialData={selectedPerson}
    />
    </div>
    
  );
}

const styles = {
  page: {
    display: 'flex',          // 1. Aktivuje Flexbox
    flexDirection: 'column',   // 2. Prvky se řadí pod sebe (Navbar nahoru, main pod něj)
    minHeight: '100vh',           // 3. Přesně 100 % výšky obrazovky (nikoliv minHeight)
    width: '100%',
    boxSizing: 'border-box',
    overflowY: 'auto',        // Zamezí scrollování celé stránky
  },
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
    marginBottom: '0px',
    marginLeft: '16px',
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
  addBtn: {
    padding: '10px 20px',
    fontSize: '16px',
    backgroundColor: 'transparent',
    color: 'white',
    cursor: 'pointer',
    border: '1px solid #e5e7eb',
    borderRadius: '8px',
    overflow: 'hidden',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    marginBottom: '0px',
    marginRight: '16px',
  },
detailBtn: {
  background: 'none',
  border: 'none',
  padding: '6px',
  cursor: 'pointer',
  fontSize: '16px',
  color: '#e5e7eb',
  display: 'inline-flex',
  alignItems: 'center',
  justifyContent: 'center',
  transition: 'transform 0.15s ease, opacity 0.15s ease',
  outline: 'none',
},
  addBtnHover: {
    backgroundColor: '#0056b3',
  },
  modalOverlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    width: '100vw',
    height: '100vh',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 99999,
  },
  modalContent: {
    background: 'white',
    padding: '24px',
    borderRadius: '8px',
    width: '400px',
    maxWidth: '90%',
    boxShadow: '0 4px 15px rgba(0, 0, 0, 0.2)',
  },
  modalActions: {
    display: 'flex',
    justifyContent: 'flex-end',
    gap: '10px',
    marginTop: '20px',
  },
  actionBtn: {
    padding: '8px 16px',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
  },
  closeBtn: {
    backgroundColor: '#ccc',
  },
  saveBtn: {
    backgroundColor: '#28a745',
    color: 'white',
  },
};
