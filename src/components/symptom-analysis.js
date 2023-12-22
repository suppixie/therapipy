const natural = require('natural');
const { adhdDataset, counselingStrategies } = require('./dataset.js');

const classifier = new natural.BayesClassifier();

adhdDataset.forEach((phrase) => {
  classifier.addDocument(phrase, 'ADHD');
});

counselingStrategies.forEach((phrase) => {
  classifier.addDocument(phrase, 'Counseling');
});

classifier.train();

function analyzeADHDSymptoms(userMessage) {
  const classification = classifier.getClassifications(userMessage);
  const topClassification = classification[0]; // Get the top classification

  // Logic to analyze ADHD symptoms based on classifier results
  let botResponse;

  if (topClassification.label === 'ADHD' && topClassification.value > -0.5) {
    botResponse = 'It seems like you are experiencing symptoms related to ADHD. How can I assist you further?';
  } else if (topClassification.label === 'ADHD' && topClassification.value <= -0.5) {
    botResponse = 'I understand, ADHD symptoms can be challenging. Would you like to learn some coping strategies?';
  } else {
    // Handle other scenarios or default response
    botResponse = null; // Indicates no specific response was generated
  }

  return botResponse;
}

module.exports = analyzeADHDSymptoms;
