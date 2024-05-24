import os

import torch
from dotenv import load_dotenv
from torch import cuda
from transformers import pipeline


def get_hugging_face_token():
    """
    Get the HuggingFace access token from the environment variables.

    Returns:
        str: The HuggingFace access token.
    """
    load_dotenv()
    hugging_face_token = os.getenv("HUGGING_FACE_TOKEN")
    return hugging_face_token


def get_model_and_tokenizer(
    model_name: str,
    local_dir: str,
    model_class: object,
    tokenizer_class: object,
) -> tuple:
    """
    Get the model and tokenizer for a given HuggingFace model.

    Args:
        model_name (str): The name of the HuggingFace model.
        local_dir (str): The local directory to look for the model files.
        model_class (object): The appropriate model class from the transformers library.
        tokenizer_class (object): The appriopriate tokenizer class from the transformers library.
        access_token (str): The access token for the HuggingFace account.

    Returns:
        tuple: The model and tokenizer.
    """
    model_path = os.path.join(local_dir, model_name)
    access_token = get_hugging_face_token()

    if not os.path.exists(model_path):
        # If the model is not available locally yet, download it
        print(f"------- model {model_name} not found: downloading it -------")
        model = model_class.from_pretrained(model_name, token=access_token)
        model.save_pretrained(model_path)
        tokenizer = tokenizer_class.from_pretrained(model_name, token=access_token)
        tokenizer.save_pretrained(model_path)
    else:
        # If the model is already available locally, load it from the local path
        print(f"------- model {model_name} found: loading it -------")
        model = model_class.from_pretrained(
            model_path, device_map="auto", low_cpu_mem_usage=True
        )
        tokenizer = tokenizer_class.from_pretrained(model_path)
    return model, tokenizer


def get_pipeline(
    model: object,
    tokenizer: object,
    task: str = "text-generation",
    precision: object = torch.float16,
    gpu_index: int = None,
):
    """
    Get the HuggingFace pipeline for a given model and tokenizer.

    Args:
        model (object): The HuggingFace model.
        tokenizer (object): The HuggingFace tokenizer.
        task (str): The task for the pipeline.
        precision (object): The precision for the pipeline.
        gpu_index (int): The index of the GPU to use.

    Returns:
        object: The HuggingFace pipeline.
    """
    if cuda.is_available():
        cuda.empty_cache()
        # if gpu_index:
        #     device = f"cuda:{gpu_index}"
        # else:
        #     device = f"cuda:{cuda.current_device()}"
        pipe = pipeline(
            task=task,
            model=model,
            tokenizer=tokenizer,
            torch_dtype=precision,
            # device=device,
            max_new_tokens=4096,
            kwargs={"do_sample": False},
        )
    else:
        pipe = pipeline(
            task=task,
            model=model,
            tokenizer=tokenizer,
            torch_dtype=precision,
            max_new_tokens=4096,
            kwargs={"do_sample": False},
        )

    device_used = pipe.model.device
    print(f"------- using device: {device_used} -------")

    return pipe
