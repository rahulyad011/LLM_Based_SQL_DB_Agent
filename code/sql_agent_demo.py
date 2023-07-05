from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st

st_callback = StreamlitCallbackHandler(st.container())

# from langchain.llms import OpenAI
# from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st
import configparser

config = configparser.ConfigParser()
config.read(r'config.txt')   
openaikey = config.get('global', 'myopenAIkey')
db = SQLDatabase.from_uri("sqlite:///../database/chinook.db")
llm = OpenAI(temperature=0, openai_api_key=openaikey)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

st.title('SQL Agent Demo App')

def generate_response(input_text):
  st.info(agent_executor.run(input_text))

with st.form('my_form'):
  text = st.text_area('Enter text:', 'What are the tables present in this database?')
  submitted = st.form_submit_button('Submit')
  if not openaikey.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
  if submitted and openaikey.startswith('sk-'):
    generate_response(text)