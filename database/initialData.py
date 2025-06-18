from datetime import datetime, timezone, timedelta
from database.connection import SessionLocal
from models import Produto, Venda


def insert_initial_data():
    session = SessionLocal()
    try:
        print("Inserindo dados iniciais...")

        produto1 = Produto(nome="Notebook Dell XPS 15", preco=8500.00)
        produto2 = Produto(nome="Monitor LG Ultrawide", preco=1500.00)
        produto3 = Produto(nome="Teclado Mecânico HyperX", preco=450.00)

        session.add_all([produto1, produto2, produto3])
        session.commit()

        produtos = [produto1, produto2, produto3]

        vendas = []

        base_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
        for i in range(20):
            produto = produtos[i % 3]
            quantidade = 1 if i % 2 == 0 else 2
            data_venda = base_date + timedelta(days=30 * (i // 3), hours=i)

            venda = Venda(
                id_produto=produto.id,
                quantidade=quantidade,
                preco_unitario=produto.preco,
                preco_total=produto.preco * quantidade,
                data=data_venda
            )
            vendas.append(venda)

        session.add_all(vendas)
        session.commit()

    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()
