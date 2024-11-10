import os
import json
import requests
from datetime import timedelta
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify, session
from config import Config
from dotenv import load_dotenv 

# Load environment variables
load_dotenv()
print("SECRET_KEY:", os.getenv('SECRET_KEY'))
print("GEMINI_API_KEY:", os.getenv('GEMINI_API_KEY'))

app = Flask(__name__)
app.config.from_object(Config)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Session expiry time

GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'
API_KEY = os.getenv("GEMINI_API_KEY")

# MongoDB connection setup
uri = "mongodb+srv://UserP:MGSdJSmOtRMJ33Er@cluster0.itxnkx2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['hotelmanagement']
collection = db['inventories']

# Helper function to initialize conversation history
def init_conversation_history():
    if 'conversation_history' not in session:
        session['conversation_history'] = []

def fetch_item_details(username):
    # print(f"Attempting to fetch data for username: {username}")
    
    # Query the MongoDB database to find the document matching the username
    user_data = collection.find_one({"username": username})
    
    if user_data is None:
        print("No data found for this username.")
        return False  # Username not found

    # print(f"User data fetched: {user_data}")

    # Check if 'itemdetails' exists in the user data
    if 'itemdetails' in user_data:
        print("Item details found.")
        # Store product data in the session for use in chat responses
        session['product_data'] = user_data['itemdetails']
        return True  # Indicate that product data was successfully fetched
    else:
        print("Item details not found for this username.")
        return False  # 'itemdetails' field not found in the data


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    username = request.json.get('username')  # Fetch the username from the request
    username = str(username)

    user_message = request.json.get('user_message')  # Fetch the username from the request
    user_message = str(user_message)

    
    init_conversation_history()  # Initialize conversation history if it's not already present
    
    # Fetch product data after username is provided
    if fetch_item_details(username):
        # Get product data from session
        product_data = session.get('product_data', [])
        # print(product_data)
        if not product_data:
            return jsonify({'reply': 'No product data available. Please check your inventory.'}), 400
        
        # Start conversation if not already done
        if len(session['conversation_history']) == 0:
            initial_instruction = f"""
            I will provide data in JSON format about my inventory: {product_data} & don't show numeric data in response just chat like a normal person providing suggestions on portion control and meal planning based on inventory including expiry dates in concise way. dont add numeric details regarding expiry dates in your answer and 
            """
            session['conversation_history'].append({"text": initial_instruction})
        else: 
            session['conversation_history'].append({"text": user_message})

        # print(f"Conversation history: {session['conversation_history']}")
        
        data={}

        if username == user_message:
            data = {
                "contents": [
                    {
                        "parts": session['conversation_history']
                    }
                ]
            }

        print(data)
        # Send the request to the Gemini API
        response = requests.post(
            f'{GEMINI_API_URL}?key={API_KEY}',
            headers={'Content-Type': 'application/json'},
            json=data
        )

        print(response)


        if response.status_code == 200:
            response_data = response.json()
            try:
                bot_reply = response_data['candidates'][0]['content']['parts'][0]['text'].strip()
                session['conversation_history'].append({"text": bot_reply})
                reply = bot_reply
            except (KeyError, IndexError) as e:
                reply = f"Error: {str(e)}, full response: {response_data}"
        else:
            reply = f"Error: {response.status_code}, {response.text}"

        return jsonify({'reply': reply})
    else:
        return jsonify({'reply': 'Invalid username or no item details found. Please try again.'}), 400


# Optional route to clear conversation history
@app.route('/clear', methods=['POST'])
def clear_history():
    session.pop('conversation_history', None)
    session.pop('product_data', None)
    return jsonify({'message': 'Conversation history and product data cleared.'})

if __name__ == '__main__':
    app.run(debug=True)
