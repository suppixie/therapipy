from flask import Flask, request, jsonify
from sentiment_cluster_tag import chatbot_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/process": {"origins": "*"}}) 

@app.route('/process', methods=['POST'])
def process():
    try:
        req_data = request.get_json()
        user_input = req_data['message']
        
        # Get the chatbot response from sentimen_cluster.py
        bot_response = chatbot_response(user_input)

        return jsonify({"chatbot_response": bot_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
