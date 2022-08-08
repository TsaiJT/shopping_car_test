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

# cart_table = Table("cart", Base.metadata,
#     Column("user_id", String(255), ForeignKey("users.id"), primary_key=True),
#     Column("product_id", String(255), ForeignKey("products.id"), primary_key=True)
# )


# checkout_table = Table("checkout", Base.metadata,
#     Column("user_id", String(255), ForeignKey("users.id"), primary_key=True),
#     Column("order_id", String(255), ForeignKey("orders.id"), primary_key=True)
# )


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

    # products = relationship("Product",
    #                     secondary=cart_table,
    #                     backref=backref("users", lazy="dynamic")
    #                     )

    # orders = relationship("Order",
    #                     secondary=checkout_table,
    #                     backref=backref("users", lazy="dynamic")
    #                     )


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
    cart_id = Column(String(255), index=True)
    buy_at = Column(DateTime, server_default=func.now())


engine = create_engine(settings.POSTGRES_DATABASE_URI)

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)