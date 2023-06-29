# pip install streamlit streamlit-chat langchain python-dotenv
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os
import uuid
import pickle
import json
from tools.tools import read_models, load_env

from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)
from langchain import PromptTemplate



models =reversed(list(read_models()))

temperature = 0.8
model = "gpt-4-0613"
chat_list = {}
chat_list_path = "chats/chat_list.json"

# Generate a unique identifier for the new chat


# Create 'chats' directory if it doesn't exist
if not os.path.exists('chats'):
    os.makedirs('chats')
    
if os.path.isfile(chat_list_path):
    with open(chat_list_path, "r") as file:
        chat_list = json.load(file)
    
def init():
    # Load the OpenAI API key from the environment variable
    load_env()
    
    # test that the API key exists
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)

    # setup streamlit page
    st.set_page_config(
        page_title=' My own Chat GPT  ',
        page_icon='data/img/snake.png' )

def get_chat_title(user_input, llm):
    
    prompt = f"""
    This is a OpenAI chat session. And As you are a helpfull assistant, 
    Give a chat title from user's first question : 
    - {user_input}
    """
    print(prompt, '\n', llm)
    response = llm(prompt)
    print(response)
    if "\nChat Title:" in response: 
        response= response.replace('Chat Title:', '')
    return response

    
def save_chat_list(chat_list):
    with open(chat_list_path, "w") as file:
        json.dump(chat_list, file)
 
def main(chat_id):
    
    global chat_list, chat_list_path, llm
        
    init()        
    

        
    with st.sidebar:
        temperature = st.slider('Temperature', 0.,1.,0.8,0.1)
        model = st.selectbox('Select the model', models) 
        def change_title_name(*args):
            print(args)
        if st.sidebar.button(f'Start New Chat - Chat id: ({chat_id[:3]}...{chat_id[-3:]})'):
            st.session_state.messages = [SystemMessage(content="You are a helpful assistant.")]

            chat_id = uuid.uuid4().hex 
            # Display chat titles and delete icons
        for c_id, chat_title in reversed(chat_list.items()):
            empt = st.empty()
            col1, col2, col3 = empt.columns([7, 1.5, 1.5])
            if col1.button(chat_title[:50], key = f"title{c_id}", type="primary" if c_id == chat_id else "secondary" ):
                with open(f'chats/{c_id}.pkl', 'rb') as f:
                    st.session_state.messages = pickle.load(f)
                    
            if col2.button("❌", key = f"del{c_id}"):
                if st.button(f'Are you sure you want to delete {chat_title}?'):
                    del chat_list[c_id]
                    os.remove(f"chats/{c_id}.pkl")
                    
            if col3.button('🖊️', key = f"edit{c_id}"):
                st.session_state['editing'] = c_id  # Store the id of the chat we're editing
                
            # Check if we're in editing mode for this chat
            if 'editing' in st.session_state and st.session_state['editing'] == c_id:
                new_title = st.text_input("New Title", chat_title)  # Duplicate this line to ensure text box stays
                if st.button('Confirm'):
                    print(f'Değiştiridiğim chat is {c_id}: {chat_title}')
                    chat_list[c_id] = new_title
                    save_chat_list(chat_list)
                    del st.session_state['editing']  # Exit editing mode after confirmation
                else:
                    print(f'Waiting for confirmation to change chat {c_id}: {chat_title}')

                    

                

            # Save the updated chat list when a delete icon is pressed
            save_chat_list(chat_list)
    chat = ChatOpenAI(temperature=temperature, model=model)
    llm = OpenAI(temperature=temperature)

    # initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]


    st.header(f"🦾 My own Chat GPT | Model : {model} ")
    # handle user input
    def get_result_and_clear_text_area():
        if user_input:
            st.session_state.messages.append(HumanMessage(content=user_input))
            # create a title from first human question (first system message second is user input)
            if len(st.session_state.messages) == 2:
                chat_title = get_chat_title(user_input, llm)
                chat_list[chat_id]=chat_title
                save_chat_list(chat_list)
                            
            with st.spinner(f"Thinking..."):
                response = chat(st.session_state.messages)
                
            st.session_state.messages.append(AIMessage(content=response.content))           
            # Save conversation
            print(st.session_state.messages)
            with open(f'chats/{chat_id}.pkl', 'wb') as f:
                pickle.dump(st.session_state.messages, f)
            
            st.session_state.user_input = ''
                
    user_input = st.text_area("Your message: ", key="user_input")
    st.button("Submit", on_click=get_result_and_clear_text_area)
    
    # display message history
    messages = st.session_state.get('messages', [])
    for i, msg in reversed(list(enumerate(messages[1:]))):
        is_user = True if i % 2 == 0 else False
        message(msg.content, is_user=is_user, key=f"{i}{'_user' if is_user else '_ai'}")


if __name__ == '__main__':
    chat_id = uuid.uuid4().hex
    main(chat_id)
