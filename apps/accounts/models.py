from db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

class Account(Base):
    name = Column(String(50), nullable=False)
    currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=False)
    currency = relationship("Currency")
    balance = Column(BigInteger, nullable=False, default=0)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="accounts")
