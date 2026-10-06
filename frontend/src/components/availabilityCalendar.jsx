import React from 'react';
import { generateHourlySlots } from '../utils/slotGenerator';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';

export default function AvailabilityCalendar({ availabilityData, onSelectSlot }) {
  
  const personId = availabilityData?.[0]?.person_id; // "?" are safe to request the data if the value doesn't exists

  const baseDate = availabilityData && availabilityData.length > 0
    ? new Date(availabilityData[0].start)
    : new Date();

  const TODAY = new Date().toISOString().split('T')[0]; // TODO potrebuju to ?
  // Výstup: "2026-10-01"

  const now = new Date();
  const dayOfWeek = now.getDay(); // 0 = neděle, 1 = pondělí, ...

  // V ČR začíná týden pondělím (index 1)
  const distanceToMonday = dayOfWeek === 0 ? -6 : 1 - dayOfWeek;
  const monday = new Date(baseDate);
  monday.setDate(baseDate.getDate() + distanceToMonday);

  const sunday = new Date(monday);
  sunday.setDate(monday.getDate() + 6);

  console.log(TODAY, monday, sunday);
  const WEEKSTART = monday;
  const WEEKEND = sunday;

  // 1. Vygenerujeme 60minutové sloty z dat z backendu
  const hourlySlots = generateHourlySlots(availabilityData || []);

  // 2. Definice pracovních dnů (Pondělí až Pátek / Neděle)
  // Poznámka: Upravte data podle aktuálního týdne z vášho dotazu (2026-09-28 až 2026-10-04)
  const dayNames = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

  const days = Array.from({length: 7}, (_,i) => {
    const currentDate = new Date(monday);
    currentDate.setDate(monday.getDate() + i);
 
    const year = currentDate.getFullYear();
    const month = String(currentDate.getMonth() + 1).padStart(2, '0');
    const day = String(currentDate.getDate()).padStart(2, '0')
    
    
    return {
      name: dayNames[i],
      dateKey: `${year}-${month}-${day}`,
    };
    });

  // Hodiny na časové ose
    const [start, end] = [9, 19];

    const hours = Array.from(
    { length: end - start }, 
    (_, i) => `${String(start + i).padStart(2, '0')}:00`
    );

  // Pomocná funkce pro zjištění, zda je daná hodina v daný den dostupná
  const getSlotForCell = (dateKey, timeKey) => {
    return hourlySlots.find(
      (slot) => slot.dateKey === dateKey && slot.timeKey === timeKey
    );
  };

  const handleAddClick = async (dateKey, timeKey) => {
    console.log('Tohle je den a cas', dateKey, timeKey);

    const [h] = timeKey.split(":");
    const endHour = String(Number(h) + 1).padStart(2, '0');

    const payload = {
      personId: personId,
      slot_start: `${dateKey}T${timeKey}:00Z`,
      slot_end: `${dateKey}T${endHour}:00Z`,
    }

    const url = `${API_URL}/api/v1/persons/${payload.personId}/availabilities?start=${encodeURIComponent(payload.slot_start)}&end=${encodeURIComponent(payload.slot_end)}`;


      
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
        },
      }); // <-- Přidána zavírací závorka pro fetch

      if (!response.ok) {
        // Použity zpětné uvozovky ` ` pro interpolaci proměnné a opraveny překlepy
        throw new Error(`Response error ${response.status}`);
      }

      const result = await response.json(); // <-- Doplněna zavírací závorka ) a středník

      console.log('Slot úspěšně vytvořen:', result);

      
    } catch (error) {
      console.error('Chyba při uložení slotu:', error);
      alert('Nepodařilo se uložit slot.');
    }
    
    
    };

 return (
    <div className="availability-calendar-widget" style={styles.calendarContainer}>
      {/* Izolované CSS pravidla pouze pro tento widget */}
      <style>{`
        .availability-calendar-widget .cell-td .add-slot-btn {
          opacity: 0;
          visibility: hidden;
          transition: all 0.15s ease;
        }

        /* Při najetí myší na prázdnou buňku zviditelníme tlačítko */
        .availability-calendar-widget .cell-td:hover .add-slot-btn {
          opacity: 1;
          visibility: visible;
        }

        .availability-calendar-widget .add-slot-btn:hover {
          background-color: '#afafb0' !important;
          color: #ffffff !important;
          border-color: '#9ca3af' !important;
        }

        .availability-calendar-widget .available-slot-btn:hover {
          background-color: #34d399 !important;
          transform: scale(1.02);
          box-shadow: 0 0 8px rgba(52, 211, 153, 0.5);
        }
      `}</style>

      <table style={styles.table}>
        <thead>
          <tr>
            <th style={styles.th}>Time</th>
            {days.map((day) => (
              <th key={day.dateKey} style={styles.th}>
                {day.name} <br />
                <span style={styles.dateSubtext}>{day.dateKey.slice(5)}</span>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {hours.map((time) => (
            <tr key={time}>
              <td style={styles.timeTd}>{time}</td>
              {days.map((day) => {
                const slot = getSlotForCell(day.dateKey, time);

                return (
                  /* Přidána třída cell-td */
                  <td key={`${day.dateKey}_${time}`} className="cell-td" style={styles.cellTd}>
                    {slot ? (
                      /* Přidána třída available-slot-btn */
                      <button
                        className="available-slot-btn"
                        style={styles.availableSlotBtn}
                        onClick={() => onSelectSlot && onSelectSlot(slot)}
                        title={`Rezervovat ${slot.label}`}
                      >
                        {slot.label}
                      </button>
                    ) : (
                      
                      <button
                        className="add-slot-btn"
                        style={styles.addSlotBtn}
                        onClick={() => handleAddClick(day.dateKey, time)}
                      >
                        + Add slot
                      </button>
                      
                    )}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const styles = {
  calendarContainer: {
    overflowX: 'auto',
    marginTop: '16px',
    border: '1px solid #374151',
    borderRadius: '8px',
    backgroundColor: '#111827',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    textAlign: 'center',
    color: '#ffffff',
  },
  th: {
    padding: '12px',
    borderBottom: '1px solid #374151',
    backgroundColor: '#1f2937',
    fontWeight: '600',
  },
  dateSubtext: {
    fontSize: '11px',
    color: '#9ca3af',
    fontWeight: 'normal',
  },
  timeTd: {
    padding: '10px',
    borderRight: '1px solid #374151',
    borderBottom: '1px solid #374151',
    fontWeight: 'bold',
    backgroundColor: '#1f2937',
    fontSize: '13px',
  },
  cellTd: {
    padding: '6px',
    minWidth: '120px',
    borderRight: '1px solid #374151',
    borderBottom: '1px solid #374151',
    height: '48px',
    transition: 'background-color 0.15s ease' // Transition effect 
  },
  availableSlotBtn: {
    width: '100%',
    height: '100%',
    backgroundColor: '#10b981', // 
    color: '#ffffff',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontWeight: '600',
    fontSize: '12px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
    transition: 'all 0.15s ease', // Plynula animace 
  },
  disabledSlot: {
    color: '#4b5563',
    fontSize: '12px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100%',
    borderRadius: '6px',
    transition: 'background-color 0.15s ease',
  },
  addSlotBtn: {
    width: '100%',
    height: '100%',
    backgroundColor: 'transparent',
    color: '#9ca3af',
    border: '1px dashed #4b5563',
    borderRadius: '6px',
    cursor: 'pointer',
    fontWeight: '500',
    fontSize: '11px',
  },
};