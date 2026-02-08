import json
from typing import List , Dict , Any
from langchain_core.messages import HumanMessage, BaseMessage, ToolMessage, AIMessage
from langchain_core.messages import BaseMessage
from langchain_community.tools import TavilySearchResults


## create the tavily search  tools 
tavily_tool = TavilySearchResults(max_result = 5)


## fuction to execute search queries from answerquestion tool calls 
def execute_tool (state: List[BaseMessage]) -> List[BaseMessage]:
    last_ai_message: AIMessage = state[-1]

    ## extract tool calls from the AI message 
    if not hasattr(last_ai_message, "tool_calls") or not last_ai_message.tool_calls:
        return[]
    
    ## process the asnwerQuestion or ReviseAnswer tool  calls to extract search queries
    tool_message = []

    for tool_call in last_ai_message.tool_calls:
        if  tool_call["name"] in  ["AnswerOuestion" , "Reviseanswer"]:
            call_id = tool_call["id"]
            search_queries = tool_call["args"].get("search_queries" , [])

            ## execute each search query using the tavily search
            query_result ={}
            for query in search_queries:
                result = tavily_tool.invoke(query)
                query_result[query] = result


                ## create a tool message with result 
            tool_message.append(
                ToolMessage(
                    content = json.dump(query_result),
                    tool_call_id = call_id
                    )
                )
    return tool_message

## example usage 

test_state= [
        HumanMessage(
        content="Write about how small business can leverage AI to grow"
    ),
    AIMessage(
        content="", 
        tool_calls=[
            {
                "name": "AnswerQuestion",
                "args": {
                    'answer': '', 
                    'search_queries': [
                            'AI tools for small business', 
                            'AI in small business marketing', 
                            'AI automation for small business'
                    ], 
                    'reflection': {
                        'missing': '', 
                        'superfluous': ''
                    }
                },
                "id": "call_KpYHichFFEmLitHFvFhKy1Ra",
            }
        ],
    )
]

# Execute the tools
# results = execute_tools(test_state)

# print("Raw results:", results)
# if results:
#     parsed_content = json.loads(results[0].content)
#     print("Parsed content:", parsed_content)

## by running this code you'll see how  it works ---->> test_state ko as a temporary state use kr rhe h yaha ---> baad m to asli state aayega hi
