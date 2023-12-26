import nltk
import random
# import time
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.cluster import KMeans
from sampledata import sample_data
import os
os.environ["LOKY_MAX_CPU_COUNT"] = "2"

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

# def additional_clustering(user_input):
#     stress_keywords = ["stressed", "can't focus", "distracted", "anxious"]
#     found_keyword = None
#     for keyword in stress_keywords:
#         if keyword in user_input.lower():
#             found_keyword = keyword
#             break

#     if found_keyword:
#         if found_keyword == "stressed":
#             return "It seems like you're feeling stressed. Let's try to find ways to manage stress."
#         elif found_keyword == "can't focus":
#             return "If you're having trouble focusing, let's explore techniques to improve your concentration."
#         elif found_keyword == "distracted":
#             return "Feeling distracted can affect productivity. Let's discuss methods to enhance focus."
#         elif found_keyword == "anxious":
#             return "If you're feeling anxious, let's find ways to help you feel more at ease."
#     else:
#         return None
def detect_greeting(user_input):
    greetings = ["hi", "hello", "hey", "howdy", "hi there", "hello there"]
    return any(greeting in user_input.lower() for greeting in greetings)

# def guided_counseling(user_input, sample_data):
#     adhd_keywords = ["adhd", "attention deficit hyperactivity disorder", "hyperactive", "impulsive", "inattentive", "distractible"]

#     specific_responses = {
#         "stressed": "It seems like you're feeling stressed. Let's try to find ways to manage stress.",
#         "distracted": "If you're feeling distracted, let's explore techniques to improve focus.",
#         "confused": "Feeling confused can be challenging. Let's discuss to clear things up.",
#         "anxious": "If you're feeling anxious, let's find ways to help you feel more at ease."
#     }

#     for sample_text in sample_data:
#         if any(keyword in user_input.lower() for keyword in adhd_keywords):
#             return "It seems you might have symptoms for ADHD. Let's discuss further about it."

#     for word, response in specific_responses.items():
#         if word in user_input.lower():
#             return response
    
#     sentiment_score = analyze_sentiment(user_input)
#     emotion_labels = assign_emotion_labels([sentiment_score])
    
