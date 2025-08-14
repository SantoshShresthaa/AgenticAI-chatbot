
from pydantic import BaseModel
from chatbot.fileParser import parser
from chatbot.utils import prompt
from .core.config import config
from openai import OpenAI

import gradio

def main() -> None:
    print("Hello from chatbot!")
    
    if not config.GEMINI_API_KEY and not config.OPEN_ROUTER_API_KEY:
        print("❌ Error: No API keys found!")
        print("Please set OPEN_ROUTER_API_KEY or GEMINI_API_KEY in your .env file")
        return



def chat(message, history):

    # Extract the content from the uploaded resume
    extracted_resume_content = parser.pdfParser()

    # Extract summary from the txt file
    self_intro_summary = parser.summeryExtractor()

    # Prompt Section 
    system_prompt = prompt.getSystemPrompt(self_intro_summary, extracted_resume_content)
    
    messages = [{"role" : "system", "content" : system_prompt}] + history + [{"role" : "user", "content" : message}]

    # LLM Call for google
    gemini = OpenAI(
        api_key= config.GEMINI_API_KEY,
        base_url= config.GEMINI_BASE_URL
        )

    response = gemini.chat.completions.create(
        model=config.GEMINI_MODEL, 
        messages=messages
        )

    return response.choices[0].message.content


def evaluator_user_prompt(reply, message, history):
    user_prompt = f"Here's the conversation between the User and the Agent: \n\n{history}\n\n"
    user_prompt += f"Here's the latest message from the User: \n\n{message}\n\n"
    user_prompt += f"Here's the latest response from the Agent: \n\n{reply}\n\n"
    user_prompt += "Please evaluate the response, replying with whether it is acceptable and your feedback."

    return user_prompt

class Evaluation(BaseModel):
    is_acceptable:bool
    feedback:str
    
def evaluate(reply,message,history) -> Evaluation:
    # Extract the content from the uploaded resume
    extracted_resume_content = parser.pdfParser()

    # Extract summary from the txt file
    self_intro_summary = parser.summeryExtractor()

    evaluator_system_prompt = prompt.getEvaluatorSystemPrompt(self_intro_summary, extracted_resume_content)

    messages=[{"role": "system", "content": evaluator_system_prompt}] + [{"role": "user", 'content': evaluator_user_prompt(reply, message, history)}]

    openai = OpenAI(
        api_key=config.OPEN_ROUTER_API_KEY,
        base_url=config.OPEN_ROUTER_BASE_URL
    )

    response = openai.beta.chat.completions.parse(
        # model="deepseek/deepseek-chat-v3-0324:free",
        model="openai/gpt-oss-20b:free",

        messages=messages,
        response_format=Evaluation
    )

    return response.choices[0].message.parsed


def rerun(reply, message, history, feedback):
        # Extract the content from the uploaded resume
    extracted_resume_content = parser.pdfParser()

    # Extract summary from the txt file
    self_intro_summary = parser.summeryExtractor()

    # Prompt Section 
    system_prompt = prompt.getSystemPrompt(self_intro_summary, extracted_resume_content)


    updated_system_prompt = system_prompt + "\n\n## Previous answer rejected\nYou just tried to reply, but the quality control rejected your reply\n"
    updated_system_prompt += f"## Your attempted answer:\n{reply}\n\n"
    updated_system_prompt += f"## Reason for rejection:\n{feedback}\n\n"
    messages = [{"role": "system", "content": updated_system_prompt}] + history + [{"role": "user", "content": message}]

    # LLM Call for google
    gemini = OpenAI(
        api_key= config.GEMINI_API_KEY,
        base_url= config.GEMINI_BASE_URL
        )

    response = gemini.chat.completions.create(model="gemini-2.0-flash", messages=messages)

    return response.choices[0].message.content
    

gradio.ChatInterface(chat, type="messages").launch()



