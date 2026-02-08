from typing import List , Sequence
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.graph import END, MessageGraph, StateGraph
from chains import generation_chain , reflection_chain

load_dotenv()

## ab ham sare nodes banaenge and then usko connect krenge 
## study what message graph do -- but from now on use the stategraph
graph = MessageGraph()

REFLECT = "reflect"
GENERATE = "generate"
graph = MessageGraph()

## ab apn banaenge function jo ki chain invoke karenge with message with message history
def generate_node(state):  ## here state is the list of messages (wahi messages jo append krte rhne hote h )
    generation_chain.invoke({
        "message": state
    })

def reflect_node(state):

    response = reflection_chain.invoke({
        "message": state
    })
    return [HumanMessage(content=response.content)]  ## yaha apne ko reflect function ka jo msg mil rha (i.e critique wala msg) usko as a human message append kr rhe h 


## ab apn banaenge graph ka structure
graph.add_node(GENERATE, generate_node)
graph.add_node(REFLECT, reflect_node)
graph.set_entry_point(GENERATE)

def should_continue(state):
    if (len(state)>6):
        return END
    return REFLECT

graph.add_conditional_edges(GENERATE, should_continue)
graph.add_edge(REFLECT, GENERATE)

## ye hua graph ka structure khatam

app = graph.compile()

print(app.get_graph().draw_mermaid())
app.get_graph().print_ascii()

response = app.invoke(HumanMessage(content="AI agents taking over content creation"))

print(response)

## ye apn se poora sikha ki reflection agent kaise banta h , smjh nai aae to ek baar chat gpt kr lena achhe se smjhne ki liye with code 

