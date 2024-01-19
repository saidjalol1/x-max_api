from config import Base
from sqlalchemy import Column,Integer, String, ForeignKey, Boolean, Text, Float, DateTime, JSON
from sqlalchemy.orm import relationship


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









