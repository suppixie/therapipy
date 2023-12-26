import React, { useState } from 'react';
import axios from 'axios';
import "./styles/chatbot.css";

function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    const newMessages = [...messages];
    newMessages.push({ text: inputText, sender: 'user' });
    setMessages(newMessages);
    setInputText('');
  
    try {
      const response = await axios.post('http://localhost:5000/process', {
        message: inputText,
      }, {
        headers: {
          'Content-Type': 'application/json',
        }
      });
  
      const botResponse = response.data.chatbot_response;
  
      const updatedMessages = [...newMessages];
      updatedMessages.push({ text: botResponse, sender: 'bot' });
      setMessages(updatedMessages); 
    } catch (error) {
      console.error('Error fetching chatbot response:', error);
    }
  };

  return (
    <div className="chatbot-container">
      <h2>ADHD Counselling Chatbot</h2>
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Type a message..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

export default Chatbot;
