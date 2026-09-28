import { Routes, Route } from 'react-router-dom';
import PersonsPage from './pages/UsersPage';
import CreditsPage from './pages/CreditsPage';
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
        path: '/credits',
        label: 'Credits',
        element: <CreditsPage />,
    }
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