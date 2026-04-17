from typing import Annotated, TypedDict

from langgraph.graph import add_messages, StateGraph, START, END
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import AIMessage, AnyMessage, HumanMessage
import json

def tool_weather_in_oulu():
    """Tool function to get current weather temperature and forecasted temperature for next 7 days in Oulu using the Open-Meteo API."""
    weather_response = requests.get('https://api.open-meteo.com/v1/forecast?latitude=65.02&longitude=25.46&hourly=temperature_2m')
    return weather_response.json()

llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash-lite')

## bind the weather tool to LLM
llm_with_tool = llm.bind_tools([tool_weather_in_oulu])


class State(TypedDict):
    # here add_messages is technically a reducer which appends the new messages to the existing messages in the state,
    # this is useful for keeping track of the conversation history in a graph execution
    messages: Annotated[list[AnyMessage], add_messages] 

# The above is a common pattern for keeping track of conversation history in a graph execution, 
# where the state is updated with new messages as the conversation progresses.
# Langgraph has a built in MessagesState which does exactly this, but we can also define our own state as shown above.

# define a node for calling the llm with the tool
# a node always has to return the new state
def llm_node(state: State):
    # copy incoming messages
    messages = list(state["messages"]) or []

    # 1) call the LLM; it may return a function call request in additional_kwargs
    ai_response_msg = llm_with_tool.invoke(messages)
    print("LLM response: ", ai_response_msg) #debug print to see the LLM response and check if it contains the function call request
    messages.append(ai_response_msg)

    # 2) detect a function/tool call requested by the model
    fc = None
    if isinstance(ai_response_msg, AIMessage):
        fc = ai_response_msg.additional_kwargs.get("function_call")

    if fc:
        func_name = fc.get("name")        

        # map function name to actual Python callable (register your tools here)
        tools = {"tool_weather_in_oulu": tool_weather_in_oulu}

        if func_name in tools:
            # execute the tool and append its output as a tool message
            tool_result = tools[func_name]()
            tool_msg = AIMessage(content=json.dumps(tool_result), additional_kwargs={"role": "tool", "name": func_name})
            messages.append(tool_msg)

            # 3) re-invoke the LLM with the tool result so it can produce the final assistant reply
            final_ai = llm_with_tool.invoke(messages)
            messages.append(final_ai)

    return {"messages": messages}

# build graph with the above node as single node
builder = StateGraph(State)
builder.add_node("tool_call_llm", llm_node)
builder.add_edge(START, "tool_call_llm")
builder.add_edge("tool_call_llm", END)
graph = builder.compile()

## execute the graph with invoke method expecting the tool to be called and the result to be in the end state
end_state_tool_result_expected = graph.invoke({
    "messages": [HumanMessage(content="What is the weather going to be in Oulu in the next days?")]
})

##print(end_state_tool_result_expected)
#print("AI response: ", end_state_tool_result_expected["messages"][-1].content)
for message in end_state_tool_result_expected["messages"]:
    message.pretty_print()


## execute the graph with a query which is not supposed to be requiring the use of the tool, to see how the graph handles it
# end_state_joke = graph.invoke({
#     "messages": [HumanMessage(content="Tell me a joke")]
# })  

# for message in end_state_joke["messages"]:
#     message.pretty_print()






