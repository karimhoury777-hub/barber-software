from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Service(Base):
    __tablename__ = "services_v2"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, default="General") # New category field
    description = Column(String, nullable=True)
    base_price = Column(Float)
    is_active = Column(Boolean, default=True)

    promotions = relationship("Promotion", back_populates="service")

class Promotion(Base):
    __tablename__ = "promotions_v2"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    discount_percentage = Column(Float)
    start_date = Column(DateTime, default=datetime.datetime.utcnow)
    end_date = Column(DateTime)
    service_id = Column(Integer, ForeignKey("services_v2.id"), nullable=True)
    
    service = relationship("Service", back_populates="promotions")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    customer_phone = Column(String)
    services_ordered = Column(String) # A comma-separated list of what they bought
    total_price = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)