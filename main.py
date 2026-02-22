from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

class ProductCreate(BaseModel):
    name: str
    description: str
    ingredients: str

app = FastAPI()

DATABASE_URL = "sqlite:///./beauty.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker( bind = engine )
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    ingredient = Column(Text)

Base.metadata.create_all(bind = engine)

class ProductCreate(BaseModel):
    name: str
    description: str
    ingredients: str


@app.post("/add_product")
def add_product(product: ProductCreate):
    db = SessionLocal()

    existing_product = db.query(Product).filter(Product.name == product.name).first()
    if existing_product :
        db.close()
        return {"error": "Product already exist"}
    new_product = Product(
        name = product.name,
        description = product.description,
        ingredient = product.ingredient
    )

    db.add(new_product)
    db.commit()
    db.close()
    return {"status": "Product save to database"}

@app.get("/product/{name}")
def get_product(name: str):
    db = SessionLocal()

    product = db.query(Product).filter(Product.name == name).first()
    db.close()

    if not product:
        return {"error": "Product not found"}

    return {
        "name": product.name,
        "description": product.description,
        "ingredients": product.ingredients
    }
