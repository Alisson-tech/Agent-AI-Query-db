from database.initialData import insert_initial_data
from services.agentService import get_model_and_data
from database.connection import engine, Base


def init_db():
    Base.metadata.create_all(bind=engine)


def get_question():
    print("=== Consultor SQL ===")
    flag = input(
        "Escolhar o modelo a utilizar (1 ou 2):\n1-LLM LLMA3 SQL DECODER (SERVIÇO EXTERNO)\n2- AGENT SPACY (SERVIÇO INTERNO)\n")
    prompt = input("\nDigite sua consulta em linguagem natural: ")

    try:
        resultado = get_model_and_data(int(flag), prompt)
        print("\nResultado:")
        for linha in resultado:
            print(linha)
    except Exception as e:
        print("Erro:", e)


if __name__ == "__main__":
    init_db()
    insert_initial_data()
    get_question()
