from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    base_price = Column(Float)
    is_active = Column(Boolean, default=True)

    # Link to any active promotions for this specific service
    promotions = relationship("Promotion", back_populates="service")

class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    discount_percentage = Column(Float)  # e.g., 15.0 for 15% off
    start_date = Column(DateTime, default=datetime.datetime.utcnow)
    end_date = Column(DateTime)
    
    # Foreign key linking the promotion to a specific service
    service_id = Column(Integer, ForeignKey("services.id"), nullable=True)
    
    service = relationship("Service", back_populates="promotions")