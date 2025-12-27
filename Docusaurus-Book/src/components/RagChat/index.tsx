import React, { useState } from 'react';
import { ChatState, Message } from './types';
import ChatSource from './Source';
import './RagChat.css';

const RagChat = () => {
  const [chatState, setChatState] = useState<ChatState>({
    messages: [],
    sources: [],
    isLoading: false,
    error: null,
  });
  const [input, setInput] = useState('');

  const handleSend = async () => {
    if (input.trim() !== '') {
      const newMessages: Message[] = [...chatState.messages, { type: 'user', text: input }];
      setChatState({ ...chatState, messages: newMessages, isLoading: true, error: null });
      setInput('');

      try {
        const response = await fetch('http://localhost:8000/ask', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ question: input }),
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        const botMessage: Message = { type: 'bot', text: data.answer };
        setChatState((prevState) => ({
          ...prevState,
          messages: [...prevState.messages, botMessage],
          sources: data.sources || [],
          isLoading: false,
        }));
      } catch (error) {
        setChatState((prevState) => ({
          ...prevState,
          error: 'Failed to get an answer.',
          isLoading: false,
        }));
      }
    }
  };

  return (
    <div className="rag-chat-widget">
      <div className="chat-window">
        <div className="messages">
          {chatState.messages.map((msg, index) => (
            <div key={index} className={`message ${msg.type}`}>
              {msg.text}
            </div>
          ))}
          {chatState.isLoading && <div className="message bot">Loading...</div>}
          {chatState.error && <div className="message error">{chatState.error}</div>}
          {chatState.sources.length > 0 && !chatState.isLoading && (
            <div className="sources">
              <h3>Sources:</h3>
              {chatState.sources.map((source, index) => (
                <ChatSource key={index} source={source} />
              ))}
            </div>
          )}
        </div>
        <div className="input-area">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask a question..."
          />
          <button onClick={handleSend}>Send</button>
        </div>
      </div>
    </div>
  );
};

export default RagChat;
