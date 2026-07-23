import { motion } from 'framer-motion';
import './Loader.css';

function Loader() {
  return (
    <div className="loader" role="status" aria-live="polite" aria-label="Loading">
      {/* TODO: Reuse this loader for async route/page states and AI response fetching states. */}
      <motion.div
        className="loader__dot"
        animate={{ rotate: 360 }}
        transition={{ repeat: Infinity, ease: 'linear', duration: 1 }}
      />
      <span>Loading...</span>
    </div>
  );
}

export default Loader;
