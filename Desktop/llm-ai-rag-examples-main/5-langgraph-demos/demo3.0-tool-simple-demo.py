from langgraph.graph import add_messages, StateGraph, START, END
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import AIMessage, AnyMessage, HumanMessage, SystemMessage

def tool_weather_in_oulu():
    """Tool function to get current weather temperature and forecasted temperature for next 7 days in Oulu using the Open-Meteo API."""
    weather_response = requests.get('https://api.open-meteo.com/v1/forecast?latitude=65.02&longitude=25.46&hourly=temperature_2m')
    return weather_response.json()

# result = tool_weather_in_oulu()
# print(result)

llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

## bind the weather tool to LLM
llm_with_tool = llm.bind_tools([tool_weather_in_oulu])

result = llm_with_tool.invoke([
    SystemMessage(content="You are a helpful assistant that can use tools to answer questions. You are not limited to just using the tool, you can also answer questions based on your own knowledge. If the user asks about the weather in Oulu, use the tool to get the information and include it in your response."),
    HumanMessage(content="What is the weather going to be in Oulu next few days?")
])

print(result)







