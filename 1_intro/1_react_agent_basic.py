from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
# Use this for the legacy executor
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_community.tools import tavily_search , TavilySearchResults
from langchain_core.prompts import PromptTemplate


load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")
search_tool = TavilySearchResults()
tools = [search_tool]


# ye purana wala way h 
#agent = create_react_agent(tool=tools, llm = llm, agent="zero-shot-react-description", verbose = True) ## zero shot ka matlb apn pehle se koi contex nai denge llm  ko ye khud se hi reasoning karega poori
template = "give me a funny tweet about today's weather in banglore"
custom_prompt = PromptTemplate.from_template(template)

 # 2. Construct the ReAct agent
agent = create_react_agent(llm= llm, tools = search_tool, prompt=custom_prompt)

# 3. Create the executor (the runtime)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
result = agent_executor.invoke({"input": "give me a funny tweet about today's weather in banglore"})


print(result)
