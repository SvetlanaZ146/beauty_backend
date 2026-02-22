from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# ---------------- Pydantic модель для JSON ----------------
class ProductCreate(BaseModel):
    name: str
    description: str
    ingredients: str

# ---------------- FastAPI ----------------
app = FastAPI()

# ---------------- SQLite ----------------
DATABASE_URL = "sqlite:///./beauty.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ---------------- Таблиця ----------------
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    ingredients = Column(Text)  # <-- виправлено на 'ingredients'

# Створення таблиці
Base.metadata.create_all(bind=engine)

# ---------------- POST ----------------
@app.post("/add_product")
def add_product(product: ProductCreate):
    db = SessionLocal()

    existing_product = db.query(Product).filter(Product.name == product.name).first()
    if existing_product:
        db.close()
        return {"error": "Product already exists"}

    new_product = Product(
        name=product.name,
        description=product.description,
        ingredients=product.ingredients  # <-- тут теж 'ingredients'
    )

    db.add(new_product)
    db.commit()
    db.close()
    return {"status": "Product saved to database"}

# ---------------- GET ----------------
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