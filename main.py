from database.initialData import insert_initial_data
from services.agentService import get_data_by_llm
from database.connection import engine, Base


def init_db():
    Base.metadata.create_all(bind=engine)


def get_question():
    print("=== Consultor SQL com LLM ===")
    pergunta = input("Digite sua consulta em linguagem natural: ")

    try:
        resultado = get_data_by_llm(pergunta)
        print("\nResultado:")
        for linha in resultado:
            print(linha)
    except Exception as e:
        print("Erro:", e)


if __name__ == "__main__":
    init_db()
    insert_initial_data()
    get_question()
