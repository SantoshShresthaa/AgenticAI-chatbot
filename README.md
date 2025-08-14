### AI Chatbot

A small, agentic AI chatbot with a Gradio UI. It uses Google Gemini for generation and OpenRouter for automatic response evaluation, driven by simple prompts and local profile data.

### Requirements

- Python ≥ 3.13 (managed automatically by `uv`)
- `uv` package manager (for dependency management, virtualenvs and builds)

### Install uv (macOS/Linux)

You can install `uv` in either of the following ways:

```bash
# Recommended one-line installer
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via Homebrew (macOS)
brew install uv

# Verify
uv --version
```

The installer will add `uv` to your PATH. If the command isn’t found after installation, restart your shell.

### Project Structure

```
chatbot/
├── bio/
│   ├── Profile.pdf            # Your resume/profile (parsed at runtime)
│   └── self_intro.txt         # A short personal summary
├── src/chatbot/
│   ├── __init__.py            # Main entry; launches Gradio UI
│   ├── core/
│   │   └── config.py          # Env-driven configuration
│   ├── fileParser/
│   │   └── parser.py          # PDF and text parsing helpers
│   ├── services/
│   │   ├── ChatService.py     # Chat orchestration with Gemini
│   │   ├── EvaluatorService.py# Quality evaluation via OpenRouter
│   │   └── UserProfileService.py # Loads content from bio/
│   └── utils/
│       └── prompt.py          # System/evaluator prompt builders
├── .env.example            # Example environment file
├── pyproject.toml             # Project metadata and dependencies
└── README.md                  # This file
```

### Setup

```bash
# 1) Clone & enter the project
git clone git@github.com:SantoshShresthaa/AgenticAI-chatbot.git

cd AgenticAI-chatbot

# 2) Install dependencies (creates a virtualenv automatically)
uv sync

# 3) Create your .env from the example and edit values
cp .env.example .env
```

### Environment Variables

The app reads configuration from `.env` via `src/chatbot/core/config.py`. Ensure the following keys exist (the values below reflect current defaults in code):

```env
# Google Gemini (used for generation)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
GEMINI_MODEL=gemini-2.0-flash

# OpenRouter (used for evaluation)
OPEN_ROUTER_API_KEY=your_openrouter_api_key_here
OPEN_ROUTER_BASE_URL=https://openrouter.ai/api/v1
```

Notes:
- You must provide at least one of `GEMINI_API_KEY` or `OPEN_ROUTER_API_KEY` for the app to start; for full functionality, set both.
- The legacy keys in `env_example.txt` (like `OPENAI_API_KEY`) are not used by the current runtime logic. Prefer the keys shown above.

### Running

```bash
# Using the console entrypoint (installed via pyproject)
uv run chatbot

```

Then open your browser at `http://localhost:7860`.

### How it works (high level)

- `ChatService.chat(...)` builds a system prompt from your local `bio/` data and the user’s message history, then calls Gemini to generate a reply.
- The reply is evaluated by `EvaluatorService.evaluate(...)` using an OpenRouter-hosted model. If rejected, the assistant re-prompts itself with feedback and retries once.

### Updating models/providers

You can change defaults via environment variables without code changes:

```env
GEMINI_MODEL=gemini-2.0-flash
OPEN_ROUTER_BASE_URL=https://openrouter.ai/api/v1
```

### Troubleshooting

- App prints: “No API keys found!”
  - Ensure `.env` is present and contains `GEMINI_API_KEY` and/or `OPEN_ROUTER_API_KEY`.
  - Restart the terminal or run `uv run env | grep -E "GEMINI|OPEN_ROUTER"` to verify they’re loaded.

- Gradio launches but responses fail
  - Check the API key scopes and remaining quota.
  - Confirm the base URLs match your provider settings.

- PDF parsing issues
  - Verify `bio/Profile.pdf` exists and is a readable PDF.
  - Ensure `bio/self_intro.txt` exists and contains UTF-8 text.

### License

MIT License