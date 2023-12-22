import React, { useState, useEffect } from 'react';
import axios from 'axios'; // Make API requests
import '../styles/chatbot.css';

const Chatbot = () => {
  const [messages, setMessages] = useState([]); // Store chat history
  const [inputMessage, setInputMessage] = useState(''); // User input

  const sendMessage = async () => {
    if (inputMessage.trim() === '') return;

    // Add user's message to the chat history
    setMessages([...messages, { text: inputMessage, sender: 'user' }]);
    setInputMessage(''); // Clear input field

    try {
      // Make an API call to your backend with the user's message
      const response = await axios.post('YOUR_BACKEND_API_ENDPOINT', {
        message: inputMessage,
      });

      // Add the chatbot's response to the chat history
      setMessages([...messages, { text: response.data.message, sender: 'bot' }]);
    } catch (error) {
      console.error('Error sending message:', error);
      // Handle errors here
    }
  };

  // Handle input changes
  const handleInputChange = (event) => {
    setInputMessage(event.target.value);
  };

  // Function to handle sending message on Enter key press
  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <div className="chatbot-container">
        <div className='title'>
            <h1>Therapipy</h1>
        </div>
      <div className="chatbot-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <div className="chatbot-input">
        <input
          type="text"
          placeholder="Type your message..."
          value={inputMessage}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default Chatbot;
