from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph , END
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

memory = MemorySaver()    ### ye langgraph ki library h jo ki memery checkpoint banane k liye use hoti h 

llm = ChatOpenAI('openai/gpt-4o-mini')

class BasicChatState(TypedDict):
    message: Annotated[list, add_messages]

def chatbot(state: BasicChatState):
    return{
        "messages": [llm.invoke(state["message"])]
    }

graph = StateGraph(BasicChatState)

graph.add_node("chatbot", chatbot)
graph.add_edge("chatbot", END)

graph.set_entry_point("chatbot")

app = graph.compile(checkpointer=memory)

config = {
    "configurable": {
        "thread_id":1  ## ye apn se ek configuration banaya and bata diya ki iss thread id pe ye wali chat run hogi to ab is config p kara gya har msg ek dusre se related h
    }
}


while True:
    user_input = input("user:")
    if(user_input in ["exit", "end"]):
        break
    else:
        result = app.invoke({
            "message": [HumanMessage(content=user_input)]
        }, config=config)

        print("AI: " + result["message"][-1].content)