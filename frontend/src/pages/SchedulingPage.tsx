import React, { useState, useEffect } from 'react';
import AvailabilityCalendar from '../components/availabilityCalendar';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';

// Ukázková data
const DAYS = [
  { key: 'Mon', label: 'Mon', dateStr: 'Oct 6' },
  { key: 'Tue', label: 'Tue', dateStr: 'Oct 7' },
  { key: 'Wed', label: 'Wed', dateStr: 'Oct 8' },
  { key: 'Thu', label: 'Thu', dateStr: 'Oct 9' },
  { key: 'Fri', label: 'Fri', dateStr: 'Oct 10' },
];

const HOURS = ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00'];

const TODAY = new Date().toISOString().split('T')[0];
// Výstup: "2026-10-01"

const now = new Date();
const dayOfWeek = now.getDay(); // 0 = neděle, 1 = pondělí, ...

// V ČR začíná týden pondělím (index 1)
const distanceToMonday = dayOfWeek === 0 ? -6 : 1 - dayOfWeek;
const monday = new Date(now);
monday.setDate(now.getDate() + distanceToMonday);

const sunday = new Date(monday);
sunday.setDate(monday.getDate() + 6);

console.log(TODAY, monday, sunday);
const WEEKSTART = monday;
const WEEKEND = sunday;

// query - datum dnes - dnesni tyden - omezi to na 7 dnu; zavola to ID candidate a



interface Slot {
  day: string;
  hour: string;
  type: 'best' | 'available';
  label: string;
}

// Generovaná volná místa pro ukázku
const MOCK_SLOTS: Slot[] = [
  { day: 'Tue', hour: '09:00', type: 'best', label: 'Best Overlap' },
  { day: 'Tue', hour: '10:00', type: 'best', label: 'Best Overlap' },
  { day: 'Wed', hour: '11:00', type: 'available', label: 'Available' },
  { day: 'Thu', hour: '14:00', type: 'available', label: 'Available' },
  { day: 'Fri', hour: '09:00', type: 'available', label: 'Available' },
];

