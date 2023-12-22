const express = require('express');
const bodyParser = require('body-parser');
const natural = require('natural');
const cors = require('cors');
const app = express();
const PORT = 3001;

// Training the classifier with a small dataset
const classifier = new natural.BayesClassifier();
classifier.addDocument('I have trouble focusing.', 'ADHD');
classifier.addDocument('I feel restless and easily distracted.', 'ADHD');
classifier.addDocument('I find it hard to follow instructions.', 'ADHD');
classifier.addDocument('I often lose things and forget appointments.', 'ADHD');
classifier.addDocument('I struggle with time management.', 'ADHD');
classifier.train();

// Middleware to parse JSON body
app.use(bodyParser.json());
app.use(cors()); 



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
