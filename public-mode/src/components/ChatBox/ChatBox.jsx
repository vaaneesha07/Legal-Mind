import { MessageSquare } from 'lucide-react';
import './ChatBox.css';

function ChatBox() {
  return (
    <section className="chat-box">
      {/* TODO: Integrate conversational AI messages, prompts, and citation cards. */}
      <header className="chat-box__header">
        <MessageSquare size={18} />
        <h2>Ask LegalMind AI</h2>
      </header>
      <div className="chat-box__body">AI chat interface placeholder for future implementation.</div>
    </section>
  );
}

export default ChatBox;
