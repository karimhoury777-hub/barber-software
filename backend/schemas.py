from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- SERVICES ---
class ServiceBase(BaseModel):
    name: str
    category: str # Added category
    description: Optional[str] = None
    base_price: float
    is_active: bool = True

class ServiceCreate(ServiceBase):
    pass

class ServiceResponse(ServiceBase):
    id: int
    class Config:
        from_attributes = True

# --- PROMOTIONS ---
class PromotionBase(BaseModel):
    title: str
    discount_percentage: float
    start_date: datetime
    end_date: datetime
    service_id: Optional[int] = None

class PromotionCreate(PromotionBase):
    pass

class PromotionResponse(PromotionBase):
    id: int
    class Config:
        from_attributes = True

# --- ORDERS (NEW) ---
class OrderBase(BaseModel):
    customer_name: str
    customer_phone: str
    services_ordered: str
    total_price: float

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True