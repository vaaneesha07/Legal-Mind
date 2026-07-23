import { BrowserRouter } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
import Footer from './components/Footer/Footer';
import AppRoutes from './routes';

function App() {
  return (
    <BrowserRouter>
      {/* TODO: Add global providers (auth, theme, i18n) when app-wide state is introduced. */}
      <div className="app-shell">
        <Navbar />
        <main className="app-main">
          <AppRoutes />
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;
