from fastapi import FastAPI
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Supabase Credentials
#SUPABASE_URL = os.getenv("SUPABASE_URL")
#SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase Client
#supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/")
def read_root():
    return {"message": "Welcome to the eCommerce API!"}

@app.get("/products")
def get_products():
    response = supabase.table("products").select("*").execute()
    return response.data

@app.post("/add-product")
def add_product(name: str, price: float, description: str = ""):
    data = {"name": name, "price": price, "description": description}
    response = supabase.table("products").insert(data).execute()
    return {"message": "Product added!", "data": response.data}

# Run with: uvicorn main:app --reload
