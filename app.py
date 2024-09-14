import streamlit as st
import ollama
import time
import json
import os
from datetime import datetime
from openai import OpenAI

# List of available models
MODELS = [
    "gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo",  # OpenAI models
    "llama3.1:8b", "gemma2:2b", "mistral-nemo:latest", "phi3:latest",  # Ollama models
]

# Math categories and levels
MATH_CATEGORIES = [
    "Arithmetic", "Algebra", "Geometry", "Trigonometry", "Calculus",
    "Statistics", "Probability", "Number Theory", "Linear Algebra"
]

DIFFICULTY_LEVELS = ["Elementary", "Middle School", "High School", "Undergraduate", "Graduate"]

def get_ai_response(messages, model):
    if model.startswith("gpt-"):
        return get_openai_response(messages, model)
    else:
        return get_ollama_response(messages, model)

def get_openai_response(messages, model):
    client = OpenAI()
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content, response.usage.prompt_tokens, response.usage.completion_tokens
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, 0, 0

def get_ollama_response(messages, model):
    try:
        response = ollama.chat(
            model=model,
            messages=messages
        )
        return response['message']['content'], response['prompt_eval_count'], response['eval_count']
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, 0, 0

def stream_response(messages, model):
    if model.startswith("gpt-"):
        return stream_openai_response(messages, model)
    else:
        return stream_ollama_response(messages, model)

def stream_openai_response(messages, model):
    client = OpenAI()
    try:
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )
        return stream
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def stream_ollama_response(messages, model):
    try:
        stream = ollama.chat(
            model=model,
            messages=messages,
            stream=True
        )
        return stream
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def save_conversation(messages, filename):
    conversation = {
        "timestamp": datetime.now().isoformat(),
        "messages": messages
    }
    
    os.makedirs('conversations', exist_ok=True)
    file_path = os.path.join('conversations', filename)
    
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                conversations = json.load(f)
        else:
            conversations = []
    except json.JSONDecodeError:
        conversations = []
    
    conversations.append(conversation)
    
    with open(file_path, 'w') as f:
        json.dump(conversations, f, indent=2)

def load_conversations(uploaded_file):
    if uploaded_file is not None:
        try:
            conversations = json.loads(uploaded_file.getvalue().decode("utf-8"))
            return conversations
        except json.JSONDecodeError:
            st.error(f"Error decoding the uploaded file. The file may be corrupted or not in JSON format.")
            return []
    else:
        st.warning("No file was uploaded.")
        return []

def main():
    st.set_page_config(layout="wide")
    st.title("Math Tutor AI: Personalized Math Problem Solving Assistance")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "token_count" not in st.session_state:
        st.session_state.token_count = {"prompt": 0, "completion": 0}

    if "user_name" not in st.session_state:
        st.session_state.user_name = "Student"

    st.session_state.user_name = st.text_input("Enter your name:", value=st.session_state.user_name)

    st.sidebar.title("Math Learning Options")
    model = st.sidebar.selectbox("Choose a model", MODELS)

    custom_instructions = st.sidebar.text_area("Custom Instructions", 
        """You are a knowledgeable and patient Math Tutor AI. Your role is to help students solve math problems and understand mathematical concepts across various difficulty levels. You should provide step-by-step explanations, ask guiding questions, and offer clear solutions to mathematical problems.

Your knowledge spans:
Arithmetic, Algebra, Geometry, Trigonometry, Calculus, Statistics, Probability, Number Theory, and Linear Algebra.

For each category and difficulty level, you should be able to:
1. Provide detailed explanations of mathematical concepts
2. Offer step-by-step solutions to problems
3. Explain problem-solving strategies and techniques
4. Break down complex problems into simpler parts
5. Relate mathematical concepts to real-world applications
6. Guide students through the problem-solving process

When interacting:
- Adapt your explanations to the student's level of understanding
- Use clear, concise language while maintaining mathematical accuracy
- Encourage critical thinking by asking follow-up questions
- Provide positive reinforcement and motivation
- Offer tips for checking work and avoiding common mistakes
- Suggest resources for further practice and learning

Remember, your goal is to be a comprehensive and supportive resource for learning mathematics, covering various topics and difficulty levels, and helping students build their problem-solving skills and mathematical intuition.""")

    category_focus = st.sidebar.multiselect("Focus on specific math categories", MATH_CATEGORIES, default=MATH_CATEGORIES)
    difficulty_level = st.sidebar.selectbox("Select difficulty level", DIFFICULTY_LEVELS)

    theme = st.sidebar.selectbox("Choose a theme", ["Light", "Dark"])
    if theme == "Dark":
        st.markdown("""
        <style>
        .stApp {
            background-color: #1E1E1E;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)

    if st.sidebar.button("Clear Chat History"):
        st.session_state.messages = []
        st.session_state.token_count = {"prompt": 0, "completion": 0}

    st.sidebar.subheader("Conversation Management")
    save_name = st.sidebar.text_input("Save conversation as:", "math_tutoring_session.json")
    if st.sidebar.button("Save Conversation"):
        save_conversation(st.session_state.messages, save_name)
        st.sidebar.success(f"Conversation saved to conversations/{save_name}")

    st.sidebar.subheader("Load Conversation")
    uploaded_file = st.sidebar.file_uploader("Choose a file to load conversations", type=["json"], key="conversation_uploader")
    
    if uploaded_file is not None:
        try:
            conversations = load_conversations(uploaded_file)
            if conversations:
                st.sidebar.success(f"Loaded {len(conversations)} conversations from the uploaded file")
                selected_conversation = st.sidebar.selectbox(
                    "Select a conversation to load",
                    range(len(conversations)),
                    format_func=lambda i: conversations[i]['timestamp']
                )
                if st.sidebar.button("Load Selected Conversation"):
                    st.session_state.messages = conversations[selected_conversation]['messages']
                    st.sidebar.success("Conversation loaded successfully!")
            else:
                st.sidebar.error("No valid conversations found in the uploaded file.")
        except Exception as e:
            st.sidebar.error(f"Error loading conversations: {str(e)}")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a math question or describe a problem:"):
        st.session_state.messages.append({"role": "user", "content": f"{st.session_state.user_name}: {prompt}"})
        with st.chat_message("user"):
            st.markdown(f"{st.session_state.user_name}: {prompt}")

        category_instruction = f"Focus on the following math categories: {', '.join(category_focus)}. "
        level_instruction = f"Provide explanations suitable for {difficulty_level} level. "
        ai_messages = [
            {"role": "system", "content": custom_instructions + category_instruction + level_instruction},
            {"role": "system", "content": "Remember to provide step-by-step explanations, encourage problem-solving skills, and adapt to the student's level of understanding."},
        ] + st.session_state.messages

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for chunk in stream_response(ai_messages, model):
                if chunk:
                    if model.startswith("gpt-"):
                        full_response += chunk.choices[0].delta.content or ""
                    else:
                        full_response += chunk['message']['content']
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.05)
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

        _, prompt_tokens, completion_tokens = get_ai_response(ai_messages, model)
        st.session_state.token_count["prompt"] += prompt_tokens
        st.session_state.token_count["completion"] += completion_tokens

    st.sidebar.subheader("Token Usage")
    st.sidebar.write(f"Prompt tokens: {st.session_state.token_count['prompt']}")
    st.sidebar.write(f"Completion tokens: {st.session_state.token_count['completion']}")
    st.sidebar.write(f"Total tokens: {sum(st.session_state.token_count.values())}")

if __name__ == "__main__":
    main()