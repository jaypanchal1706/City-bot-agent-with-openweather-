# 🌆 City AI Assistant

A Streamlit-based AI city assistant that combines **Groq**, **OpenWeather**, and **Tavily** to answer questions about current weather and the latest news for Indian cities.

The application uses a LangChain agent to decide which tool to call based on the user's request.

## ✨ Features

- 🌤️ Get current weather for an Indian city
- 📰 Get the latest news for a city
- 🤖 AI agent powered by Groq
- 🔧 LangChain tools for weather and news
- 💬 Interactive Streamlit chat interface
- ⚡ Quick-action buttons for common queries
- 🗑️ Clear chat history
- 🔐 API keys loaded securely from `.env`
- ⚠️ Error handling for API failures

## 🧰 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application programming language |
| Streamlit | Web UI |
| LangChain | Agent and tool orchestration |
| Groq | LLM |
| OpenWeather | Current weather data |
| Tavily | Web/news search |
| python-dotenv | Environment variable management |
| Requests | OpenWeather API requests |

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │    Streamlit UI     │
                    │                     │
                    │  Chat / Quick       │
                    │  Actions            │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   LangChain Agent   │
                    │      + Groq LLM     │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
             ┌──────────────┐      ┌──────────────┐
             │ Weather Tool │      │   News Tool  │
             └──────┬───────┘      └──────┬───────┘
                    │                     │
                    ▼                     ▼
             ┌──────────────┐      ┌──────────────┐
             │ OpenWeather  │      │    Tavily    │
             │     API      │      │     API      │
             └──────────────┘      └──────────────┘
```

## 📁 Project Structure

```text
RUNNABLE PROJECT/
│
├── streamlit_app.py
├── .env
└── README.md
```

> Do not commit `.env` to GitHub because it contains API keys.

## 🔑 API Keys

The application requires three API keys.

Create a `.env` file in the project directory:

```env
OPENWEATHER_API_KEY=your_openweather_api_key
TAVILY_API_KEY=your_tavily_api_key
GROQ_API_KEY=your_groq_api_key
```

The application loads these variables using `python-dotenv`.

### Getting the API keys

- **OpenWeather:** Create an account and obtain an API key from OpenWeather.
- **Tavily:** Create an account and obtain an API key from Tavily.
- **Groq:** Create an account and obtain a Groq API key.

## ⚙️ Installation

### 1. Clone the project

```bash
git clone <your-repository-url>
cd <your-project-folder>
```

### 2. Create a virtual environment

On Windows:

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install streamlit python-dotenv requests tavily-python langchain langchain-groq
```

## ▶️ Run the Application

Start the Streamlit application with:

```bash
streamlit run streamlit_app.py
```

Streamlit will provide a local URL, normally similar to:

```text
http://localhost:8501
```

Open the URL in your browser.

## 💬 Example Questions

You can ask questions such as:

```text
What is the current weather in Ahmedabad?
```

```text
What is the latest news in Mumbai?
```

```text
Give me the current weather and latest news in Delhi.
```

```text
What's the weather like in Rajkot?
```

The agent decides whether it needs the weather tool, the news tool, or both.

## 🔧 Tools

### Weather Tool

The `get_weather` tool accepts a city name and retrieves current weather information from OpenWeather.

It returns information including:

- Temperature
- Weather description
- Feels-like temperature
- Humidity

Example:

```text
Weather in Ahmedabad: clear sky, 34.67°C.
Feels like 35.2°C, humidity 42%.
```

### News Tool

The `get_news` tool searches Tavily for recent news related to the requested city.

It returns:

- News title
- Source URL
- Short content summary

## 🤖 AI Agent

The application creates a LangChain agent using the Groq model:

```python
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
)
```

The agent has access to:

```python
tools=[get_weather, get_news]
```

Its system prompt instructs it to use the weather tool for weather questions and the news tool for current-news questions.

## 🖥️ User Interface

The Streamlit interface contains:

### Sidebar

- 🌤️ City Weather
- 📰 city News
- 🌤️📰 Both
- 🗑️ Clear Chat

### Main Area

- Application title
- Chat history
- Chat input
- Agent response
- Loading indicator

## 🔒 Security

### ✅ Use `.env`

```env
OPENWEATHER_API_KEY=your-key
TAVILY_API_KEY=your-key
GROQ_API_KEY=your-key
```


## 🚀 Future Improvements

Possible improvements include:

- 🌡️ More detailed weather cards
- 🌦️ Weather icons
- 📰 Dedicated news cards with clickable source links
- 📍 Automatic location detection
- 📅 Weather forecast
- 🔎 News category filtering
- 🗣️ Voice input
- 💾 Persistent conversation history
- 🎨 Custom Streamlit theme
- 🐳 Docker deployment
- ☁️ Deployment to Streamlit Community Cloud

## 📜 License

This project is intended for learning and demonstration purposes. Add your preferred license here if you plan to publish the project.

---

Built with **Python + Streamlit + LangChain + Groq + OpenWeather + Tavily**.
