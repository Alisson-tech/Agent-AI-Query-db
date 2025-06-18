from agent.extern.llma3Sqldecoder import sql_generate
from services.queryService import raw_sql


def get_data_by_llm(prompt: str) -> list[dict]:

    sql = sql_generate(prompt)
    return raw_sql(sql)
