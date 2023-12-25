import nltk
import random
import time
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.cluster import KMeans
from sampledata import sample_data

nltk.download('punkt')
nltk.download('vader_lexicon')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(user_input):
    words = nltk.word_tokenize(user_input.lower())
    words = [word for word in words if word.isalnum()]
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    preprocessed_text = ' '.join(words)
    return preprocessed_text

def analyze_sentiment(data):
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(data)['compound']
    return sentiment_score

def perform_clustering(preprocessed_data, num_clusters=3):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(preprocessed_data)
    kmeans = KMeans(n_clusters=num_clusters, n_init=10)
    kmeans.fit(X)
    cluster_labels = kmeans.labels_
    return cluster_labels.tolist()

def assign_emotion_labels(sentiment_scores):
    emotion_labels = []
    thresholds = [0.7, 0.5, 0.3, 0.1, -0.1, -0.3, -0.5, -0.7]
    emotion_categories = [
        "Very Positive Emotion",
        "Positive Emotion",
        "Fairly Positive Emotion",
        "Slightly Positive Emotion",
        "Neutral Emotion",
        "Slightly Negative Emotion",
        "Negative Emotion",
        "Fairly Negative Emotion",
        "Very Negative Emotion"
    ]
    for score in sentiment_scores:
        for i, threshold in enumerate(thresholds):
            if score >= threshold:
                emotion_labels.append(emotion_categories[i])
                break
    return emotion_labels

def detect_greeting(user_input):
    greetings = ["hi", "hello", "hey", "howdy", "hi there", "hello there"]
    return any(greeting in user_input.lower() for greeting in greetings)

def guided_counseling(user_input, sample_data):
    adhd_keywords = ["adhd", "attention deficit hyperactivity disorder", "hyperactive", "impulsive", "inattentive", "distractible"]

    specific_responses = {
        "stressed": "It seems like you're feeling stressed. Let's try to find ways to manage stress.",
        "distracted": "If you're feeling distracted, let's explore techniques to improve focus.",
        "confused": "Feeling confused can be challenging. Let's discuss to clear things up.",
        "anxious": "If you're feeling anxious, let's find ways to help you feel more at ease."
    }

    for sample_text in sample_data:
        if any(keyword in user_input.lower() for keyword in adhd_keywords):
            return "It seems your input is related to ADHD. Let's discuss further about it."

    for word, response in specific_responses.items():
        if word in user_input.lower():
            return response
    
    sentiment_score = analyze_sentiment(user_input)
    emotion_labels = assign_emotion_labels([sentiment_score])
    
    

while True:
    user_input = input("User: ")
    processed_input = preprocess_text(user_input)
    
    sentiment_score = analyze_sentiment(processed_input)
    print("Sentiment Score:", sentiment_score)
    
    processed_sample_data = [preprocess_text(text) for text in sample_data]
    cluster_labels = perform_clustering(processed_sample_data)
    
    emotion_labels = assign_emotion_labels([sentiment_score])
    print("Emotion Labels:", emotion_labels)
    
    response = guided_counseling(processed_input, sample_data)
    # print("Bot:", response)

    if detect_greeting(user_input):
        print( "Hello! How can I assist you further?")
    if "Positive Emotion" in emotion_labels:
        random_question = random.choice([
            "Have you watched any good movies lately?",
            "What's your favorite hobby?",
            "Do you follow any sports?",
            "I love traveling, do you?",
            "How's your day going?",
            "What have you been up to lately?",
            "Any plans for the weekend?",
            "Do you have any hobbies or interests?",
            "How do you cope with stress?",
            "Have you tried any relaxation techniques?",
            "Do you find it hard to focus sometimes?",
            "Do you have any tips for staying motivated?",
        ])
        print( f"Great to hear! {random_question}")

    if "Negative Emotion" in emotion_labels:
        print("Bot: You seem to be experiencing a negative emotion. What do you want to do?")
        print("1. Do you want to talk more about it?")
        print("2. I'm concerned, need my help?")
        print("3. Suggest me some activity?")
        
        user_choice = input("User: ")
        
        if user_choice == "1":
            print("Bot: Go on, I'm all ears.")
            # user_input = input("User: ") 
            # processed_input= preprocess_text(user_input)
            
        elif user_choice == "2":
            print("Bot: Are you seeking advice or help to manage your current feelings? (yes/no)")
            advice_help = input("User: ")
            
            if advice_help.lower() == "yes":
                advice_phrases = [
                    "Mindfulness exercises might help in improving focus and reducing impulsivity.",
                    "Setting structured routines and using planners can assist in better organization.",
                    "Break tasks into smaller, manageable parts to improve productivity",
                    "Practice relaxation techniques like deep breathing or meditation to alleviate stress",
                    "Cognitive-behavioral therapy (CBT) can assist in managing ADHD symptoms effectively",
                    "Using tools such as timers or alarms for better time management",
                    "Regular physical exercise and a balanced diet can positively impact ADHD symptoms",
                    "Seeking support from a counselor or support groups for guidance and advice"
                ]
                suggested_advice = random.choice(advice_phrases)
                print(f"Bot: {suggested_advice}")
                # user_input = input("User: ")  
                # processed_input= preprocess_text(user_input)   

            elif advice_help.lower() == "no":
                # user_input = input("User: ")  
                # processed_input= preprocess_text(user_input) 
                continue

            else:
                print("Bot: I didn't catch that. Let's continue.")
                # user_input = input("User: ")  
                # processed_input= preprocess_text(user_input)       

        elif user_choice == "3":
            print("Bot: Let's do a breathing exercise.")
            for _ in range(4):
                print("inhale and exhale")
                time.sleep(10)
            # user_input = input("User: ")  
            # processed_input= preprocess_text(user_input)     

        else:
            print("Bot: Your input is not recognized. How can I assist you?")
            # user_input = input("User: ")  
            # processed_input= preprocess_text(user_input)