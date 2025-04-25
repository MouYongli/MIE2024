from typing import Any, List, Optional

import torch
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from transformers import AutoModelForCausalLM, AutoTokenizer

from hugging_face_adapter.utils import get_model_and_tokenizer, get_pipeline


class HuggingFaceLocal(LLM):
    """
    Custom LLM class for local HuggingFace models to make them invokable by langchain.

    Args:
        model_name (str): The name of the HuggingFace model.
        output_to_string (object): The function to convert the model output to a string.
    """

    pipeline: object
    tokenizer: object
    output_to_string: object

    def __init__(self, model_name: str, output_to_string, gpu_index: int | None = None):
        """
        Initialize the HuggingFaceLocal class.
        Set self.pipeline, self.tokenizer and self.output_to_string.
        """
        super().__init__()
        self.output_to_string = output_to_string
        model, self.tokenizer = get_model_and_tokenizer(
            model_name=model_name,
            local_dir="models",
            model_class=AutoModelForCausalLM,
            tokenizer_class=AutoTokenizer,
        )
        self.pipeline = get_pipeline(
            model, self.tokenizer, "text-generation", torch.float16, gpu_index
        )

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """
        Call the HuggingFace pipeline with the given prompt.
        Called internally by langchain when invoking the LLM.
        """
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")

        prompt_length = len(self.tokenizer.encode(prompt))
        print(f"------- prompt length: {prompt_length} tokens -------")

        response = self.pipeline(prompt, max_new_tokens=8192 - prompt_length)
        response_text = self.output_to_string(response)
        response_length = len(self.tokenizer.encode(response_text))
        print(
            f"------- prompt + response length: {prompt_length + response_length} tokens -------"
        )

        return response_text
