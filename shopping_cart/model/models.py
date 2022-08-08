# built-in
import uuid

# 3rd
from sqlalchemy import create_engine, Integer, Column, Sequence, String, DateTime, Boolean, Table, ForeignKey, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# module
from config import settings


Base = declarative_base()


def generate_uuid():
    return uuid.uuid4().hex

class User(Base):
    __tablename__ = "users"

    id = Column(String(255), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    description = Column(String(255))
    create_at = Column(DateTime, server_default=func.now())
    is_block = Column(Boolean, nullable=False, default=False)


class Product(Base):
    __tablename__ = "products"

    id = Column(String(255), primary_key=True, default=generate_uuid)
    name = Column(String(255), unique=True, nullable=False)
    price = Column(Float, nullable=False)
    inventory = Column(Integer, nullable=False)


class CartInfo(Base):
    __tablename__ = "cart_info"

    id = Column(String(255), primary_key=True, default=generate_uuid)
    owner_id = Column(String(255), index=True)
    item_id = Column(String(255), index=True)
    quantity = Column(Integer, nullable=False)
    

class Order(Base):
    __tablename__ = "orders"

    id = Column(String(255), primary_key=True, default=generate_uuid)
    owner_id = Column(String(255), index=True)
    record = Column(JSONB, nullable=False)
    total = Column(Integer, nullable=False)
    buy_at = Column(DateTime, server_default=func.now())


engine = create_engine(settings.POSTGRES_DATABASE_URI)

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)