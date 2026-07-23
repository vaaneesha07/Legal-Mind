import './Footer.css';

function Footer() {
  return (
    <footer className="footer">
      {/* TODO: Add policy links, legal disclaimers, and multilingual contact channels. */}
      <div className="container footer__content">
        <p>© {new Date().getFullYear()} LegalMind AI · Public Mode</p>
      </div>
    </footer>
  );
}

export default Footer;
