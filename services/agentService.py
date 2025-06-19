from agent.extern.llma3Sqldecoder import sql_generate
from services.queryService import raw_sql, buscar, agregado
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
    intencao, filtros = get_query_filters(prompt)

    if intencao == "listar_produtos":
        return buscar(Produto, filtros)

    elif intencao == "listar_vendas":
        return buscar(Venda, filtros)

    elif intencao == "quantidade_produtos_vendidos":
        return agregado(Venda, filtros, Venda.quantidade)

    elif intencao == "valor_total_vendido":
        return agregado(Venda, filtros, Venda.preco_total)

    return []
