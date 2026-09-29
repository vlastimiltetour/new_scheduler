'use client';
import React, { useEffect, useState } from 'react';
// import { Calendar, momentLocalizer } from 'react-big-calendar';
// import moment from 'moment';
// import 'react-big-calendar/lib/css/react-big-calendar.css';


export default function AvailabilityPage() {

  const [availability, setAvailability] = useState([]);
  const [persons, setPersons] = useState([]);

  const fetchAvailability = () => {
      fetch('http://localhost:8080/api/v1/persons/')
        .then((res) => res.json())
        .then((data) => setPersons(data))
        .catch((err) => console.error('Error fetching data:', err));
    }
  
    useEffect(() => {
      fetchAvailability();
    }, []);
    

    // 1. Initialize moment localizer
    const localizer = momentLocalizer(moment);

    const interviewers = [
    { id: 'a', title: 'Sarah (Eng Lead)' },
    { id: 'b', title: 'Alex (Product)' },
    ];

    const events = [
    {
        title: 'Busy - Interview',
        start: new Date(2026, 7, 20, 10, 0),
        end: new Date(2026, 7, 20, 11, 0),
        resourceId: 'a',
    },
    ];


    return (
        <div style={{ height: '600px', padding: '20px' }}>
        <Calendar
            localizer={localizer}
            events={events}
            resources={interviewers}
            resourceIdAccessor="id"
            resourceTitleAccessor="title"
            defaultView="day"
            defaultDate={new Date(2026, 7, 20)}
            style={{ height: '100%' }}
        />
        </div>
    );
}
