from typing import Annotated, TypedDict

from langgraph.graph import add_messages, StateGraph, START, END
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import AIMessage, AnyMessage, HumanMessage
from langgraph.prebuilt import ToolNode, tools_condition
import json

def tool_weather_in_oulu():
    """Tool function to get current weather temperature and forecasted temperature for next 7 days in Oulu using the Open-Meteo API."""
    weather_response = requests.get('https://api.open-meteo.com/v1/forecast?latitude=65.02&longitude=25.46&hourly=temperature_2m')
    return weather_response.json()

llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash-lite')

## bind the weather tool to LLM
tools = [tool_weather_in_oulu]
llm_with_tool = llm.bind_tools(tools)


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
    response = llm_with_tool.invoke(state["messages"])

    return {"messages": [response]}

# build graph with the above node as single node
builder = StateGraph(State)
builder.add_node("llm", llm_node)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "llm")

#  if the last AIMessage contains tool calls, route to the tool execution node; otherwise, end the workflow.
builder.add_conditional_edges("llm", tools_condition)
builder.add_edge("tools", "llm")


graph = builder.compile()

## execute the graph with invoke method expecting the tool to be called and the result to be in the end state
end_state_tool_result_expected = graph.invoke({
    "messages": [HumanMessage(content="What is the expected weather temperature in Oulu for the next few days?")]
})

for message in end_state_tool_result_expected["messages"]:
    message.pretty_print()




## execute the graph with a query which is not supposed to be requiring the use of the tool, to see how the graph handles it
# end_state_joke = graph.invoke({
#     "messages": [HumanMessage(content="Tell me a joke")]
# })  

# print(end_state_joke)






