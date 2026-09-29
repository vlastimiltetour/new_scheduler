import { Routes, Route } from 'react-router-dom';
import PersonsPage from './pages/UsersPage';
import CreditsPage from './pages/CreditsPage';
import AvailabilityPage from './pages/AvailabilityPage';
import HomePage from './pages/HomePage';
import Layout from './components/Layout';


export const routesConfig = [
    {
        path: '/',
        label: 'Home',
        element: <HomePage />,
    },
    {
        path: '/persons',
        label: 'Users',
        element: <PersonsPage />,
    },
    {
        path: '/availability',
        label: 'Scheduling',
        element: <AvailabilityPage />,
    },
    {
        path: '/credits',
        label: 'Credits',
        element: <CreditsPage />,
    },
   {
    path: 'http://130.61.94.72:8088',
    label: 'Monitoring',
      element: (
        <button 
          onClick={() => window.location.href = 'http://130.61.94.72:8088'}
          style={{ display: 'none' }} 
          ref={(node) => node && window.location.replace('http://130.61.94.72:8088')}
        />
      ),
  },
    
]

export default function AppRoutes() {
  return (
    <Routes>
        <Route element={<Layout />}>
      {routesConfig
      .filter((route) => route.path !== "/")
      .map((route) => (
        <Route key={route.path} path={route.path} element={route.element} />
        
      ))}
        </Route>
    </Routes>
  );
}