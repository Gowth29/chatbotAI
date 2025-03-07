import pandas as pd
from langchain_ollama import ChatOllama

# Load Llama 3 from Ollama
llm = ChatOllama(model="llama3")

# Load dataset (assuming CSV format)
orders_df = pd.read_csv("orders.csv")  # Replace with your dataset path

def track_order(order_id):
    order = orders_df[orders_df["order_id"] == order_id]
    if not order.empty:
        return f"Order {order_id} is {order['status'].values[0]}."
    else:
        return "Sorry, order not found."

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    
    if "track order" in user_input.lower():
        order_id = user_input.split()[-1]  # Extract order ID from the message
        response = track_order(order_id)
    else:
        response = llm.invoke(user_input).content  # Normal chatbot response

    print("Bot:", response)