export default function SchedulingPage() {
  const [candidate, setCandidate] = useState([]);
  const [interviewer, setInterviewer] = useState([]);
  const [duration, setDuration] = useState('60 min');
  
  const [hasSearched, setHasSearched] = useState(false);
  const [selectedSlot, setSelectedSlot] = useState<{ dayLabel: string; dateStr: string; hour: string } | null>(null);
  const [booked, setBooked] = useState(false);



  // my functions from UsersPage
    const [persons, setPersons] = useState([]);


    const fetchPersons = () => {
        fetch(`${API_URL}/api/v1/persons/`)
        .then((res) => res.json())
        .then((data) => setPersons(data))
        .catch((err) => console.error('Error fetching data:', err));
    }

    useEffect(() => {
        fetchPersons();
    }, []);
  // end my functions from UsersPage

  const handleFindSlots = () => {
    setHasSearched(true);
    setSelectedSlot(null);
    setBooked(false);
  };

  const handleSelectSlot = (dayLabel: string, dateStr: string, hour: string) => {
    setSelectedSlot({ dayLabel, dateStr, hour });
    setBooked(false);
  };

  const handleConfirmBook = () => {
    setBooked(true);
  };

  const getSlot = (dayKey: string, hour: string) => {
    if (!hasSearched) return null;
    return MOCK_SLOTS.find((s) => s.day === dayKey && s.hour === hour);
  };

  //const currentCandidate = persons.find((c) => c.person_type === 'candidate')?.name;
  const candidateNames = persons
  .filter((c) => c.person_type === 'candidate')
  .map((c) => c);
  const interviewerNames = persons.filter((i) => i.person_type === 'interviewer').map((i) => i)

  return (
    <div style={styles.container}>
      
      {/* Hlavní box podle vašeho wireframu */}
      <div style={styles.card}>
        
        {/* Hlavička */}
        <div style={styles.header}>
          Schedule Interview
        </div>

        {/* Tělo - Rozděleno na Levý panel (Lidé) a Pravý panel (Kalendář) */}
        <div style={styles.body}>
          
          {/* LEVÝ PANEL - Formulář */}
          <div style={styles.sidebar}>
            
            <div>
              <label style={styles.label}>Candidate</label>
              <select 
                value={candidate} 
                onChange={(e) => setCandidate(e.target.value)}
                style={styles.select}
              >
                {candidateNames.map((c) => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
            </div>

            <div>
              <label style={styles.label}>Interviewer</label>
              <select 
                value={interviewer} 
                onChange={(e) => setInterviewer(e.target.value)}
                style={styles.select}
              >
                {interviewerNames.map((i) => (
                  <option key={i.id} value={i.id}>{i.name}</option>
                ))}
              </select>
            </div>

            <div>
              <label style={styles.label}>Duration</label>
              <select 
                value={duration} 
                onChange={(e) => setDuration(e.target.value)}
                style={styles.select}
              >
                <option value="60 min">60 min</option> 
              </select>
            </div>

            <button 
              onClick={handleFindSlots}
              style={styles.findBtn}
            >
              [Find Slots]
            </button>
          </div>

          {/* PRAVÝ PANEL - Scheduler */}
          <div style={styles.content}>
            <AvailabilityCalendar/>
            
          </div>
        </div>

        {/* SPODNÍ PANEL - Potvrzení slotu */}
        {selectedSlot && (
          <div style={styles.footer}>
            <div style={styles.footerText}>
              <strong>Selected:</strong> {selectedSlot.dateStr}, {selectedSlot.hour}
              <span style={styles.footerSubText}>
                ({currentCandidate} & {currentInterviewer})
              </span>
            </div>
            <button 
              onClick={handleConfirmBook}
              style={styles.confirmBtn}
            >
              [Confirm & Book]
            </button>
          </div>
        )}
      </div>

      {/* Oznámení o rezervaci */}
      {booked && selectedSlot && (
        <div style={styles.alert}>
          <strong>Úspěšně zamluveno!</strong> Pohovor pro {currentCandidate} s {currentInterviewer} byl naplánován na {selectedSlot.dateStr} v {selectedSlot.hour}.
        </div>
      )}
    </div>
  );
}

// STYLY POD KOMPONENTOU
const styles: Record<string, React.CSSProperties> = {
  container: {
    padding: '20px',
    maxWidth: '100%',
    margin: '0 auto',
    fontFamily: 'sans-serif',
  },
  card: {
    border: '2px solid #333',
    borderRadius: '8px',
    overflow: 'hidden',
    background: 'transparent',
  },
  header: {
    borderBottom: '2px solid #333',
    padding: '14px',
    textAlign: 'center',
    fontSize: '20px',
    fontWeight: 'bold',
    background: 'transparent',
  },
  body: {
    display: 'flex',
    minHeight: '420px',
  },
  sidebar: {
    width: '260px',
    borderRight: '2px solid #333',
    padding: '20px',
    display: 'flex',
    flexDirection: 'column',
    gap: '18px',
    background: 'transparent',
  },
  label: {
    display: 'block',
    fontWeight: 'bold',
    marginBottom: '6px',
  },
  select: {
    width: '100%',
    padding: '8px',
    borderRadius: '4px',
    border: '1px solid #ccc',
    fontSize: '14px',
  },
  findBtn: {
    marginTop: 'auto',
    padding: '10px',
    background: '#0d6efd',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontWeight: 'bold',
    fontSize: '15px',
  },
  content: {
    flex: 1,
    padding: '20px',
    display: 'flex',
    flexDirection: 'column',
  },
  title: {
    textAlign: 'center',
    fontWeight: 'bold',
    letterSpacing: '2px',
    marginBottom: '15px',
    color: '#555',
  },
  emptyState: {
    flex: 1,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    color: '#777',
    border: '2px dashed #ddd',
    borderRadius: '6px',
    padding: '20px',
    textAlign: 'center',
  },
  tableWrapper: {
    overflowX: 'auto',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    textAlign: 'center',
  },
  thTime: {
    width: '60px',
    padding: '8px',
  },
  thDay: {
    padding: '8px',
    fontWeight: 'bold',
  },
  tdTime: {
    padding: '8px',
    fontSize: '12px',
    color: '#666',
    fontWeight: 'bold',
  },
  tdCell: {
    border: '1px solid #e0e0e0',
    height: '50px',
    padding: '4px',
  },
  slotBadge: {
    borderRadius: '4px',
    padding: '4px',
    fontSize: '11px',
    fontWeight: 'bold',
  },
  footer: {
    borderTop: '2px solid #333',
    padding: '14px 20px',
    background: '#f8f9fa',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  footerText: {
    fontSize: '15px',
  },
  footerSubText: {
    color: '#666',
    marginLeft: '10px',
    fontSize: '13px',
  },
  confirmBtn: {
    padding: '8px 18px',
    background: '#198754',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    fontWeight: 'bold',
    cursor: 'pointer',
  },
  alert: {
    marginTop: '15px',
    padding: '12px 16px',
    background: '#d1e7dd',
    color: '#0f5132',
    border: '1px solid #badbcc',
    borderRadius: '6px',
  },
};