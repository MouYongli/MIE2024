import os
import sys

import torch
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI
from transformers import AutoModelForCausalLM, AutoTokenizer

sys.path.insert(0, "..")
from hugging_face_adapter.langchain_integration import HuggingFaceLocal
from hugging_face_adapter.utils import get_model_and_tokenizer, get_pipeline


def get_openai_api_key():
    """
    Get the OpenAI API key from the environment variables.

    Returns:
        str: The OpenAI API key.
    """
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return openai_api_key


def hf_get_pipeline(model: str):
    """
    Get the language model pipeline.

    Args:
        model (str): The name of the HuggingFace model.

    Returns:
        object: The transformers pipeline.
    """
    model, tokenizer = get_model_and_tokenizer(
        model_name=model,
        local_dir="models",
        model_class=AutoModelForCausalLM,
        tokenizer_class=AutoTokenizer,
    )
    pipe = get_pipeline(model, tokenizer, "text-generation", torch.float16)
    return pipe


def run_llm(
    prompt_template: PromptTemplate,
    prompt_variables_list: list[dict],
    mode: str,
    model: str | None = None,
    output_to_string: object | None = None,
    gpu_index: int | None = None,
):
    """
    Run the Language Model (LLM) with the given prompt template and prompt variables.

    Args:
        prompt_template (PromptTemplate): The prompt template.
        prompt_variables (dict): The variables for the prompt.
        mode (str): The type of LLM to be run (OpenAI/HuggingFace/Ollama).
        model (str, optional): The name of the model. Required when mode is "OpenAI" or "HuggingFace".
        output_to_string (object, optional): The function to convert the model output to a string. Required when mode is "HuggingFace".

    Returns:
        str: The response from the LLM.
    """
    match mode:
        case "OpenAI":
            llm = ChatOpenAI(
                openai_api_key=get_openai_api_key(),
                temperature=0.0001,
                model_name=model if model else "gpt-4",
            )
        case "HuggingFace":
            if model is None or output_to_string is None:
                raise ValueError(
                    "model_name and output_to_string must be provided when mode=HuggingFace"
                )
            llm = HuggingFaceLocal(
                model_name=model, output_to_string=output_to_string, gpu_index=gpu_index
            )
        case "Ollama":
            if model is None:
                raise ValueError("model must be provided when mode=Ollama")
            llm = Ollama(model=model)

    llm_chain = LLMChain(prompt=prompt_template, llm=llm)

    responses = []
    for prompt_variables in prompt_variables_list:
        resp = llm_chain.invoke(prompt_variables)
        responses.append(resp)

    return responses
