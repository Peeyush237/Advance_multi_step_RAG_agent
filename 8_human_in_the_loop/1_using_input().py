from typing import List, Annotated, TypedDict
from langchain_core.messages import HumanMessage
from  langgraph.graph import add_messages, StateGraph, END
from langchain_openai import ChatOpenAI

class state(TypedDict):
    message = Annotated[list, add_messages]


llm = ChatOpenAI('openai/gpt-4o-mini')

GENERATE_POST = "generate_post"
GET_REVIEW_DECISION = "get_review_decision"
POST = "post"
COLLECT_FEEDBACK = "collect_feedback"

def generate_post(state:state):
    post_content = state["message"][-1].content 


    print("\n ::current linkedIN post::")
    print(post_content)
    print("\n")

    decision = input("post to linkedIN ? y/n: ")

    if decision.lowe() =="yes":
        return POST
    else:
        return COLLECT_FEEDBACK

def get_review_decision(state: state):  
    post_content = state["messages"][-1].content 
    
    print("\n📢 Current LinkedIn Post:\n")
    print(post_content)
    print("\n")

    decision = input("Post to LinkedIn? (yes/no): ")

    if decision.lower() == "yes":
        return POST
    else:
        return COLLECT_FEEDBACK
    

def post(state: state):  
    final_post = state["messages"][-1].content  
    print("\n📢 Final LinkedIn Post:\n")
    print(final_post)
    print("\n✅ Post has been approved and is now live on LinkedIn!")


def collect_feedback(state:state):
    feedback = input("how can i improve this post")
    return{
        "message": [HumanMessage(content=feedback)]
    }

graph = StateGraph(state)


graph.add_node(GENERATE_POST, generate_post)
graph.add_node(GET_REVIEW_DECISION, get_review_decision)
graph.add_node(COLLECT_FEEDBACK, collect_feedback)
graph.add_node(POST, post)

graph.set_entry_point(GENERATE_POST)

graph.add_conditional_edges(GENERATE_POST, get_review_decision)
graph.add_edge(POST, END)
graph.add_edge(COLLECT_FEEDBACK, GENERATE_POST)

app = graph.compile()

response = app.invoke({
    "message": [HumanMessage(content="write me a linkedIN post on AI agent taking over the content creation")]
})
print(response)

