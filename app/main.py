from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Model untuk produk fashion
class Product(BaseModel):
    id: int
    name: str
    category: str
    price: float
    stock: int
    description: str

# Database sementara (simulasi)
products = [
    Product(id=1, name="Summer Dress", category="Dresses", price=49.99, stock=20, description="A lightweight summer dress perfect for hot weather."),
    Product(id=2, name="Denim Jacket", category="Outerwear", price=79.99, stock=15, description="A classic denim jacket for casual occasions."),
    Product(id=3, name="Running Shoes", category="Footwear", price=89.99, stock=30, description="Comfortable running shoes for your daily jog."),
]

@app.get("/")
def read_root():
    return {"message": "Welcome to the Fashion Store API! Explore our latest collections."}

@app.get("/products", response_model=List[Product])
def get_all_products():
    """Mengambil semua produk yang tersedia di toko fashion."""
    return products

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    """Mengambil detail produk berdasarkan ID."""
    for product in products:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/products/category/{category}", response_model=List[Product])
def get_products_by_category(category: str):
    """Mengambil produk berdasarkan kategori."""
    filtered_products = [product for product in products if product.category.lower() == category.lower()]
    if not filtered_products:
        raise HTTPException(status_code=404, detail="No products found in this category")
    return filtered_products

@app.post("/products", response_model=Product)
def add_product(new_product: Product):
    """Menambahkan produk baru ke toko fashion."""
    if any(product.id == new_product.id for product in products):
        raise HTTPException(status_code=400, detail="Product with this ID already exists")
    products.append(new_product)
    return new_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    """Menghapus produk berdasarkan ID."""
    global products
    products = [product for product in products if product.id != product_id]
    return {"message": f"Product with ID {product_id} has been deleted"}

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, updated_product: Product):
    """Memperbarui data produk berdasarkan ID."""
    for index, product in enumerate(products):
        if product.id == product_id:
            products[index] = updated_product
            return updated_product
    raise HTTPException(status_code=404, detail="Product not found")
