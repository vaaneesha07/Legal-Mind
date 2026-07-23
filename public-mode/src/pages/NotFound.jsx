import { Link } from 'react-router-dom';

function NotFound() {
  return (
    <section className="container page-section not-found">
      {/* TODO: Add helpful recovery links based on common navigation failures and user context. */}
      <h1>404</h1>
      <p className="page-intro">The page you are looking for does not exist.</p>
      <Link className="button-link" to="/">
        Go back home
      </Link>
    </section>
  );
}

export default NotFound;
