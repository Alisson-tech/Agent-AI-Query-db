from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from database.connection import Base


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    preco = Column(Float)

    vendas = relationship("Venda", back_populates="produto")
