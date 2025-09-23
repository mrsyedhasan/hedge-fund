# AI Hedge Fund - Quick Start

## 🚀 Running Analysis

### Simple Analysis
```bash
python3.10 run_analysis.py AAPL
```

### Available Tickers
- AAPL (Apple)
- GOOGL (Google/Alphabet)
- MSFT (Microsoft)
- TSLA (Tesla)
- Any valid stock ticker

## 🤖 Model Configuration

This system uses **Mistral 7B via Ollama** for all AI analysis.

### Prerequisites
1. **Ollama installed and running**
2. **Mistral model downloaded**: `ollama pull mistral:7b-instruct`
3. **Python 3.10+**

## 📊 What You Get

The system runs **18 different agents**:

### Legendary Investors (12)
- Warren Buffett
- Charlie Munger  
- Ben Graham
- Peter Lynch
- Phil Fisher
- Bill Ackman
- Cathie Wood
- Stanley Druckenmiller
- Michael Burry
- Mohnish Pabrai
- Rakesh Jhunjhunwala
- Aswath Damodaran

### Core Analysis (4)
- Technical Analysis
- Fundamental Analysis
- Sentiment Analysis
- Valuation Analysis

### Management (2)
- Risk Management
- Portfolio Manager

## ⏱️ Performance

- **Execution Time**: ~1.5 minutes for full analysis
- **Data Range**: 1 year of historical data
- **Output**: Detailed signals, confidence levels, and reasoning

## 📁 Project Structure

```
src/
├── agents/          # All 18 analysis agents
├── tools/           # Data fetching and API tools
├── utils/           # LLM utilities and helpers
├── data/            # Data models and caching
├── graph/           # Langgraph workflow state
├── llm/             # Model configuration
└── main.py          # Main analysis engine
```

## 🔧 Dependencies

All dependencies are managed via `pyproject.toml` and `poetry.lock`.

Key packages:
- `langchain-ollama` - Ollama integration
- `langgraph` - Agent workflow orchestration
- `pydantic` - Data validation
- `rich` - Beautiful terminal output
