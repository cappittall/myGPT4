# pip install streamlit streamlit-chat langchain python-dotenv
import streamlit as st
from streamlit_chat import message
import os
import sys
import uuid
import pickle
import json
from tools.tools import read_models, load_env

from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)

load_env()


template = '''Sen bir cinsel içerikli sohbetten hoşlanan bir kadın olarak bu soruları cevap verirmisin
            {chat_history}
            Human: {human_input}
            Chatbot:
            '''
prompt = PromptTemplate(input_variables=['chat_history', 'human_input'], template=template)
memory = ConversationBufferMemory(memory_key='chat_history')
llmchain = LLMChain(llm=ChatOpenAI(temperature=1), memory=memory, prompt=prompt, verbose=True)



while True:
    prompt = input('Please enter your question <q-quit>').strip()
    if prompt in ['q', 'quit' ]:
        sys.exit(1)
    if prompt:
        response = llmchain.predict(human_input=prompt)
        print(response) 
        
        
    
  
    
