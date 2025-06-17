import streamlit as st
from transformers import pipeline
import torch

st.set_page_config(page_title="chatbot", layout="wide")
st.title("ChatBot: AI Assistant")

# Initialize the model using Hugging Face Transformers
@st.cache(allow_output_mutation=True)
def load_model():
    try:
        # Use a smaller model that works well on free tier
        model = pipeline(
            "text-generation",
            model="microsoft/DialoGPT-medium",
            tokenizer="microsoft/DialoGPT-medium",
            device=-1  # Use CPU
        )
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

model = load_model()

# Chat history using session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

text = st.chat_input("Type Here....")

# Function to generate responses
def generate_response(user_input):
    if model is None:
        return "Sorry, the model is not available right now."
    
    try:
        # Create a simple prompt
        prompt = f"Human: {user_input}\nAssistant:"
        
        # Generate response
        response = model(
            prompt,
            max_length=len(prompt.split()) + 50,
            num_return_sequences=1,
            temperature=0.7,
            do_sample=True,
            pad_token_id=model.tokenizer.eos_token_id
        )
        
        # Extract the generated text
        generated_text = response[0]['generated_text']
        assistant_response = generated_text.split("Assistant:")[-1].strip()
        
        # Limit response to 100 words
        words = assistant_response.split()
        if len(words) > 100:
            assistant_response = " ".join(words[:100]) + "..."
            
        return assistant_response
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

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
            st.markdown(f"**{len(st.session_state['chat_history']) - i}.** {chat['user'][:50]}...")
    else:
        st.write("No messages yet.")
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state["chat_history"] = []
        st.rerun()

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
</style>
""", unsafe_allow_html=True)

# Render messages like a real chat interface
for chat in st.session_state['chat_history']:
    # User message on right
    st.markdown(f"<div class='user-message'><strong>You:</strong><br>{chat['user']}</div>", unsafe_allow_html=True)
    # Assistant message on left
    st.markdown(f"<div class='bot-message'><strong>Assistant:</strong><br>{chat['assistant']}</div>", unsafe_allow_html=True)
