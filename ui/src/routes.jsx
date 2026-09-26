import { Routes, Route } from 'react-router-dom';
import PersonsPage from './pages/UsersPage';
import AvailabilityPage from './pages/AvailabilityPage';

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<h1>App is running</h1>} />
      <Route path="/persons" element={<PersonsPage />} />
      <Route path="/Credits" element={<CreditsPage />} />
    </Routes>
  );
}