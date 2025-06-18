from datetime import datetime, timedelta
import spacy
import os
import re

model_path = os.path.abspath("agent/intern/trainer/model_classifier")

nlp = spacy.load(model_path)

CAMPOS_MODELS = {
    "produto": {
        "nome": "texto",
        "preco": "numero"
    },
    "venda": {
        "quantidade": "numero",
        "preco_unitario": "numero",
        "preco_total": "numero",
        "data": "data"
    }
}

MODELOS_VALIDOS = {"produto", "venda"}

OPERADORES = {
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


def get_query_filters(texto):
    intencao = predict_intent(texto)
    filtros = extrair_filtros(texto)

    print('\n\n')
    print(intencao)
    print('\n')
    print(filtros)
    return 'fim'


def predict_intent(texto):
    doc = nlp(texto)
    intent = max(doc.cats, key=doc.cats.get)
    print(f"Intenção: {intent}")
    print(f"Probabilidades: {doc.cats}")
    return intent, doc.cats


def interpretar_data(valor):
    for fmt in ("%d-%m-%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(valor, fmt).strftime("%Y-%m-%d")
        except:
            pass
    return valor


def extrair_filtros(texto):
    texto = texto.lower()
    filtros = []

    # Detecta modelo mencionado no texto
    modelo_usado = next(
        (m for m in MODELOS_VALIDOS if m in texto or f"{m}s" in texto), None)
    if not modelo_usado:
        return filtros

    campos = CAMPOS_MODELS[modelo_usado]

    # Captura intervalo de datas
    intervalo = re.search(
        r"(\d{2}[-/]\d{2}[-/]\d{4})\s+(?:a|e|até)\s+(\d{2}[-/]\d{2}[-/]\d{4})", texto
    )
    if intervalo and "data" in campos:
        filtros.append({
            "campo": "data",
            "operador": ">=",
            "valor": interpretar_data(intervalo.group(1)),
            "tipo": "data"
        })
        filtros.append({
            "campo": "data",
            "operador": "<=",
            "valor": interpretar_data(intervalo.group(2)),
            "tipo": "data"
        })

    doc = nlp(texto)
    for token in doc:
        if token.text in campos:
            tipo = campos[token.text]
            janela = doc[max(token.i - 3, 0): token.i + 4].text
            for op_texto, op_simbolo in OPERADORES.items():
                if op_texto in janela:
                    match_valor = re.search(
                        rf"{re.escape(op_texto)} ([\w/.,-]+)", janela)
                    if match_valor:
                        valor_bruto = match_valor.group(1)
                        valor = interpretar_data(valor_bruto) if tipo == "data" else float(
                            valor_bruto.replace(",", "."))
                        filtros.append({
                            "campo": token.text,
                            "operador": op_simbolo,
                            "valor": valor,
                            "tipo": tipo
                        })

    return filtros
