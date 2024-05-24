from langchain.prompts import PromptTemplate


def get_prompt_template():
    """
    Get the prompt template for the pathology report task.

    Return:
        PromptTemplate: The prompt template.
    """
    prompt_template_text = """{begin_tokens}Ich werde dir im Folgenden ein oder mehrere Dokumente übergeben, die sich auf eine pathologische Untersuchung bei einem Brustkrebspatienten beziehen.
    Deine Antwort soll aus einem JSON-Objekt bestehen, dass die gemeinsamen Informationen aus den Dokumenten enthält.

    Das JSON-Objekt soll folgendem JSON-Schema entsprechen, wobei immer nur Werte ermittelt werden dürfen, die in dem jeweiligen Datentypen erlaubt sind. 
    Also wenn z.B. der Datentyp im JSON-Schema string ist, dann darf der Wert ein beliebiger String sein.
    Wenn allerdings der Datentyp enum ist mit einer Liste von möglichen Werten, darf nur ein Wert aus dieser Liste genommen werden!
    Nimm also dann immer den wahrscheinlichsten Wert aus der Liste. Wenn bei einem Feld kein Wert sicher ermittelt werden kann, ist das Feld wegzulasen.
    In der 'description' erkläre ich dir jeweils, wie du den richtigen Wert ermittelst. Hier ist das JSON-Schema:

    {json_schema}

    Dies sind die Dokumente:
        
    {documents}
        
    Bitte beachte, dass deine Antwort das gesuchte JSON-Objekt sein soll und keine weiteren Informationen wie erklärenden Text beinhalten darf.
    Deine Antwort muss sich also direkt gegen das obige Schema validieren lassen.{end_tokens}"""

    prompt_template = PromptTemplate(
        template=prompt_template_text,
        input_variables=["json_schema", "documents", "begin_tokens", "end_tokens"],
    )

    return prompt_template
