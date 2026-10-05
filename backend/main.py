from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db
import datetime

# Automatically create tables in your Neon database if they don't exist yet
models.Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application
app = FastAPI(title="Barber Menu API")

@app.post("/services/", response_model=schemas.ServiceResponse)
def create_service(service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    # Convert the incoming schema into a database model and save it
    db_service = models.Service(**service.model_dump())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

@app.get("/services/", response_model=list[schemas.ServiceResponse])
def read_active_services(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Fetch all services where is_active is True
    services = db.query(models.Service).filter(models.Service.is_active == True).offset(skip).limit(limit).all()
    return services

@app.put("/services/{service_id}", response_model=schemas.ServiceResponse)
def update_service(service_id: int, service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    # Find the specific service in the database
    db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
    
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    # Update the values
    db_service.name = service.name
    db_service.description = service.description
    db_service.base_price = service.base_price
    db_service.is_active = service.is_active
    
    db.commit()
    db.refresh(db_service)
    return db_service


@app.post("/promotions/", response_model=schemas.PromotionResponse)
def create_promotion(promo: schemas.PromotionCreate, db: Session = Depends(get_db)):
    db_promo = models.Promotion(**promo.model_dump())
    db.add(db_promo)
    db.commit()
    db.refresh(db_promo)
    return db_promo

@app.get("/promotions/", response_model=list[schemas.PromotionResponse])
def read_active_promotions(db: Session = Depends(get_db)):
    now = datetime.datetime.now()
    # Only return promotions where 'now' is between start and end dates
    promos = db.query(models.Promotion).filter(
        models.Promotion.start_date <= now,
        models.Promotion.end_date >= now
    ).all()
    return promos


@app.post("/orders/", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order