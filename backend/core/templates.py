from typing import Dict

def render_template(body: str, variables: Dict[str, str] | None) -> str:
    """
    Substitui marcadores {{nome}} no body por valores do dict.
    Se alguma variável não existir, deixa o marcador como está.
    """
    if not variables:
        return body
    
    result = body
    for key, value in variables.items():
        placeholder = "{{" + key + "}}"
        result = result.replace(placeholder, value)
    return result