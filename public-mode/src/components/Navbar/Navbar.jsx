import { NavLink } from 'react-router-dom';
import { Scale } from 'lucide-react';
import './Navbar.css';

const navItems = [
  { path: '/', label: 'Home' },
  { path: '/ask-ai', label: 'Ask AI' },
  { path: '/rights', label: 'Rights' },
  { path: '/complaint', label: 'Complaint' },
  { path: '/laws', label: 'Laws' },
  { path: '/services', label: 'Services' }
];

function Navbar() {
  return (
    <header className="navbar">
      {/* TODO: Add mobile drawer navigation and user language selector. */}
      <div className="container navbar__content">
        <NavLink className="navbar__brand" to="/">
          <Scale size={20} />
          <span>LegalMind AI</span>
        </NavLink>
        <nav className="navbar__links" aria-label="Primary navigation">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                isActive ? 'navbar__link navbar__link--active' : 'navbar__link'
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </div>
    </header>
  );
}

export default Navbar;
