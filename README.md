# PoC Tool for Tumor Documentation of German Pathology Reports

This repository demonstrates how pathology reports at the Center for Integrated Oncology Aachen can be structured using either closed-source models such as GPT-4 or open-source models such as Mixtral-8x7b-Instruct. The input has to be a set of pathology reports describing a biopsy of a breast-cancer patient and the output will be a JSON object containing the extracted features as well as a CSV file that can be imported into the proprietary tumor documentation system Onkostar. The main goals of this tools are:
- to demonstrate how complex NLP tasks can be performed via prompt engineering of SOTA models to determine the correct values needed for tumor documentation
- to show how an AI-based tool could be integrated into the workflow at the Cancer Registry CIO Aachen

Please note that the tool's prompts were constructed specifically for pathology reports at the hospital in Aachen. Therefore, the performance may be worse for pathology reports from other sources. Specifically, this tool is only intended for pathology reports in German. Also, for privacy reasons we can not provide you with real pathology reports, so please use your own reports and make sure that they are sufficiently pseudonymized when using models via API.

## Repository Structure:
```
.
├── README.md
├── app.py                         # CLI, which can be used with python app.py
├── model_config.py                # Configuration of models that can be used. Add your own models here
├── requirements.txt               # Python dependencies, which can be installed with pip install -r requirements.txt
├── data_model                     
│   ├── data_model.py              # Pydantic model with prompts given as descriptions, implementing a structured data model for pathology reports
│   └── types.py                   # Custom data types
├── hugging_face_adapter
│   ├── langchain_integration.py   # Hugging Face Wrapper, extending Langchain's LLM class
│   └── utils.py                   # Wrapper for Hugging Face functions
├── pipeline_stages
│   ├── _1_text_extraction.py      # Extracting text of docx and pdf documents
│   ├── _2_prompt_template.py      # Prompt template
│   ├── _3_json_schema.py          # JSON utilities
│   ├── _4_LLMManager.py           # Wrapper for LLM inference
│   └── _5_onkostar_converter.py   # Creating a CSV that can be imported into Onkostar
└── dataset                        # Add your own dataset of pathology reports here
```

## Getting Started:

To run the PoC app locally, follow these steps:

1. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Create an environment file .env that contains the variables ```OPENAI_API_KEY``` and ```HUGGING_FACE_TOKEN``` containing your API keys.

3. Please add your own example pathology reports. Therefore, create the folder structure ```dataset\test\patient_1\entity_1\document_1.docx``` where ```document_1.docx```, ```document_2.docx```,... are the pathology reports of the pathological examinations of tumor entity 1 of patient 1. Of course, you can add add more entities (```entity_n```) and patients (```patient_n```).

4. Run the app with:
    ```
    python app.py --model model_name --patient patient_id --entity entity_id
    ```
    For example, use ```--model gpt-4 --patient 1 --entity 1``` to create the documentation for entity_1 of patient_1 using the OpenAI API with gpt-4. To use other OpenAI 
    endpoints or local models, please add the model to ```model_config.py``` or use one of the existing models in there.

## Architecture of our Tool:

![image](https://github.com/MouYongli/MIE2024/assets/56689318/0e57660f-43dc-4a6c-9c9a-ab17bbccd72d)
