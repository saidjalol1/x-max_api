from config import Base
from sqlalchemy import Column,Integer, String, ForeignKey, Boolean, Text, Float, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# Cart Models

    

class Category(Base):
    __tablename__ = "product_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))

    products = relationship("Product", back_populates="category")


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(100))
    product_id = Column(Integer, ForeignKey("products.id"))

    product = relationship("Product", back_populates="images")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    price = Column(Float, default=0)
    amount = Column(Integer, default=0)
    description = Column(Text)
    
    sold_amount = Column(Integer, default=0)
    wishlist_indicator = Column(Integer, default=0)

    category_id = Column(Integer, ForeignKey("product_categories.id"))

    category = relationship("Category", back_populates="products")
    cart_items = relationship("CartItem", back_populates="item")
    # order_item = relationship("OrderItems", back_populates="product")
    wish_list = relationship("WishlistItem", back_populates="item")

    images = relationship("ProductImage", back_populates="product")

    def __repr__(self):
        return self.name
    

class CartItem(Base):
    __tablename__ = "cart_items"
    
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(16))
    quantity = Column(Integer, default=0)
    item_id = Column(Integer, ForeignKey("products.id"))

    item = relationship("Product", back_populates="cart_items")

    def __repr__(self):
        return str(self.id) + "-" + "cart_item"
    

class WishlistItem(Base):
    __tablename__ = "wishlist_item"
    
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(16))
    quantity = Column(Integer, default=0)
    item_id = Column(Integer, ForeignKey("products.id"))

    item = relationship("Product", back_populates="wish_list")

    def __repr__(self):
        return str(self.id) + "-" + "whishlist"
    

# class Order(Base):
#     __tablename__ = "orders"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     surname = Column(String, nullable=True)
#     phone = Column(String)
#     second_phone = Column(String, nullable=True)
#     location = Column(String, nullable=True)
#     address = Column(String, nullable=True)
#     target = Column(String, nullable=True)
#     date_ordered = Column(DateTime(timezone=True), server_default=func.now())
#     paymnet_type = Column(String, default="Naqd")

#     order_items = relationship("OrderItems", back_populates="order")

#     def __repr__(self):
#         return str(self.id) + "-" + "order"


# class OrderItems(Base):
#     __tablename__ = "order_item"
    
#     id = Column(Integer, primary_key=True, index=True)
#     quantity = Column(Integer, default=0)

#     product_id = Column(Integer, ForeignKey("products.id"))
#     order_id = Column(Integer, ForeignKey("orders.id"))

#     product = relationship("Product", back_populates="order_item")
#     order = relationship("Order", back_populates="order_items")

#     def __repr__(self):
#         return str(self.id) + "-" + "order_item"
    
    
# class Expansion(Base):
#     __tablename__ = "expansions"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     amount = Column(Integer)
#     date = Column(String, nullable=True)
#     date_ordered = Column(DateTime(timezone=True), server_default=func.now())









