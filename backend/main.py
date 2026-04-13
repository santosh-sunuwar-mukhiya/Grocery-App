from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import json
from database import init_database
from daos import uom_dao, products_dao, orders_dao

# Initialize databases on startup
init_database()

app = FastAPI(title="Grocery Store Management API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Grocery Store Management System API"}


@app.get("/getUOM")
def get_uom():
    """Get all units of measure"""
    response = uom_dao.get_uoms()
    return response


@app.get("/getProducts")
def get_products():
    """Get all products"""
    response = products_dao.get_all_products()
    return response


@app.post("/insertProduct")
def insert_product(data: str = Form(...)):
    """Insert a new product"""
    request_payload = json.loads(data)
    product_id = products_dao.insert_new_product(request_payload)
    return {"product_id": product_id}


@app.get("/getAllOrders")
def get_all_orders():
    """Get all orders with details"""
    response = orders_dao.get_all_orders()
    return response


@app.post("/insertOrder")
def insert_order(data: str = Form(...)):
    """Insert a new order"""
    request_payload = json.loads(data)
    order_id = orders_dao.insert_order(request_payload)
    return {"order_id": order_id}


@app.post("/deleteProduct")
def delete_product(product_id: str = Form(...)):
    """Delete a product"""
    return_id = products_dao.delete_product(product_id)
    return {"product_id": return_id}


if __name__ == "__main__":
    import uvicorn

    print("Starting FastAPI Server For Grocery Store Management System")
    uvicorn.run(app, host="0.0.0.0", port=5000)
