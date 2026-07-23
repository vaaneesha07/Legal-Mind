import { motion } from 'framer-motion';
import './Hero.css';

function Hero() {
  return (
    <section className="hero">
      {/* TODO: Replace static copy with CMS-driven public education messaging. */}
      <motion.div
        className="container hero__content"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <p className="hero__badge">Public Mode</p>
        <h1>Understand Indian law in simple language.</h1>
        <p>
          LegalMind AI helps citizens explore rights, legal procedures, and public services with
          confidence.
        </p>
      </motion.div>
    </section>
  );
}

export default Hero;
