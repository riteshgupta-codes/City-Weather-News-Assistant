# agent.py

from dotenv import load_dotenv
load_dotenv()

import os
import requests
from tavily import TavilyClient

from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# ==============================
# API KEYS
# ==============================
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# ==============================
# TOOLS
# ==============================
@tool
def get_weather(city: str) -> str:
    """Get current weather of a city"""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}"
    res = requests.get(url).json()

    if str(res.get("cod")) != "200":
        return "City not found"

    temp = res["main"]["temp"] - 273.15
    desc = res["weather"][0]["description"]

    return f"{city.title()}: {desc}, {temp:.2f}°C"


tavily = TavilyClient(api_key=TAVILY_API_KEY)

@tool
def get_news(city: str) -> str:
    """Get latest news of a city"""
    res = tavily.search(query=f"latest news in {city}", max_results=3)
    return "\n\n".join([r["title"] for r in res["results"]])


# ==============================
# LLM
# ==============================
llm = ChatMistralAI(
    model="mistral-small-2506",
    api_key=MISTRAL_API_KEY
)

llm_with_tools = llm.bind_tools([get_weather, get_news])

tools = {
    "get_weather": get_weather,
    "get_news": get_news
}


# ==============================
# SIMPLE AGENT (NO STREAMING)
# ==============================
def run_agent(user_input):
    response = llm_with_tools.invoke(user_input)

    # If tool needed
    if response.tool_calls:
        tc = response.tool_calls[0]

        tool_name = tc["name"]
        tool_args = tc["args"]

        tool_result = tools[tool_name].invoke(tool_args)

        # Create properly formatted message objects
        messages = [
            HumanMessage(content=user_input),
            response,
            ToolMessage(
                content=str(tool_result),
                tool_call_id=tc["id"]
            )
        ]

        # Final answer after tool
        final = llm_with_tools.invoke(messages)

        return final.content

    return response.content