def additional_clustering(user_input):
    keywords = [
        "stressed", "distracted", "anxious",
        "impulsive", "restless", "forgetful",
        "hyperactive"
    ]
    found_keyword = None
    for keyword in keywords:
        if keyword in user_input.lower():
            found_keyword = keyword
            break

    if found_keyword:
        if found_keyword == "stressed":
            stress_advice = [
                "Identifying Triggers:\nLet's take a moment to identify the specific triggers contributing to your stress. Is it the feeling of being overwhelmed by tasks or challenges in staying organized? Pinpointing these triggers helps in finding targeted solutions.",
                "Organizational Strategies:\nImplementing organizational strategies can significantly alleviate stress. Techniques like breaking tasks into smaller, manageable parts, creating schedules, and using reminder apps or planners can bring structure to your routine.",
                "Stress Management Techniques:\nStress management techniques such as deep breathing exercises, meditation, or mindfulness can be incredibly beneficial. These practices help in grounding yourself during overwhelming moments and provide mental clarity.",
                "Seeking Support:\nDon't hesitate to seek support from professionals or support groups specializing in ADHD. They offer valuable guidance, coping strategies, and a supportive community that understands what you're going through.",
                "Self-Compassion:\nIt's essential to be kind to yourself. Dealing with ADHD can be challenging, but remember, you're doing your best. Celebrate small victories and practice self-care to recharge yourself.",
                "Balanced Lifestyle:\nMaintaining a balanced lifestyle with regular exercise, a nutritious diet, and sufficient sleep positively impacts ADHD symptoms and aids in stress reduction.",
                "Professional Help:\nConsider consulting a therapist or counselor specializing in ADHD. They can offer tailored strategies and cognitive-behavioral therapy techniques to manage stress effectively.",
                "Patience and Persistence:\nManaging ADHD-related stress is a journey. It takes time, patience, and persistence. Be open to trying different techniques and approaches until you find what works best for you."
            ]
            return "It's completely understandable to feel stressed, especially when managing ADHD symptoms. Acknowledging this stress is a positive step towards managing it better.\n", random.choice(stress_advice)
            
        
        elif found_keyword == "distracted":
            distracted_advice = [
                "Identifying Distraction Triggers: Let's pinpoint the specific triggers contributing to your distraction. Is it the abundance of stimuli around you, difficulty in maintaining attention on tasks, or feeling overwhelmed by multiple thoughts? Understanding these triggers is crucial for finding effective coping strategies.",
                "Strategies to Improve Focus: Implementing strategies tailored to enhance focus can significantly help manage distraction. Techniques like breaking tasks into smaller, manageable chunks, setting clear priorities, and using visual aids or timers can bring structure to your daily routine.",
                "Environmental Organization: Creating an organized and conducive environment can aid in reducing distraction. Designating a quiet workspace, minimizing clutter, and reducing potential distractions can help create a focused atmosphere.",
                "Mindfulness and Grounding Techniques: Practicing mindfulness exercises, grounding techniques, or meditation can assist in regaining focus during moments of distraction. These practices help anchor your attention and bring awareness to the present moment.",
                "Use of Technology: Explore the use of technology to your advantage. Consider using apps or tools designed to aid focus and attention. Timer-based apps, task managers, or focus-oriented apps can assist in staying on track.",
                "Breaks and Rest: Recognize the importance of breaks. Taking short, structured breaks between tasks allows for mental rejuvenation and can enhance overall focus and productivity.",
                "Professional Guidance: Consider seeking support from specialists in ADHD. Professionals can provide personalized strategies, behavioral therapies, and cognitive techniques tailored to address your specific challenges with distraction.",
                "Patience and Self-Encouragement: Remember, managing distraction linked to ADHD is a gradual process. Be patient with yourself and acknowledge small achievements along the way. Encouraging self-talk and maintaining a positive mindset are key components of managing distraction effectively."
            ]
            return "It's completely understandable to feel distracted, particularly when dealing with ADHD symptoms. Acknowledging this distraction is an essential step towards addressing and managing it better.\n", random.choice(distracted_advice)

        elif found_keyword == "anxious":
            anxious_advice = [
                "Identifying Anxiety Triggers: Let's identify the specific triggers contributing to your anxiety. Is it the pressure of deadlines, fear of forgetting tasks, or feeling overwhelmed by responsibilities? Pinpointing these triggers is crucial in finding targeted solutions.",
                "Stress-Reducing Techniques: Implement stress-reducing techniques to alleviate anxiety. Practices like deep breathing exercises, progressive muscle relaxation, or guided imagery can help calm the mind and body during anxious moments.",
                "Structured Planning: Organize tasks systematically to reduce anxiety. Breaking tasks into smaller steps, setting achievable goals, and using planners or checklists can bring clarity and reduce anxiety about pending tasks.",
                "Mindfulness and Grounding Exercises: Incorporating mindfulness practices or grounding exercises helps anchor your focus to the present moment, reducing anxiety caused by racing thoughts or worries about the future.",
                "Establishing a Support System: Don't hesitate to reach out for support. Engage with trusted friends, family members, or support groups. Sharing concerns and seeking advice from a supportive network can alleviate feelings of anxiety.",
                "Professional Assistance: Consider seeking guidance from mental health professionals specializing in ADHD and anxiety. Therapists can provide cognitive-behavioral strategies and coping mechanisms tailored to manage anxiety effectively.",
                "Self-Care and Relaxation: Prioritize self-care activities to reduce anxiety levels. Engage in activities you enjoy, practice relaxation techniques, and ensure adequate rest to rejuvenate both mentally and physically.",
                "Mindset Shift: Practice positive self-talk and affirmations. Replace negative thoughts with positive ones to build resilience against anxiety and foster a more optimistic outlook."
            ]
            return "It's common to experience anxiety, especially in managing ADHD symptoms. Acknowledging this anxiety is an important step towards addressing and managing it better.\n", random.choice(anxious_advice)
        
        elif found_keyword == "impulsive":
            impulsive_advice = [
                "Pause and Reflect: When you feel impulsive, take a moment to pause before acting. Reflect on the potential outcomes of your actions to make more informed decisions.",
                "Strategic Planning: Incorporate structured planning techniques to minimize impulsive behavior. Creating to-do lists, setting priorities, and allocating specific time for tasks can curb impulsivity.",
                "Mindfulness Practices: Practice mindfulness exercises to improve self-awareness. Techniques like deep breathing or meditation can help in managing impulsive urges by fostering a sense of calm and control.",
                "Delayed Gratification: Embrace the concept of delayed gratification. Train yourself to delay immediate impulses by setting goals and rewarding yourself after completing tasks or reaching milestones.",
                "Seeking Support: Engage with support groups or seek guidance from professionals specializing in ADHD. They can offer coping strategies and behavioral interventions tailored to manage impulsivity.",
                "Positive Reinforcement: Reward yourself for practicing control over impulsive behaviors. Celebrate small victories and progress made towards managing impulsivity.",
                "Healthy Distractions: Engage in activities that redirect impulsive tendencies positively, such as hobbies, creative pursuits, or physical exercises.",
                "Social Strategies: Use social cues and strategies to manage impulsivity in social situations. Practice active listening, take breaks during conversations, and use relaxation techniques to ease impulsivity.",
                "Environment Management: Create an environment that minimizes impulsivity triggers. Organize your space, reduce clutter, and establish a calming atmosphere to mitigate impulsive behaviors.",
                "Develop Routine: Establishing a structured routine helps in managing impulsivity. Stick to a consistent schedule for tasks, activities, and breaks to regulate impulsive tendencies.",
                "Recognize Patterns: Identify patterns and situations triggering impulsivity. Understanding the triggers helps in developing personalized strategies to manage impulsive behaviors."
            ]
            return "Recognize that impulsivity is a common challenge in ADHD. Acknowledging this impulsivity is the first step towards managing it better.\n", random.choice(impulsive_advice)
        
        elif found_keyword == "forgetful":
            forgetful_advice = [
                "Memory Techniques: Practice memory improvement techniques such as visual association, mnemonic devices, or creating mind maps to aid in remembering information.",
                "Use Reminders: Utilize reminder apps, sticky notes, or alarms to prompt and remember tasks or important information.",
                "Organize Information: Organize information in a structured manner. Use lists, calendars, or digital organizers to keep track of schedules, appointments, and tasks.",
                "Focus and Attention: Enhance focus and attention to minimize forgetfulness. Implement concentration techniques like mindfulness, deep breathing, or meditation.",
                "Reduce Distractions: Minimize distractions in your environment to improve memory retention. Create a conducive space for better focus and reduced forgetfulness.",
                "Healthy Lifestyle: Maintain a healthy lifestyle with adequate sleep, regular exercise, and a balanced diet. Physical health positively impacts memory and cognitive functions.",
                "Break Tasks: Break down tasks into smaller, manageable parts. This approach reduces overwhelm and makes it easier to remember and complete tasks.",
                "Repeat and Review: Practice repetition and review of important information. Revisiting and reinforcing details helps in better retention and recall.",
                "Mindfulness Practices: Incorporate mindfulness practices in your routine to improve attention and memory. Engage in mindful activities that promote mental clarity and focus."
            ]
            return "Forgetfulness can be challenging, especially when managing ADHD symptoms. Acknowledging this forgetfulness is the first step towards addressing and managing it better.\n", random.choice(forgetful_advice)
        
        elif found_keyword == "hyperactive":
            hyperactive_advice = [
                "Physical Activity: Engaging in regular physical exercise can help channel excessive energy. Consider activities like jogging, cycling, or yoga to release pent-up energy.",
                "Structured Routine: Establish a structured routine to regulate hyperactivity. Follow a schedule for tasks, breaks, meals, and bedtime to create a sense of order and stability.",
                "Mindfulness Practices: Incorporate mindfulness and relaxation techniques to calm the mind and reduce hyperactivity. Try deep breathing, meditation, or progressive muscle relaxation.",
                "Fidget Tools: Use fidget toys or gadgets as a physical outlet to channel restless energy. These tools can provide sensory stimulation and aid in managing hyperactivity.",
                "Limit Stimulants: Reduce intake of stimulants like caffeine or sugar as they can exacerbate hyperactivity. Opt for a balanced diet and adequate hydration for better focus.",
                "Quiet Time: Allocate periods for quiet activities to calm hyperactivity. Reading, drawing, or listening to calming music can help redirect excessive energy.",
                "Positive Outlets: Encourage involvement in constructive activities or hobbies to redirect hyperactive behavior positively. Creative endeavors or hobbies offer a healthy outlet for energy.",
                "Support Networks: Connect with support groups or therapists specializing in ADHD. They offer guidance, coping strategies, and understanding in managing hyperactivity."
            ]
            return "Feeling hyperactive is a common aspect of ADHD. Acknowledging this hyperactivity is a positive step towards managing it effectively.\n", random.choice(hyperactive_advice)
        
        elif found_keyword == "restless":
             restless_advice = [
                "I understand feeling restless can be challenging. Finding an outlet for your energy could help. Have you tried physical activities like running, walking, or yoga?",
                "Restlessness is common with ADHD. Consider engaging in calming activities such as meditation or deep breathing exercises to channel your energy positively.",
                "It's okay to feel restless at times. Have you explored activities that could provide a creative outlet? Drawing, writing, or crafting might help channel your energy productively.",
                "Feeling restless could be a sign of excess energy. How about incorporating a daily exercise routine to release some of that energy in a positive way?"]
        return random.choice(restless_advice)

    else:
        return None


def chatbot_response(user_input):
    response = ""

    if detect_greeting(user_input):
        response = "Hello! How can I assist you today?"
    elif len(user_input) < 30:
        response = "Please elaborate a bit more (min 2 lines)."
    else:
        processed_input = preprocess_text(user_input)
        sentiment_score = analyze_sentiment(processed_input)
        processed_sample_data = [preprocess_text(text) for text in sample_data]
        cluster_labels = perform_clustering(processed_sample_data)
        emotion_labels = assign_emotion_labels([sentiment_score])
        additional_cluster_response = additional_clustering(user_input)

        if additional_cluster_response:
            response = additional_cluster_response

    return response