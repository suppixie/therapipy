import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sampledata import sample_data

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text):
    words = nltk.word_tokenize(text.lower())
    words = [word for word in words if word.isalnum()]
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(words)

def preprocess_sample_data():
    processed_sample_data = [preprocess_text(text) for text in sample_data]
    return processed_sample_data

if __name__ == "__main__":
    processed_sample_data = preprocess_sample_data()
    with open('processed_sample_data.txt', 'w') as file:
        for data in processed_sample_data:
            file.write(data + '\n')
