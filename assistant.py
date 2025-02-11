# assistant.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from utils.printer import Printer
from prompt_templates import get_patient_prompt_template_text
from dotenv import load_dotenv

import warnings


import os, getpass

def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

_set_env("OPENAI_API_KEY")


def warn(message, category=None, stacklevel=1):
    # Custom warning function implementation
    print(f"Warning: {message}")

warnings.warn = warn

class VirtualHealthAssistant:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        
        # Initialize the OpenAI model with dynamic response generation
        self.llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.75,  # Increase creativity and randomness
            model_kwargs={
                "top_p": 0.85,  # Refine choices for more varied output
                "frequency_penalty": 0.7,  # Limit repetitive phrases
                "presence_penalty": 0.4  # Encourage new ideas and unique responses
            }
        )

        
        # Define the prompt template for patient interaction in French
        patient_prompt_template = get_patient_prompt_template_text()
        self.prompt_template = PromptTemplate.from_template(patient_prompt_template)

        # Initialize memory to keep track of the conversation
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="text")

        # Create a simple LLM chain for conversation
        self.chat_chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt_template,
            memory=self.memory
        )

        # Initialize the Printer class
        self.printer = Printer()
