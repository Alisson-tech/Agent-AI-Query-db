from sqlalchemy import select, text, func
from database import SessionLocal
from sqlalchemy.dialects import postgresql


OPERATOR_MAP = {
    ">": lambda col, val: col > val,
    "<": lambda col, val: col < val,
    ">=": lambda col, val: col >= val,
    "<=": lambda col, val: col <= val,
    "=": lambda col, val: col == val
}


def raw_sql(sql: str) -> list[dict]:
    try:
        print("\nQuery Gerada: ")
        print(sql)
        with SessionLocal() as session:
            result = session.execute(text(sql))
            columns = result.keys()
            return [dict(zip(columns, row)) for row in result.fetchall()]
    except Exception as e:
        raise RuntimeError(f"Erro ao executar SQL: {e}")


def get_list_data(modelo, filtros: list[dict]) -> list[dict]:
    try:
        with SessionLocal() as db:
            columns = list(modelo.__table__.columns)
            stmt = select(*columns)
            for f in filtros:
                column = getattr(modelo, f["campo"], None)
                if column and f["operador"] in OPERATOR_MAP:
                    stmt = stmt.where(
                        OPERATOR_MAP[f["operador"]](column, f["valor"]))

            print("\nQuery Gerada: ")
            print(stmt.compile(dialect=postgresql.dialect(),
                  compile_kwargs={"literal_binds": True}))
            result = db.execute(stmt)
            columns_name = result.keys()
            return [dict(zip(columns_name, row)) for row in result.fetchall()]
    except Exception as e:
        raise RuntimeError(
            f"Erro ao buscar dados de {modelo.__tablename__}: {e}")


def get_aggregate_data(modelo, filtros: list[dict], campo_agregado) -> list[dict]:
    try:
        with SessionLocal() as db:
            stmt = select(func.sum(campo_agregado).label("total"))
            for f in filtros:
                column = getattr(modelo, f["campo"], None)
                if column and f["operador"] in OPERATOR_MAP:
                    stmt = stmt.where(
                        OPERATOR_MAP[f["operador"]](column, f["valor"]))

            print("\nQuery Gerada: ")
            print(stmt.compile(dialect=postgresql.dialect(),
                  compile_kwargs={"literal_binds": True}))
            result = db.execute(stmt)
            columns = result.keys()
            return [dict(zip(columns, row)) for row in result.fetchall()]
    except Exception as e:
        raise RuntimeError(
            f"Erro ao calcular agregação de {modelo.__tablename__}: {e}")
