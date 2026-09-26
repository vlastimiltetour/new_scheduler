import React from 'react';
import { Outlet } from 'react-router-dom';

export default function Layout() {
    return (
        <>
       
        <div
              style={{
                backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url('/bg.jpg')`,
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                backgroundRepeat: 'no-repeat',
                width: '100vw',
                minHeight: '100vh',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                gap: '24px'
              }}
            >
                <Outlet />
            </div>
        </>
    )
}; 

