from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, CheckConstraint, DateTime
from sqlalchemy.sql import func
Base = declarative_base()

class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255))
    price = Column(Numeric(precision=10, scale=2), nullable=False)
    count = Column(Integer, default=0, nullable=False)

    

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    __table_args__ = (CheckConstraint('count >= 0', name='check_count_positive'),
                      CheckConstraint('price > 0', name='check_price_positive'),)