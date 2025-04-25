model_config = {
    "mistral": {
        "model_name": "mistralai/Mistral-7B-Instruct-v0.2",
        "begin_tokens": "[INST]",
        "end_tokens": "[/INST]",
        "mode": "HuggingFace",
        "output_to_string": lambda x: x[0]["generated_text"]
        .split("[/INST]")[-1]
        .strip(),
    },
    "mixtral": {
        "model_name": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "begin_tokens": "[INST]",
        "end_tokens": "[/INST]",
        "mode": "HuggingFace",
        "output_to_string": lambda x: x[0]["generated_text"]
        .split("[/INST]")[-1]
        .strip(),
    },
    "llama-7b": {
        "model_name": "meta-llama/Llama-2-7b-chat-hf",
        "begin_tokens": "[INST]",
        "end_tokens": "[/INST]",
        "mode": "HuggingFace",
        "output_to_string": lambda x: x[0]["generated_text"]
        .split("[/INST]")[-1]
        .strip(),
    },
    "llama-13b": {
        "model_name": "meta-llama/Llama-2-13b-chat-hf",
        "begin_tokens": "[INST]",
        "end_tokens": "[/INST]",
        "mode": "HuggingFace",
        "output_to_string": lambda x: x[0]["generated_text"]
        .split("[/INST]")[-1]
        .strip(),
    },
    "llama-70b": {
        "model_name": "meta-llama/Llama-2-70b-chat-hf",
        "begin_tokens": "[INST]",
        "end_tokens": "[/INST]",
        "mode": "HuggingFace",
        "output_to_string": lambda x: x[0]["generated_text"]
        .split("[/INST]")[-1]
        .strip(),
    },
    "gpt-4": {
        "model_name": "gpt-4",
        "begin_tokens": "",
        "end_tokens": "",
        "mode": "OpenAI",
        "output_to_string": None,
    },
    "gpt-4-turbo": {
        "model_name": "gpt-4-0125-preview",
        "begin_tokens": "",
        "end_tokens": "",
        "mode": "OpenAI",
        "output_to_string": None,
    },
    "gpt-3.5": {
        "model_name": "gpt-3.5-turbo",
        "begin_tokens": "",
        "end_tokens": "",
        "mode": "OpenAI",
        "output_to_string": None,
    },
}
