app = Flask(__name__)
# app.config.from_object(Config)
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Session expiry time

# GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'
# API_KEY = os.getenv("GEMINI_API_KEY")



# # Helper function to initialize conversation history
# def init_conversation_history():
#     if 'conversation_history' not in session:
#         session['conversation_history'] = []



# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/fetch_data', methods=['POST'])
# def fetch_data():
#     try:
#         print(f"Received request: {request.data}")
#         username = request.json.get('username')
#         print(f"Received username: {username}")
        
#         if not username:
#             return jsonify({'message': 'Invalid username. Please provide a username.'}), 400
         
#         if fetch_item_details(username):
#             return jsonify({'message': 'Product data successfully fetched and stored.'})
#         else:
#             return jsonify({'message': 'Sorry, invalid username or no item details found.'}), 400
#     except Exception as e:
#         print(f"Error in fetch_data: {e}")
#         return jsonify({'message': f"Error: {e}"}), 500


# # Initialize conversation and provide a meal suggestion based on inventory
# @app.route('/chat', methods=['POST'])
# def chat():
#     user_message = request.json.get('message')
#     print(f"User message: {user_message}")
    
#     if not user_message:
#         return jsonify({'reply': 'Please provide a message.'}), 400
    
#     init_conversation_history()
    
#     # Fetch product data from session
#     product_data = session.get('product_data', [])
    
#     if len(session['conversation_history']) == 0:
#         initial_instruction = f"""
#         I will provide data in JSON format about products: {product_data}.
#         Suggest Indian meals using these ingredients, especially items expiring soon.
#         """
#         session['conversation_history'].append({"text": initial_instruction})

#     session['conversation_history'].append({"text": user_message})

#     data = {
#         "prompt": { "parts": session['conversation_history'] }
#     }

#     response = requests.post(
#         f'{GEMINI_API_URL}?key={API_KEY}',
#         headers={'Content-Type': 'application/json'},
#         json=data
#     )

#     if response.status_code == 200:
#         response_data = response.json()
#         try:
#             bot_reply = response_data['candidates'][0]['content']['parts'][0]['text'].strip()
#             session['conversation_history'].append({"text": bot_reply})
#             reply = bot_reply
#         except (KeyError, IndexError) as e:
#             reply = f"Error: {str(e)}, full response: {response_data}"
#     else:
#         reply = f"Error: {response.status_code}, {response.text}"

#     return jsonify({'reply': reply})

# # Optional route to clear conversation history
# @app.route('/clear', methods=['POST'])
# def clear_history():
#     session.pop('conversation_history', None)
#     session.pop('product_data', None)
#     return jsonify({'message': 'Conversation history and product data cleared.'})

# if __name__ == '__main__':
#     app.run(debug=True)
