const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { startConversation, classifyUserMessage } = require('./components/greeting.js');
const analyzeADHDSymptoms = require('./components/symptom-analysis.js');

const app = express();
const PORT = 3001;
const { adhdDataset, counselingStrategies } = require('./components/dataset.js');

// Natural language classifier setup
const natural = require('natural');
const classifier = new natural.BayesClassifier();

adhdDataset.forEach((phrase) => {
  classifier.addDocument(phrase, 'ADHD');
});

counselingStrategies.forEach((phrase) => {
  classifier.addDocument(phrase, 'Counseling');
});

classifier.train();

// Middleware setup
app.use(bodyParser.json());
const corsOptions = {
  origin: 'http://localhost:3000',
  methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
  credentials: true,
  optionsSuccessStatus: 204
};
app.use(cors(corsOptions));
app.options('*', cors(corsOptions));

// Endpoint to handle user messages
app.post('/process-message', (req, res) => {
  const userMessage = req.body.message;
  let botResponse;

  if (!req.body.message) {
    startConversation(); // Greet the user with initial conversation messages
  } else {
    botResponse = analyzeADHDSymptoms(userMessage);
  }

  if (!botResponse) {
    botResponse = classifyUserMessage(userMessage);
  }

  res.json({ botResponse });
});

// Root endpoint
app.get('/', (req, res) => {
  res.send('Welcome to the ADHD Counseling Chatbot Server');
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
