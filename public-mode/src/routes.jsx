import { useRoutes } from 'react-router-dom';
import Home from './pages/Home';
import AskAI from './pages/AskAI';
import Rights from './pages/Rights';
import Complaint from './pages/Complaint';
import Laws from './pages/Laws';
import Services from './pages/Services';
import NotFound from './pages/NotFound';

export const appRoutes = [
  { path: '/', element: <Home /> },
  { path: '/ask-ai', element: <AskAI /> },
  { path: '/rights', element: <Rights /> },
  { path: '/complaint', element: <Complaint /> },
  { path: '/laws', element: <Laws /> },
  { path: '/services', element: <Services /> },
  { path: '*', element: <NotFound /> }
];

function AppRoutes() {
  // TODO: Add route guards and lazy-loading strategy when protected/public route rules are finalized.
  return useRoutes(appRoutes);
}

export default AppRoutes;
