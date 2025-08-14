from openai import OpenAI
from chatbot.core.config import config
from chatbot.services.EvaluatorService import evaluate
from chatbot.services.UserProfileService import getUserProfile
from chatbot.utils import prompt


def chat(message, history):

    # Extract the content from the uploaded resume
    extracted_resume_content, self_intro_summary = getUserProfile()

    # Prompt Section 
    system_prompt = prompt.getSystemPrompt(self_intro_summary, extracted_resume_content)

    if "hello" in message:
        system = system_prompt + "\n\n Everything in your reply should strictly to be in pig latin \
            it is mandatory that you respond only  and entirely in pig latin"
    else:
        system = system_prompt

    
    messages = [{"role" : "system", "content" : system}] + history + [{"role" : "user", "content" : message}]

    # LLM Call for google
    gemini = OpenAI(
        api_key= config.GEMINI_API_KEY,
        base_url= config.GEMINI_BASE_URL
        )

    response = gemini.chat.completions.create(
        model=config.GEMINI_MODEL, 
        messages=messages
        )

    reply = response.choices[0].message.content

    evaluator_system_prompt = prompt.getEvaluatorSystemPrompt(self_intro_summary, extracted_resume_content)

    evaluation = evaluate(evaluator_system_prompt, reply, message, history)

    if evaluation.is_acceptable:
        print ("Passed evaluation - returning reply")
    else:
        print("Evaluation failed - re running the prompt.")
        print(evaluation.feedback)

        reply = rerun(reply, message, history, evaluation.feedback)

    return reply;


def rerun(reply, message, history, feedback):

    extracted_resume_content, self_intro_summary = getUserProfile()

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