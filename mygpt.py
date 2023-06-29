
import streamlit as st
from dotenv import load_dotenv

import os

## LangChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.schema import (AIMessage, SystemMessage, HumanMessage)
from streamlit_chat import message

from tools import tools

def init():
    st.set_page_config(
        page_title='My own Chat GPT ',
        page_icon='snake.png')
    
    st.header('🏄🏾 Ask Me What Ever You Want ')
    chat = ChatOpenAI(temperature=0.9, model="gpt-4-0613")
    
    if os.getenv('OPENAI_API_KEY') == None or os.getenv('OPENAI_API_KEY')=="": exit(1)
    
    return chat

def sidebar(chat):
    if 'messages' not in st.session_state:
        st.session_state.messages = [SystemMessage(content="You are a helpful assistant")]
        st.session_state.message_submitted = False  # Add the flag

    with st.sidebar:
        user_input = st.text_area("Your question...", key="user_input")
        submit_button = st.button("Submit")  # Add a submit button

        if submit_button and user_input and not st.session_state.message_submitted:
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner("Thinking..."):
                response = chat(st.session_state.messages)
            st.session_state.messages.append(AIMessage(content=response.content))
            st.session_state.message_submitted = True  # Set the flag

        if st.session_state.message_submitted:
            # Display a message indicating that the input has been submitted
            st.info("Message submitted!")

            # Clear the text area by setting the user_input to an empty string
            st.session_state.user_input = ""

    # Clear the text area when an AI response is received
    if len(st.session_state.messages) > 1 and isinstance(st.session_state.messages[-1], AIMessage):
        st.session_state.user_input = ""
                
         
def display_messages():
    messages = st.session_state.get('messages', [])  
    print(messages)  
    if len(messages)>1:  
        for i in range(1, len(messages)):
            msg = messages[i]
            is_user = False if i % 2 == 0 else True 
            key = f'{i}_{"user" if is_user else "ai"}' 
            message(msg.content, is_user = is_user, key = key )
        
            
def main():
    chat=init()
    sidebar(chat)
    display_messages()
    

    
    
    
if __name__=='__main__':
    main()
    
    