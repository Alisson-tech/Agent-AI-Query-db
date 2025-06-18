from sqlalchemy import text
from database import SessionLocal


def raw_sql(sql: str) -> list[dict]:
    try:
        with SessionLocal() as session:
            resultado = session.execute(text(sql))
            colunas = resultado.keys()
            return [dict(zip(colunas, row)) for row in resultado.fetchall()]
    except Exception as e:
        raise RuntimeError(f"Erro ao executar SQL: {e}")
