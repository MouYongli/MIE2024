import json

from data_model.data_model import BaseModel


def simplify_schema(schema):
    """
    Simplifies a JSON Schema generated by pydantic into my desired format.

    Args:
        schema (dict): the JSON schema

    Returns:
        dict: the JSON schema with definitions inlined and other simplifications
    """

    def replace_ref(obj):
        if isinstance(obj, dict):
            if "$ref" in obj:
                ref_path = obj["$ref"]
                def_name = ref_path.split("/")[-1]
                definition = schema["$defs"][def_name]
                # Remove the 'title' key
                definition.pop("title", None)
                return definition
            else:
                new_obj = {k: replace_ref(v) for k, v in obj.items()}
                # Remove the 'title' key from all dictionaries
                new_obj.pop("title", None)
                # Simplify the 'allOf' construction for enums
                if "allOf" in new_obj:
                    enum_details = new_obj["allOf"][0]
                    if "enum" in enum_details:
                        new_obj.update(enum_details)
                        del new_obj["allOf"]
                return new_obj
        elif isinstance(obj, list):
            return [replace_ref(i) for i in obj]
        else:
            return obj

    inlined_schema = replace_ref(schema)
    if "$defs" in inlined_schema:
        del inlined_schema["$defs"]
    return inlined_schema


def get_json_schema(data_model: BaseModel):
    """
    Get the JSON schema as a dictionary.

    Returns:
        dict: the JSON schema as a dictionary
    """
    schema = simplify_schema(data_model.model_json_schema())

    return json.dumps(schema, indent=4, ensure_ascii=False)
