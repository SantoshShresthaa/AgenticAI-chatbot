from chatbot.services.ChatService import chat
from .core.config import config

import gradio

def main() -> None:
    print("Hello from chatbot!")
    
    if not config.GEMINI_API_KEY and not config.OPEN_ROUTER_API_KEY:
        print("❌ Error: No API keys found!")
        print("Please set OPEN_ROUTER_API_KEY or GEMINI_API_KEY in your .env file")
        return



gradio.ChatInterface(chat, type="messages").launch()



