from typing import Annotated, TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

class ChatState(TypedDict):
    messages: Annotated[list, add_messages] # APPEND reducer​ 

def call_llm(state: ChatState) -> dict:
    response = llm.invoke(state["messages"]) # pass message list​. Note! The response type of invoke is an AIMessage, not a string
    return {"messages": [response]} # AIMessage appended​

g = StateGraph(ChatState)
g.add_node("call_llm", call_llm)
g.add_edge(START, "call_llm"); 
g.add_edge("call_llm", END)
app = g.compile()

result = app.invoke({"messages": [
    SystemMessage("You are a helpful assistant expert in funny animal jokes."),
    HumanMessage("Tell me a joke I have not heard before. Make it funny!")
]})

print(result)
print("\n\n\nFull message history:")
for msg in result['messages']:
    print(f"{(msg.type)} - {msg.content}")