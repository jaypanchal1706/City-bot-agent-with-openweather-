import os
import requests
import streamlit as st
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.agents import create_agent

load_dotenv()

st.set_page_config(
    page_title="City AI Assistant",
    page_icon="🌆",
    layout="wide",
)

# -----------------------------
# API / environment checks
# -----------------------------
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not OPENWEATHER_API_KEY or not TAVILY_API_KEY:
    st.error(
        "Missing API keys. Add OPENWEATHER_API_KEY and TAVILY_API_KEY "
        "to your .env file."
    )
    st.stop()


# -----------------------------
# Weather tool
# -----------------------------
@tool
def get_weather(city: str) -> str:
    """Get current weather of a city."""
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city},IN&appid={OPENWEATHER_API_KEY}&units=metric"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
    except requests.RequestException as e:
        return f"Weather API error: {e}"

    if str(data.get("cod")) != "200":
        return f"Weather error: {data.get('message', 'Could not fetch weather')}"

    temp = data["main"]["temp"]
    feels_like = data["main"].get("feels_like")
    humidity = data["main"].get("humidity")
    desc = data["weather"][0]["description"]

    return (
        f"Weather in {city}: {desc}, {temp}°C. "
        f"Feels like {feels_like}°C, humidity {humidity}%."
    )


# -----------------------------
# Tavily news tool
# -----------------------------
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


@tool
def get_news(city: str) -> str:
    """Get latest news about a city."""
    try:
        response = tavily_client.search(
            query=f"latest news in {city}",
            search_depth="basic",
            max_results=5,
        )
    except Exception as e:
        return f"News API error: {e}"

    results = response.get("results", [])

    if not results:
        return f"No news found for {city}"

    news_list = []

    for r in results:
        title = r.get("title", "No title")
        url = r.get("url", "")
        snippet = r.get("content", "")

        news_list.append(
            f"TITLE: {title}\n"
            f"URL: {url}\n"
            f"SUMMARY: {snippet[:250]}"
        )

    return f"Latest news in {city}:\n\n" + "\n\n".join(news_list)


# -----------------------------
# Groq agent
# -----------------------------
@st.cache_resource
def get_agent():
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
    )

    return create_agent(
        llm,
        tools=[get_weather, get_news],
        system_prompt=(
            "You are a helpful city assistant. "
            "You can provide current weather and latest city news. "
            "Use the weather tool for weather questions and the news tool "
            "for current news questions. "
            "If the user asks for both, use both tools."
        ),
    )


agent = get_agent()


# -----------------------------
# Session state
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_weather" not in st.session_state:
    st.session_state.last_weather = None


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.title("🌆 City AI")
    st.caption("Weather + News Assistant")

    st.markdown("---")

    st.subheader("Quick actions")

    if st.button("🌤️ Ahmedabad Weather", use_container_width=True):
        st.session_state.quick_prompt = "What is the current weather in Ahmedabad?"

    if st.button("📰 Ahmedabad News", use_container_width=True):
        st.session_state.quick_prompt = "What is the latest news in Ahmedabad?"

    if st.button("🌤️📰 Both", use_container_width=True):
        st.session_state.quick_prompt = (
            "Give me the current weather and latest news in Ahmedabad."
        )

    st.markdown("---")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_weather = None
        st.rerun()

    st.markdown("---")
    st.caption("Powered by Groq + OpenWeather + Tavily")


# -----------------------------
# Main UI
# -----------------------------
st.title("🌆 City AI Assistant")
st.markdown(
    "Ask about **weather**, **latest news**, or both for any Indian city."
)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -----------------------------
# Input
# -----------------------------
prompt = st.chat_input(
    "Example: What's the weather and latest news in Ahmedabad?"
)

# Handle sidebar quick action
if "quick_prompt" in st.session_state:
    prompt = st.session_state.pop("quick_prompt")


if prompt:
    # User message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Agent response
    with st.chat_message("assistant"):
        with st.spinner("Checking weather/news..."):
            try:
                result = agent.invoke(
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": prompt,
                            }
                        ]
                    }
                )

                answer = result["messages"][-1].content

                if isinstance(answer, list):
                    answer = "\n".join(
                        str(item) for item in answer
                    )

            except Exception as e:
                answer = f"Something went wrong: {e}"

        st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
