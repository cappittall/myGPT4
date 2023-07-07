# pip install streamlit streamlit-chat langchain python-dotenv
import streamlit as st
from streamlit_chat import message
import os
import uuid
import pickle
import json
from tools.tools import read_models, load_env

from langchain.memory import ConversationBufferMemory
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)
from langchain import OpenAI, PromptTemplate, LLMChain 



try:
    os.environ['OPENAI_API_KEY'] = st.secrets["openai"]
except:
    pass
    
models =reversed(list(read_models()))

chat_list = {}
chat_list_path = "chats/chat_list.json"

# Add CSS styles for the button
button_style = """
    <style>
    .custom-button {
        background-color: red;
        color: white;
    }
    </style>
"""

# Create 'chats' directory if it doesn't exist
if not os.path.exists('chats'):
    os.makedirs('chats')
    
if os.path.isfile(chat_list_path):
    with open(chat_list_path, "r") as file:
        chat_list = json.load(file)
    
def init():
    # Load the OpenAI API key from the environment variable
    load_env()
    
    # setup streamlit page
    st.set_page_config(
        page_title=' My own Chat GPT  ',
        page_icon='data/img/snake.png' )
    st.session_state.temperature = 0.8
    st.session_state.model = "gpt-4-0613"
    st.session_state.system_message = "You are a helpful assistant."
    st.session_state.user_input = ""
    if "chat_id" not in st.session_state:
        st.session_state.chat_id = uuid.uuid4().hex 
    st.markdown(button_style, unsafe_allow_html=True)
    
def save_chat_list(chat_list):
    with open(chat_list_path, "w") as file:
        json.dump(chat_list, file)
 
def start_new_chat():
    st.session_state.messages = [SystemMessage(content=st.session_state.system_message)]
    st.session_state.chat_id = uuid.uuid4().hex 
            
def side_bar():
    # st.image(logo, width=50, output_format="auto")    
    with st.sidebar:
        st.session_state.system_message = st.text_input("What your need from GPT as assistant", value=st.session_state.system_message)
        st.session_state.temperature = st.slider('Temperature', 0.,1.,0.8,0.1)
        st.session_state.model = st.selectbox('Select the model', models) 
        st.sidebar.button(f'Start New Chat ', on_click=start_new_chat)
                    
        # Display chat titles and delete icons
        reversed_keys = reversed(list(chat_list.keys()))
        for c_id in reversed_keys:
            empt = st.empty()
            col1, col2, col3 = empt.columns([8, 1, 1])
            if col1.button(chat_list[c_id][:50], key = f"title{c_id}" ):
                st.session_state.chat_id = c_id
                with open(f'chats/{c_id}.pkl', 'rb') as f:
                    st.session_state.messages = pickle.load(f)
                    
            if col2.button("❌", key = f"del{c_id}"):
                st.session_state['delete'] = c_id

                    
            if col3.button('🖊️', key = f"edit{c_id}"):
                st.session_state['editing'] = c_id  # Store the id of the chat we're editing


            # Check if we're in editing mode for this chat
            if 'editing' in st.session_state and st.session_state['editing'] == c_id:
                new_title = st.text_input("New Title", chat_list[c_id])  # Duplicate this line to ensure text box stays
                if st.button('Confirm', key="custom_button"):
                    print(f'Değiştiridiğim chat is {c_id}: {chat_list[c_id]}')
                    chat_list[c_id] = new_title
                    save_chat_list(chat_list)
                    del st.session_state['editing']  # Exit editing mode after confirmation
                else:
                    print(f'Waiting for confirmation to change chat {c_id}: {chat_list[c_id]}')

                        # Check if we're in editing mode for this chat
            if 'delete' in st.session_state and st.session_state['delete'] == c_id:
                if st.button(f'Are you sure you want to delete \n\n{chat_list[c_id]}?', key="custom_button"):
                        # Store the id of the chat we're deleting
                    print(f'Delete chat is {c_id}: {chat_list[c_id]}')
                    del chat_list[c_id]
                    save_chat_list(chat_list)
                    os.remove(f"chats/{c_id}.pkl")
                    del st.session_state['delete']  # Exit delete mode after confirmation
                else:
                    print(f'Waiting for confirmation to delete chat {c_id}: {chat_list[c_id]}')

            # Save the updated chat list when a delete icon is pressed
            save_chat_list(chat_list)
   
def get_result_and_clear_text_area():
    text = st.session_state.user_input
    if text:
        st.session_state.messages.append(HumanMessage(content=text))
        # create a title from first human question (first system message second is user input)
        if len(st.session_state.messages) == 2:
            chat_title = title_chain.run(text)
            chat_list[st.session_state.chat_id]=chat_title
            save_chat_list(chat_list)

        with st.spinner(f"Thinking..."):
            response = chain.predict(human_input=text)
            st.session_state.messages.append(AIMessage(content=response))  
                    
            # Save conversation
        with open(f'chats/{st.session_state.chat_id}.pkl', 'wb') as f:
            pickle.dump(st.session_state.messages, f)
        st.session_state.user_input=""
    
   
       
def main():
    global chain, title_chain
    side_bar()
    
      # initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content=st.session_state.system_message)
        ]

    
    title_template = PromptTemplate(input_variables=['human_input'], 
            template="Write me a conversation's title about the question, Title:{human_input}")
    template = '''Please answer below questions 
                  {chat_history} 
                  Question: {human_input} 
                  Chatbot:?''' 
    prompt = PromptTemplate(input_variables=["chat_history", "human_input"], template=template)
    
    
    
    memory = ConversationBufferMemory(memory_key="chat_history")
    
    llm = OpenAI(temperature=st.session_state.temperature) #, model=st.session_state.model)    
    title_chain = LLMChain(llm=llm, prompt=title_template) 
    chain = LLMChain(llm=llm,  prompt=prompt, verbose=True, memory=memory) 

      
    st.header(f"🦾 My own Chat GPT ") 
  
    st.session_state.user_input = st.text_area('Please ask your question ', st.session_state.user_input)
    st.button(f"Submit ({st.session_state.chat_id[:3]}..{st.session_state.chat_id[-3:]})",
              on_click=get_result_and_clear_text_area )

        # display message history
    messages = st.session_state.get('messages', [])
    for i, msg in reversed(list(enumerate(messages[1:]))):
        is_user = True if i % 2 == 0 else False
        message(msg.content, is_user=is_user, key=f"{i}{'_user' if is_user else '_ai'}")

    with st.expander('Chat Message History'):
        st.info(memory.buffer)

if __name__ == "__main__":
    init()
    main()
    