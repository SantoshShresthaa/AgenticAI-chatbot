# AI Chatbot

A scalable, agentic AI chatbot built with Python, supporting multiple LLM providers (OpenAI and Google Gemini) with a clean Gradio interface.

## 🏗️ Project Structure

```
chatbot/
├── src/chatbot/
│   ├── core/
│   │   └── config.py          # Configuration management
│   ├── llm/
│   │   ├── base.py            # Abstract LLM interface
│   │   ├── openai_provider.py # OpenAI implementation
│   │   └── gemini_provider.py # Google Gemini implementation
│   ├── agent.py               # Simple chat agent
│   ├── factory.py             # LLM provider factory
│   ├── ui.py                  # Gradio interface
│   └── __init__.py            # Main entry point
├── example.py                 # Command-line example
├── env_example.txt            # Environment variables template
├── pyproject.toml             # Project dependencies
└── README.md                  # This file
```

## 🚀 Features

- **Multiple LLM Providers**: Support for OpenAI and Google Gemini
- **Clean Architecture**: Follows SOLID principles with clear separation of concerns
- **Extensible Design**: Easy to add new LLM providers or agents
- **Modern UI**: Beautiful Gradio-based chat interface
- **Simple Configuration**: Environment-based configuration
- **Type Safety**: Full type hints throughout

## 📦 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd chatbot
```

2. Install dependencies:
```bash
uv sync
# or
pip install -e .
```

3. Set up environment variables:
```bash
cp env_example.txt .env
# Edit .env with your API keys
```

## 🔧 Configuration

Create a `.env` file with your API keys:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Google Gemini Configuration  
GEMINI_API_KEY=your_gemini_api_key_here

# Default LLM Provider (openai or gemini)
DEFAULT_LLM_PROVIDER=openai

# Default Model
DEFAULT_MODEL=gpt-3.5-turbo
```

## 🎯 Usage

### Web Interface

Launch the Gradio web interface:

```bash
python -m chatbot
# or
chatbot
```

Then open your browser to `http://localhost:7860`

### Command Line Example

Run the simple command-line example:

```bash
python example.py
```

### Programmatic Usage

```python
import asyncio
from src.chatbot.factory import LLMFactory
from src.chatbot.agent import ChatAgent

async def main():
    # Create LLM provider
    provider = LLMFactory.create_provider("openai", "your-api-key")
    
    # Create agent
    agent = ChatAgent(provider, "You are a helpful assistant.")
    
    # Chat
    response = await agent.chat("Hello, how are you?")
    print(response)

asyncio.run(main())
```

## 🧩 Architecture

This project follows **SOLID principles** and clean architecture:

### Single Responsibility Principle (SRP)
- Each class has one clear responsibility
- `LLMProvider` only handles LLM communication
- `ChatAgent` only manages conversation flow
- `ChatInterface` only handles UI

### Open/Closed Principle (OCP)
- Easy to add new LLM providers by extending `LLMProvider`
- New agent types can be created by extending `ChatAgent`

### Liskov Substitution Principle (LSP)
- All LLM providers can be used interchangeably
- Factory pattern ensures consistent interfaces

### Interface Segregation Principle (ISP)
- Clean, minimal interfaces for each component
- No forced dependencies on unused methods

### Dependency Inversion Principle (DIP)
- High-level modules depend on abstractions
- `ChatAgent` depends on `LLMProvider` interface, not concrete implementations

## 🔌 Adding New LLM Providers

1. Create a new provider class:

```python
from .base import LLMProvider, ChatMessage

class CustomProvider(LLMProvider):
    async def generate_response(self, messages: List[ChatMessage]) -> str:
        # Implement your provider logic
        pass
```

2. Register in the factory:

```python
# In factory.py
elif provider_type == "custom":
    return CustomProvider(api_key, model)
```

## 🧪 Testing

Run tests:

```bash
pytest
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License

