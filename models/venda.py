from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.connection import Base
from datetime import datetime, timezone


class Venda(Base):
    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True, index=True)
    id_produto = Column(Integer, ForeignKey("produtos.id"))
    quantidade = Column(Integer)
    preco_unitario = Column(Float)
    preco_total = Column(Float)
    data = Column(DateTime, default=datetime.now(timezone.utc))

    produto = relationship("Produto", back_populates="vendas")
