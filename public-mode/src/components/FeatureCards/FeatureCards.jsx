import { motion } from 'framer-motion';
import { FileText, ShieldCheck, Scale } from 'lucide-react';
import './FeatureCards.css';

const features = [
  {
    title: 'Simplified Laws',
    description: 'Get easy-to-understand summaries of legal topics relevant to daily life.',
    icon: Scale
  },
  {
    title: 'Know Your Rights',
    description: 'Learn fundamental rights and protections available to every citizen.',
    icon: ShieldCheck
  },
  {
    title: 'Guided Complaints',
    description: 'Understand complaint pathways and required documents before filing.',
    icon: FileText
  }
];

function FeatureCards() {
  return (
    <section className="feature-cards">
      {/* TODO: Load feature modules dynamically based on user intent and language preference. */}
      <div className="container feature-cards__grid">
        {features.map((feature, index) => {
          const Icon = feature.icon;
          return (
            <motion.article
              key={feature.title}
              className="feature-card"
              initial={{ opacity: 0, y: 18 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.2 }}
              transition={{ duration: 0.4, delay: index * 0.1 }}
            >
              <Icon size={20} />
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </motion.article>
          );
        })}
      </div>
    </section>
  );
}

export default FeatureCards;
