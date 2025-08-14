from pydantic import BaseModel
from openai import OpenAI

from chatbot.core.config import config
from chatbot.utils.prompt import evaluator_user_prompt

class Evaluation(BaseModel):
    is_acceptable:bool
    feedback:str

def evaluate(evaluator_system_prompt, reply,message,history) -> Evaluation:

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