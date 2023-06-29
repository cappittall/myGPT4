import streamlit as st 
from langchain import PromptTemplate, LLMChain
from langchain.llms import GPT4All

PATH = 'C:/Users/User/AppData/Local/nomic.ai/GPT4All/ggml-mpt-7b-instruct.bin'

llm = GPT4All(model=PATH, verbose=True)

prompt = PromptTemplate(input_variables=['question'], template="""
    Question: {question}
    
    Answer: Let's think step by step.
    """)

llm_chain = LLMChain(prompt=prompt, llm=llm)

st.title(' 🦾 🧠   GPT 4  for may ovn    ')
st.info('Ask me, what ever you want!')

prompt = st.text_input('Ben Rebeka, emrediniz efendim ! - V.chain')

if prompt: 
    response = llm_chain.run(prompt)
    print(response)
    st.write(response)