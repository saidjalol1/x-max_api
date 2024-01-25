from config import Base
from sqlalchemy import Column,Integer, String, ForeignKey, Boolean, Text, Float, DateTime, JSON
from sqlalchemy.orm import relationship


class User(Base):
    id = Column(Integer, primary_key=True ,index=True)
    username = Column(String(100))
    email = Column(String(100), nullable=True)
    password = Column(String(8))
    sum_sold = Column(Integer, default=0)
    number_of_product_sold = Column(Integer, default=0)
    salary = Column(String, nullable=True)
    is_superuser = Column(Boolean, default=True)
    is_seller = Column(Boolean, default=False)
    is_cashier = Column(Boolean, default=False)
