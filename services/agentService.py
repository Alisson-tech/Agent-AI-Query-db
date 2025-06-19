from agent.extern.llma3Sqldecoder import sql_generate
from services.queryService import raw_sql, get_list_data, get_aggregate_data
from agent.intern.spacyGetKeyWords import get_query_filters
from models import Produto, Venda


def get_model_and_data(flag: int, prompt: str):
    if (flag == 1):
        return _get_data_by_llm(prompt)
    elif (flag == 2):
        return _get_data_by_spacy(prompt)

    raise ValueError(f"Flag inválida: {flag}. Use 1 para LLM ou 2 para spaCy.")


def _get_data_by_llm(prompt: str) -> list[dict]:

    sql = sql_generate(prompt)
    return raw_sql(sql)


def _get_data_by_spacy(prompt: str):
    intent, filters = get_query_filters(prompt)

    if intent == "listar_produtos":
        return get_list_data(Produto, filters)

    elif intent == "listar_vendas":
        return get_list_data(Venda, filters)

    elif intent == "quantidade_produtos_vendidos":
        return get_aggregate_data(Venda, filters, Venda.quantidade)

    elif intent == "valor_total_vendido":
        return get_aggregate_data(Venda, filters, Venda.preco_total)

    return []
