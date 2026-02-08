from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode

load_dotenv()

class BasicChatBot(TypedDict):
    message: Annotated[list, add_messages]

search_tool = TavilySearchResults()
tools = [search_tool]

llm = ChatOpenAI('openai/gpt-4o-mini')

llm_with_tools = llm.bind_tools(tools=tools)

def chatbot(state: BasicChatBot):
    return{
        "message": [llm_with_tools.invoke(state["message"])]
    }

tool_node = ToolNode(tools=tools)

## ekabut main cheezz -- jo llm se output aata h usme bahut saari cheeze hoti h it look something like image.png -- for eg. content , tool_call(mtlb  tool call krne ki jrurat h kya )
def tools_router(state: BasicChatBot):
    last_message = state['message'][[-1]]  ## yaha pe apn ne messages ki list se last message utha lia h 

    if(hasattr(last_message, "tool_calls") and len(last_message.tool_calls)>0):
        return "tool_node"
    else:
        return END
    

graph = StateGraph(BasicChatBot)

graph.add_node("chatbot", chatbot)
graph.add_node("tool_node", tool_node)
graph.set_entry_point("chatbot")

graph.add_conditional_edges("chatbot", tools_router)
graph.add_edge("tool_node", "chatbot")

app = graph.compile()


while True:
    user_input = input("user: ")
    if(user_input in ["exit", "end"]):
        break
    else: 
        result = app.invoke({
            "messages": [HumanMessage(content=user_input)]
        })

        print(result)



        