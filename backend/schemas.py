from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# The base properties every service has
class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    base_price: float
    is_active: bool = True

# Schema used when creating a new service
class ServiceCreate(ServiceBase):
    pass

# Schema used when returning a service (includes the generated ID)
class ServiceResponse(ServiceBase):
    id: int

    class Config:
        from_attributes = True



# --- PROMOTIONS SCHEMAS ---
class PromotionBase(BaseModel):
    title: str
    discount_percentage: float
    start_date: datetime
    end_date: datetime
    service_id: Optional[int] = None  # None means it applies to the whole store

class PromotionCreate(PromotionBase):
    pass

class PromotionResponse(PromotionBase):
    id: int

    class Config:
        from_attributes = True