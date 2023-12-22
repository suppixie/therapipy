const natural = require('natural');
const { conversationalPhrases } = require('./dataset.js');

const classifier = new natural.BayesClassifier();

conversationalPhrases.forEach((phrase) => {
  classifier.addDocument(phrase, 'GREETINGS');
});

classifier.train();

function classifyUserMessage(userMessage) {
  const classification = classifier.getClassifications(userMessage);
  const topClassification = classification[0]; // Get the top classification

  // Determine the appropriate response based on classification
  let botResponse;

  if (topClassification.label === 'GREETINGS' && topClassification.value > -0.5) {
    botResponse = 'How are you feeling today?';
  } else {
    botResponse = 'Thank you for sharing. Is there anything else you would like to discuss?';
  }

  return botResponse;
}

function startConversation(userMessage) {
  const greetingPhrases = ['hi', 'hello', 'hey']; // Specific greeting phrases

  // Check if user's message matches any of the greeting phrases
  if (greetingPhrases.includes(userMessage.toLowerCase())) {
    return 'Hi there! How are you feeling today?';
  } else {
    return 'How are you feeling today?';
  }
}

module.exports = {
  startConversation,
  classifyUserMessage
};
