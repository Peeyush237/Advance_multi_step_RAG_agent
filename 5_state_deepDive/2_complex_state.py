from  typing import TypedDict , List , Annotated  ## annotated alg se padh lo yrr kahi se --> actuallly code thoda compelx ho  jata h isme
from langgraph.graph import END ,StateGraph
import operator

class SimpleState(TypedDict):
    count : int
    sum: Annotated [int , operator.add]
    history: List[int]


def increment(state: SimpleState) -> SimpleState:    ## since we are dealing with stategraph so instead of message graph poora simpleState class hi share hoga instead of just messages    ---> har node ko share kiya jaega --> ek m update hua to sbme update hoga
    

    new_count = state["count"] +1
    return{
        "count" : new_count,
        "sum": state["sum"] + new_count,
        "history": state["history"] + [new_count]
     } 

def should_continue(state):
    if(state["count"]<5):
        return "continue"
    else:
        return "stop"


graph = StateGraph(SimpleState)  ## poore graph k sath share kr diya stategraph  

graph.add_node("increment" , increment)

graph.set_entry_point("increment")

graph.add_conditional_edges(
    "increment",
    should_continue,
    {
    "continue": "increment",
    "stop": END
    }
)
 
app = graph.compile()

state = {
    "count": 0,
    "sum": 0,
    "history": 0
}


result = app.invoke(state)
print(result)