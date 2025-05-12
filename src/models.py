from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
import datetime

Base = declarative_base()

class Trade(Base):
    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, nullable=False)            # p.ej. 'AAPL', 'BTC'
    quantity = Column(Float, nullable=False)           # unidades compradas
    price = Column(Float, nullable=False)              # precio por unidad
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return (f"<Trade(id={self.id}, symbol='{self.symbol}', "
                f"qty={self.quantity}, price={self.price}, date={self.date})>")