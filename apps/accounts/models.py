from db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship

class Account(Base):
    name = Column(String(50), nullable=False)
    currency_id = Column(Integer, ForeignKey("currencies.id"))
    currency = relationship("Currency")
    balance = Column(DECIMAL(14,2), nullable=False, default=0.00)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="accounts")
