import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import re

load_dotenv()

client = InferenceClient(
    provider="featherless-ai",
    api_key=os.getenv("HUGGINGFACE_API_TOKEN"),
)


def sql_generate(prompt: str) -> str:
    schema_prompt = """
    Considerando o seguinte banco de dados PostgresSql com as tabelas e colunas:

    - produtos(id, nome, preco)
    - vendas(id, id_produto, quantidade, preco_unitario, preco_total, data)

    Gere apenas queries SQL do tipo SELECT, sem modificações ou inserts.
    """

    full_prompt = f"{schema_prompt}\n\n: {prompt}\nSQL:"

    completion = client.chat.completions.create(
        model="defog/llama-3-sqlcoder-8b",
        messages=[
            {
                "role": "user",
                "content": full_prompt
            }
        ],
    )

    sql_result = completion.choices[0].message.content.strip()

    if not _sql_validate(sql_result):
        raise ValueError("Query potencialmente perigosa detectada!")

    return sql_result


def _sql_validate(sql: str) -> bool:
    sql_clean = sql.strip().lower()

    if not sql_clean.startswith("select"):
        return False

    danger_patterns = [
        r"\bdelete\b",
        r"\bdrop\b",
        r"\binsert\b",
        r"\bupdate\b",
        r"\btruncate\b",
        r"--",
        r"\bexec\b",
        r"\bunion\b",
    ]

    for pattern in danger_patterns:
        if re.search(pattern, sql_clean):
            return False

    return True
