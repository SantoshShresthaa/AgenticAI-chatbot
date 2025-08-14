"""Simple example of using the chatbot."""

import asyncio
import os
from src.chatbot.factory import LLMFactory
from src.chatbot.agent import ChatAgent

async def simple_chat_example():
    """Simple command-line chat example."""
    
    # Set your API key here or in environment variable
    api_key = os.getenv("OPENAI_API_KEY") or "your-api-key-here"
    
    if api_key == "your-api-key-here":
        print("Please set your OPENAI_API_KEY environment variable or update the api_key in this file")
        return
    
    try:
        # Create LLM provider
        provider = LLMFactory.create_provider("openai", api_key)
        
        # Create agent
        agent = ChatAgent(provider, "You are a helpful and friendly AI assistant.")
        
        print("🤖 Chatbot ready! Type 'quit' to exit.")
        print("-" * 50)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            try:
                response = await agent.chat(user_input)
                print(f"\n🤖 Assistant: {response}")
            except Exception as e:
                print(f"❌ Error: {e}")
    
    except Exception as e:
        print(f"❌ Failed to start chatbot: {e}")

if __name__ == "__main__":
    asyncio.run(simple_chat_example())

