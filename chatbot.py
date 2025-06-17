import streamlit as st
import requests
import json

st.set_page_config(page_title="chatbot", layout="wide")
st.title("ChatBot: AI Assistant")

# Chat history using session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

text = st.chat_input("Type Here....")

# Simple response function (you can replace this with any AI service)
def generate_response(user_input):
    # For now, let's create a simple rule-based response
    # You can replace this with any AI API call
    
    user_input_lower = user_input.lower()
    
    if "hello" in user_input_lower or "hi" in user_input_lower:
        return "Hello! How can I help you today?"
    elif "how are you" in user_input_lower:
        return "I'm doing great! Thanks for asking. How are you?"
    elif "what is your name" in user_input_lower:
        return "I'm your AI assistant chatbot. You can ask me anything!"
    elif "bye" in user_input_lower or "goodbye" in user_input_lower:
        return "Goodbye! Have a great day!"
    elif "help" in user_input_lower:
        return "I'm here to help! You can ask me questions, have a conversation, or just chat about anything."
    elif "weather" in user_input_lower:
        return "I don't have access to real-time weather data, but you can check your local weather service for current conditions."
    elif "time" in user_input_lower:
        return "I don't have access to real-time clock, but you can check the time on your device."
    else:
        responses = [
            f"That's interesting! Tell me more about {user_input}.",
            f"I understand you're asking about {user_input}. Can you provide more details?",
            f"Thanks for sharing that with me. What would you like to know more about?",
            f"I'd be happy to help you with {user_input}. What specific aspect interests you?",
            "That's a great question! While I don't have all the details, I'm here to chat and help however I can."
        ]
        import random
        return random.choice(responses)

# Handle user input
if text:
    with st.spinner("Thinking...."):
        response = generate_response(text)
        st.session_state["chat_history"].append({'user': text, 'assistant': response})

# Sidebar
with st.sidebar:
    st.title("Dashboard")
    st.write("Chat about anything with your AI friendly Assistant")
    st.markdown("---")
    st.subheader("Conversation History")
    
    # Display all user questions in the sidebar
    if st.session_state["chat_history"]:
        for i, chat in enumerate(reversed(st.session_state["chat_history"])):
            question_preview = chat['user'][:50] + "..." if len(chat['user']) > 50 else chat['user']
            st.markdown(f"**{len(st.session_state['chat_history']) - i}.** {question_preview}")
    else:
        st.write("No messages yet.")
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state["chat_history"] = []
        st.experimental_rerun()

# Add some CSS for alignment
st.markdown("""
<style>
.user-message {
    padding: 15px;
    border-radius: 15px;
    max-width: 70%;
    margin-left: auto;
    margin-right: 20px;
    margin-bottom: 10px;
    text-align: right;
    background-color: #DCF8C6;
    border: 1px solid #C1E1C1;
}
.bot-message {
    padding: 15px;
    border-radius: 15px;
    max-width: 70%;
    margin-right: auto;
    margin-left: 10px;
    margin-bottom: 10px;
    text-align: left;
    background-color: #F1F1F1;
    border: 1px solid #E0E0E0;
}
.chat-container {
    padding: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# Render messages like a real chat interface
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for chat in st.session_state['chat_history']:
    # User message on right
    st.markdown(f"<div class='user-message'><strong>You:</strong><br>{chat['user']}</div>", unsafe_allow_html=True)
    # Assistant message on left
    st.markdown(f"<div class='bot-message'><strong>Assistant:</strong><br>{chat['assistant']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("💬 **Simple AI Chatbot** - Built with Streamlit")
