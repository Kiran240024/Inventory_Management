from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from session import engine,session
import database
from sqlalchemy.orm import Session

app= FastAPI()

app.add_middleware(
     CORSMiddleware,
     allow_origins=["http://localhost:3000"],
     allow_methods=["*"]
)

database.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "Welcome to Telusko Trac"

product=[Product(id=1,name="laptop",description="macbook",price=1000,quantity=2),Product(id=6,name="phone",description="apple",price=5000,quantity=3),Product(id=10,name="watch",description="titan",price=700,quantity=5),Product(id=11,name="television",description="samsung",price=10000,quantity=8)]

def init_db():
    db=session()
    count=db.query(database.Product).count()
    if count==0:
        for i in product:
            db.add(database.Product(**i.model_dump()))
        db.commit()
init_db()

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()



@app.get("/product")
def get_products(db: Session=Depends(get_db)):
    db_prod=db.query(database.Product).all()
    return db_prod

@app.get("/product/{id}")
def id_product(id:int,db: Session=Depends(get_db)):
    db_prod=db.query(database.Product).filter(database.Product.id==id).first()
    if db_prod:
            return db_prod
    return "not found"

@app.post("/product")
def from_user(input:Product,db:Session=Depends(get_db)):
    db.add(database.Product(**input.model_dump()))
    db.commit()
    return input

@app.put("/product/{id}")
def update(input :Product,id:int,db:Session=Depends(get_db)):
    db_prod=db.query(database.Product).filter(database.Product.id==id).first()
    if db_prod:
            db_prod.description=input.description
            db_prod.name=input.name
            db_prod.quantity=input.quantity
            db_prod.price=input.price
            db.commit()
            return "Added Successfully"
    else:
        return "Not Added Successfullly"

@app.delete("/product/{id}")
def delete(id:int,db:Session=Depends(get_db)):
        db_prod=db.query(database.Product).filter(database.Product.id==id).first()
        if db_prod:
            db.delete(db_prod)
            db.commit()
            return "deleted successfully"
        else:
            return "Did not delete successfully"
