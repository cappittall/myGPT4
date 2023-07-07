## Chats with own documents. 
import os
import sys

import openai
import streamlit as st

from langchain.document_loaders import UnstructuredExcelLoader
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

from tools.tools import load_env

import pandas as pd


load_env()
if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "": 
    print('Api key not exists') 
    exit(1)
    
def main():
    
    st.title(' 🫰💸 PVD Fiyat hesaplama ')
    model = "gpt-4-0613"
    # loader = UnstructuredHTMLLoader('../barlokmetal/index.html', mode="single")
    loader = UnstructuredExcelLoader('data/fiyatlar/Fiyat.xlsx')
    
    index = VectorstoreIndexCreator().from_loaders([loader])
    
    
    chain = RetrievalQA.from_chain_type(llm=ChatOpenAI(model=model), chain_type="stuff", retriever=index.vectorstore.as_retriever(), input_key="question")

    query = st.chat_input('Lütfen talebinizi girin: \'örn: çap 10 mm yükseklik 20 mm silindir. Titan kaplanacak')
    

    if query:
        ## response = chain.run({'question': query})
        st.warning(query)
        st.write(chain({"question" : query } )['result'])
    

if __name__== '__main__':
    main()
    
    