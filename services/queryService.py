from sqlalchemy import select, text, func
from database import SessionLocal


OPERADOR_MAP = {
    ">": lambda col, val: col > val,
    "<": lambda col, val: col < val,
    ">=": lambda col, val: col >= val,
    "<=": lambda col, val: col <= val,
    "=": lambda col, val: col == val
}


def raw_sql(sql: str) -> list[dict]:
    try:
        with SessionLocal() as session:
            resultado = session.execute(text(sql))
            colunas = resultado.keys()
            return [dict(zip(colunas, row)) for row in resultado.fetchall()]
    except Exception as e:
        raise RuntimeError(f"Erro ao executar SQL: {e}")


def buscar(modelo, filtros: list[dict]) -> list[dict]:
    try:
        with SessionLocal() as db:
            colunas = list(modelo.__table__.columns)
            stmt = select(*colunas)
            for f in filtros:
                coluna = getattr(modelo, f["campo"], None)
                if coluna and f["operador"] in OPERADOR_MAP:
                    stmt = stmt.where(
                        OPERADOR_MAP[f["operador"]](coluna, f["valor"]))
            resultado = db.execute(stmt)
            nomes_colunas = resultado.keys()
            return [dict(zip(nomes_colunas, row)) for row in resultado.fetchall()]
    except Exception as e:
        raise RuntimeError(
            f"Erro ao buscar dados de {modelo.__tablename__}: {e}")


def agregado(modelo, filtros: list[dict], campo_agregado) -> list[dict]:
    try:
        with SessionLocal() as db:
            stmt = select(func.sum(campo_agregado).label("total"))
            for f in filtros:
                coluna = getattr(modelo, f["campo"], None)
                if coluna and f["operador"] in OPERADOR_MAP:
                    stmt = stmt.where(
                        OPERADOR_MAP[f["operador"]](coluna, f["valor"]))
            resultado = db.execute(stmt)
            colunas = resultado.keys()
            return [dict(zip(colunas, row)) for row in resultado.fetchall()]
    except Exception as e:
        raise RuntimeError(
            f"Erro ao calcular agregação de {modelo.__tablename__}: {e}")
