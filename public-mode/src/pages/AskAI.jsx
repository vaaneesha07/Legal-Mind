import ChatBox from '../components/ChatBox/ChatBox';

function AskAI() {
  return (
    <section className="container page-section">
      {/* TODO: Add guided AI prompts for legal FAQs, emergency help, and legal workflow assistance. */}
      <h1>Ask AI</h1>
      <p className="page-intro">Get step-by-step legal guidance in simple language.</p>
      <ChatBox />
    </section>
  );
}

export default AskAI;
