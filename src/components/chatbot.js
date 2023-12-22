import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import '../styles/chatbot.css';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef(null);

  const handleUserInput = async () => {
    if (inputMessage.trim() !== '') {
      setMessages([...messages, { text: inputMessage, sender: 'user' }]);

      try {
        const response = await axios.post('http://localhost:3001/process-message', {
          message: inputMessage
        });

        const botResponse = response.data.botResponse;
        setMessages([
          ...messages,
          { text: botResponse, sender: 'bot' }
        ]);
      } catch (error) {
        console.error('Error sending message to server:', error);
      }

      setInputMessage('');
    }
  };

  const handleInputChange = (e) => {
    setInputMessage(e.target.value);
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  return (
    <div className="App">
      <h1>ADHD Counseling Chatbot</h1>
      <div className="chat-window">
        <div className="messages">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.sender === 'user' ? 'user' : 'bot'}`}
            >
              {message.text}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleUserInput();
          }}
        >
          <input
            type="text"
            value={inputMessage}
            onChange={handleInputChange}
            placeholder="Type a message..."
          />
          <button type="submit">Send</button>
        </form>
      </div>
    </div>
  );
};

export default Chatbot;
