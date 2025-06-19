from datetime import datetime, timedelta
import spacy
import os
import re

model_path = os.path.abspath("agent/intern/trainer/model_classifier")

nlp = spacy.load(model_path)

FIELDS_MODELS = {
    "produto": {
        "nome": "prompt",
        "preco": "numero"
    },
    "venda": {
        "quantidade": "numero",
        "preco_unitario": "numero",
        "preco_total": "numero",
        "data": "data"
    }
}

VALID_MODELS = {"produto", "venda"}

OPERATOR = {
    "maior que": ">",
    "acima de": ">",
    "menor que": "<",
    "abaixo de": "<",
    "igual a": "=",
    "iguais a": "=",
    "exatamente": "=",
    "antes de": "<=",
    "depois de": ">=",
    "em": "="
}


def get_query_filters(prompt):
    intent = predict_intent(prompt)
    filters = extract_filters(prompt)

    return (intent, filters)


def predict_intent(prompt):
    doc = nlp(prompt)
    intent = max(doc.cats, key=doc.cats.get)
    return intent


def extract_date(value):
    for fmt in ("%d-%m-%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
        except:
            pass
    return value


def extract_filters(prompt):
    prompt = prompt.lower()
    filters = []

    used_model = next(
        (m for m in VALID_MODELS if m in prompt or f"{m}s" in prompt), None)
    if not used_model:
        return filters

    fields = FIELDS_MODELS[used_model]

    interval = re.search(
        r"(\d{2}[-/]\d{2}[-/]\d{4})\s+(?:a|e|até)\s+(\d{2}[-/]\d{2}[-/]\d{4})", prompt
    )
    if interval and "data" in fields:
        filters.append({
            "campo": "data",
            "operador": ">=",
            "value": extract_date(interval.group(1)),
            "type": "data"
        })
        filters.append({
            "campo": "data",
            "operador": "<=",
            "value": extract_date(interval.group(2)),
            "type": "data"
        })

    doc = nlp(prompt)
    for token in doc:
        if token.text in fields:
            type = fields[token.text]
            windown = doc[max(token.i - 3, 0): token.i + 4].text
            for op_prompt, op_simbolo in OPERATOR.items():
                if op_prompt in windown:
                    match_value = re.search(
                        rf"{re.escape(op_prompt)} ([\w/.,-]+)", windown)
                    if match_value:
                        gross_value = match_value.group(1)
                        value = extract_date(gross_value) if type == "data" else float(
                            gross_value.replace(",", "."))
                        filters.append({
                            "campo": token.text,
                            "operador": op_simbolo,
                            "value": value,
                            "type": type
                        })

    return filters
