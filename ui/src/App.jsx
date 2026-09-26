import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import PersonsPage from './pages/UsersPage';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import CreditsPage from './pages/CreditsPage';

export default function App() {
  return (
     <BrowserRouter>
      {/* Routes Definition */}
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/persons" element={<PersonsPage />} />
          <Route path="/Credits" element={<CreditsPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

