from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from langchain_ollama import ChatOllama
import os

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

llm = ChatOllama(model="llama3")

# Load dataset safely
ORDERS_FILE = r"C:\Users\ACER PC\OneDrive\Desktop\chatbotAI\backend\orders.csv"
if os.path.exists(ORDERS_FILE):
    orders_df = pd.read_csv(ORDERS_FILE)
else:
    orders_df = None
    print("Error: 'orders.csv' not found!")

def track_order(order_id):
    if orders_df is None:
        return "Order tracking is currently unavailable. Please try again later."

    try:
        order_id = int(order_id)  # Ensure order_id is a number
        order = orders_df[orders_df["order_id"] == order_id]
        if not order.empty:
            return f"Order {order_id} is {order['status'].values[0]}."
        else:
            return f"Sorry, no order found with ID {order_id}."
    except ValueError:
        return "Invalid order ID. Please enter a valid number."

@app.route("/")
def home():
    return "Welcome to the AI Chatbot API!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "").strip()

    if user_input.lower().startswith("track order"):
        order_id = user_input.split()[-1]  # Extract order ID
        response = track_order(order_id)
    else:
        response = llm.invoke(user_input).content

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
