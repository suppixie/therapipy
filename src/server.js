const express = require('express');
const bodyParser = require('body-parser');
const natural = require('natural');
const cors = require('cors');
const app = express();
const PORT = 3001;
const { adhdDataset, counselingStrategies } = require('./dataset.js');

const classifier = new natural.BayesClassifier();

adhdDataset.forEach((phrase) => {
  classifier.addDocument(phrase, 'ADHD');
});

counselingStrategies.forEach((phrase) => {
  classifier.addDocument(phrase, 'Counseling');
});

classifier.train();


// Middleware to parse JSON body
app.use(bodyParser.json());
const corsOptions = {
    origin: 'http://localhost:3000', // Replace with your frontend's URL
    methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
    credentials: true,
    optionsSuccessStatus: 204 // Set the preflight OPTIONS success status
  };
  app.use(cors(corsOptions));
  
  // Handle preflight request for all routes
  app.options('*', cors(corsOptions));

// Endpoint to handle user messages
app.post('/process-message', (req, res) => {
  const userMessage = req.body.message;

  // Function to classify user messages
  function classifyUserMessage(userMessage) {
    const classification = classifier.getClassifications(userMessage);
    const topClassification = classification[0]; // Get the top classification
    let botResponse;

    if (topClassification.label === 'ADHD' && topClassification.value > -0.5) {
      botResponse = 'It seems like you are experiencing symptoms related to ADHD. How can I assist you further?';
    } else if (topClassification.label === 'ADHD' && topClassification.value <= -0.5) {
      botResponse = 'I understand, ADHD symptoms can be challenging. Would you like to learn some coping strategies?';
    } else {
      botResponse = 'Thank you for sharing. Is there anything else you would like to discuss?';
    }

    return botResponse;
  }

  const botResponse = classifyUserMessage(userMessage);

  res.json({ botResponse });
});

// Route handler for GET requests at the root URL ('/')
app.get('/', (req, res) => {
  res.send('Welcome to the ADHD Counseling Chatbot Server');
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
