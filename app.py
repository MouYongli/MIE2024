import argparse
import os
import pprint
import re
from typing import Any

from arrow import get
from langchain.output_parsers import PydanticOutputParser
from openai import models

from data_model.data_model import AllFields, get_data_models
from model_config import model_config
from pipeline_stages._1_text_extraction import read_all_docxs
from pipeline_stages._2_prompt_template import get_prompt_template
from pipeline_stages._3_json_schema import get_json_schema
from pipeline_stages._4_LLMManager import run_llm
from pipeline_stages._5_onkostar_converter import convert_to_onkostar_csv


def main(
    file_paths: dict, model: str, pat_id: int, gpu_index: int | None = None
) -> Any:
    try:
        # Step 1: Extract text from documents
        content_dict = read_all_docxs(file_paths)

        # Step 2: Load prompt template
        prompt_template = get_prompt_template()

        data_models = get_data_models()

        json_schema_list = []
        for data_model in data_models:
            # Step 3: Load JSON schema
            json_schema = get_json_schema(data_model)
            json_schema_list.append(json_schema)

        # Step 4: Run LLM
        parameters = model_config[model]
        llm_outputs = run_llm(
            prompt_template,
            prompt_variables_list=[
                {
                    "documents": content_dict,
                    "json_schema": schema,
                    "begin_tokens": parameters["begin_tokens"],
                    "end_tokens": parameters["end_tokens"],
                }
                for schema in json_schema_list
            ],
            mode=parameters["mode"],
            model=parameters["model_name"],
            output_to_string=parameters["output_to_string"],
            gpu_index=gpu_index,
        )
        response_texts = map(lambda x: x["text"], llm_outputs)

        # Step 5: Parse LLM output to Pydantic Object
        parsed_responses = []
        for data_model, response_text in zip(data_models, response_texts):
            parser = PydanticOutputParser(pydantic_object=data_model)
            parsed_response = parser.parse(response_text)
            parsed_responses.append(parsed_response)
        parsed_responses = AllFields(*parsed_responses)

        # Step 6: Write extracted features to OnkoStar CSV
        csv_file_path = os.path.dirname(file_paths[0])
        convert_to_onkostar_csv(parsed_responses, csv_file_path, model, pat_id)
        return parsed_responses

    except Exception as e:
        # Handle or log error
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", help="name of model to be used", required=True)
    parser.add_argument("--gpu", help="index of gpu to be used")
    parser.add_argument(
        "--patient", help="index of patient to be documented", required=True
    )
    parser.add_argument(
        "--entity", help="index of patient's tumor entity to be documented"
    )
    args = parser.parse_args()

    model = args.model
    if args.gpu:
        gpu_index = args.gpu
    else:
        gpu_index = None
    patient_id = int(args.patient)
    if args.entity:
        entity_id = int(args.entity)
    else:
        entity_id = 1

    file_paths = []

    document_i = 1
    while os.path.isfile(
        os.path.join(
            "dataset",
            "test",
            f"patient_{patient_id}",
            f"entity_{entity_id}",
            f"document_{document_i}.docx",
        )
    ):
        file_paths.append(
            os.path.join(
                "dataset",
                "test",
                f"patient_{patient_id}",
                f"entity_{entity_id}",
                f"document_{document_i}.docx",
            )
        )
        document_i += 1

    parsed_response = main(file_paths, model, gpu_index)
    pprint.pprint(parsed_response.dict())
