import streamlit as st

from langchain.llms import GPT4All

from langchain.agents.agent_toolkits import create_python_agent
from langchain.tools.python.tool import PythonREPLTool

# path to weights
PATH = '/home/cappittall/Documents/myGPT4/model/GPT4ALL'

llm = GPT4All(model=PATH, verbose=True)


agent_executor = create_python_agent(llm=llm, tool=PythonREPLTool, verbose=True)

st.title(' 🦾 🧠   GPT 4  for may ovn    ')
st.info('Ask me, what ever you want!')

prompt = st.text_input('Ben Rebeka, emrediniz efendim !')

# if prompt exist call api 
if prompt:
    
    # pass the prompt to LLM chain
    response = agent_executor.run(prompt)
    st.write(response)