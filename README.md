# 🤖 City Weather & News Assistant

An AI-powered conversational assistant that provides real-time weather conditions and latest news for any city worldwide. Built with **Mistral AI**, **LangChain**, and **Streamlit**.

---

## ✨ Features

- **Real-time Weather** — Fetches current temperature and weather conditions for any city via OpenWeatherMap API
- **Latest News** — Retrieves the top 3 most recent news stories for any city via Tavily Search
- **Agentic Tool Use** — Automatically decides which tool(s) to invoke based on user intent using Mistral's function-calling capability
- **Conversational UI** — Clean, persistent chat interface built with Streamlit with session-based history
- **Natural Language Understanding** — Users can ask in plain English; the agent handles routing and response synthesis

---

## 🏗️ Architecture

```
User Query
    │
    ▼
ChatMistralAI (mistral-small-2506)
    │  bind_tools([get_weather, get_news])
    ▼
Tool Router
    ├── get_weather(city)  →  OpenWeatherMap API
    └── get_news(city)     →  Tavily Search API
    │
    ▼
LLM Synthesizes Final Response
    │
    ▼
Streamlit Chat UI
```

The agent follows a **ReAct-style single-step loop**:
1. LLM receives the user query
2. If a tool is needed, it's invoked with extracted arguments
3. The tool result is appended to the message history
4. LLM generates a final, synthesized natural language response

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Mistral AI (`mistral-small-2506`) |
| Agent Framework | LangChain + LangChain-MistralAI |
| Weather Data | OpenWeatherMap API |
| News Search | Tavily Search API |
| Frontend | Streamlit |
| Environment | Python-dotenv |

---

## 📁 Project Structure

```
city-assistant/
├── agent.py              # Core agent logic, tool definitions, LLM setup
├── app.py                # Streamlit frontend and chat UI
├── requirements.txt      # Python dependencies
├── .env                  # API keys (not committed)
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- API keys for:
  - [Mistral AI](https://console.mistral.ai/)
  - [OpenWeatherMap](https://openweathermap.org/api)
  - [Tavily](https://tavily.com/)

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/your-username/city-assistant.git
cd city-assistant
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
TAVILY_API_KEY=your_tavily_api_key
```

**5. Run the application**

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`.

---

## 💬 Example Usage

| User Query | Agent Behavior |
|---|---|
| `"What's the weather in Tokyo?"` | Calls `get_weather("Tokyo")`, returns temperature & conditions |
| `"Latest news from Berlin"` | Calls `get_news("Berlin")`, returns top 3 headlines |
| `"Tell me about the weather and news in Mumbai"` | Calls both tools, synthesizes a combined response |

---

## ⚙️ Configuration

### Changing the LLM Model

In `agent.py`, update the model name:

```python
llm = ChatMistralAI(
    model="mistral-large-latest",   # or any Mistral model
    api_key=MISTRAL_API_KEY
)
```

### Adding New Tools

Define a new tool using the `@tool` decorator and register it:

```python
@tool
def get_population(city: str) -> str:
    """Get the population of a city"""
    # your implementation
    ...

# Add to the tools dict and bind to the LLM
tools = {"get_weather": get_weather, "get_news": get_news, "get_population": get_population}
llm_with_tools = llm.bind_tools([get_weather, get_news, get_population])
```

---

## 🔒 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `MISTRAL_API_KEY` | Mistral AI API key | ✅ |
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key | ✅ |
| `TAVILY_API_KEY` | Tavily Search API key | ✅ |

> ⚠️ **Never commit your `.env` file.** Add it to `.gitignore`.

---

## 🧩 Limitations & Known Constraints

- The agent handles **one tool call per turn**. Multi-tool parallel calls in a single turn are not yet supported.
- Conversation history is stored in **Streamlit session state** and is lost on page refresh.
- Weather temperatures are converted from Kelvin to Celsius server-side.

---

## 🗺️ Roadmap

- [ ] Multi-tool parallel invocation per query
- [ ] Persistent conversation history (database-backed)
- [ ] Support for additional languages via Mistral's multilingual capability
- [ ] Dockerized deployment
- [ ] Unit and integration tests for tool functions

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue first to discuss proposed changes, then submit a pull request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request
