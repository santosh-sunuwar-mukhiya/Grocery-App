# Grocery Store Management System - Backend

A FastAPI-based backend for the Grocery Store Management System using SQLite3 database.

## Features

- RESTful API endpoints for managing products, orders, and units of measure
- SQLite3 database with automatic initialization
- CORS enabled for frontend integration
- Form data processing for requests

## API Endpoints

### Units of Measure (UOM)
- `GET /getUOM` - Get all units of measure

### Products
- `GET /getProducts` - Get all products with UOM information
- `POST /insertProduct` - Insert a new product
- `POST /deleteProduct` - Delete a product

### Orders
- `GET /getAllOrders` - Get all orders with their details
- `POST /insertOrder` - Insert a new order with order details

## Database Tables

- **uom** - Units of Measure (kg, liter, piece, pack)
- **products** - Product information with pricing
- **orders** - Customer orders
- **order_details** - Individual items in each order

## Setup Instructions

### 1. Install Dependencies

```bash
cd /Users/princeysunar/Dev/Grocery/Grocery-App
pip install -r requirements.txt
```

### 2. Run the Backend

Navigate to the project root and run:

```bash
python -m uvicorn backend.main:app --reload --port 5000
```

Or from the backend directory:

```bash
cd backend
python main.py
```

The API will be available at: **http://localhost:5000**

API documentation will be available at: **http://localhost:5000/docs**

### 3. Database

The SQLite database (`grocery_store.db`) will be automatically created in the `backend` directory when the application starts. It includes sample UOM data (kg, liter, piece, pack).

## Frontend Setup

### 1. Start a Local Web Server

The frontend is located in the `frontend` directory. You need to serve the HTML files via HTTP (not file://).

**Option 1: Using Python's built-in server**

```bash
cd frontend
python -m http.server 8000
```

Then open: **http://localhost:8000**

**Option 2: Using Node.js (if installed)**

```bash
cd frontend
npx http-server -p 8000
```

**Option 3: Using any other web server (nginx, Apache, etc.)**

## Running Both Backend and Frontend

### Terminal 1 - Start Backend:
```bash
cd /Users/princeysunar/Dev/Grocery/Grocery-App
python -m uvicorn backend.main:app --reload --port 5000
```

### Terminal 2 - Start Frontend:
```bash
cd /Users/princeysunar/Dev/Grocery/Grocery-App/frontend
python -m http.server 8000
```

### Access the Application:
- Frontend: **http://localhost:8000**
- Backend API: **http://localhost:5000**
- API Docs: **http://localhost:5000/docs**

## API Request Examples

### Insert Product
```bash
curl -X POST "http://localhost:5000/insertProduct" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'data={"product_name":"potato","uom_id":1,"price_per_unit":10.5}'
```

### Insert Order
```bash
curl -X POST "http://localhost:5000/insertOrder" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'data={"customer_name":"John","grand_total":100,"order_details":[{"product_id":1,"quantity":2,"total_price":21}]}'
```

### Get all Products
```bash
curl "http://localhost:5000/getProducts"
```

### Get all Orders
```bash
curl "http://localhost:5000/getAllOrders"
```

### Get UOM
```bash
curl "http://localhost:5000/getUOM"
```

### Delete Product
```bash
curl -X POST "http://localhost:5000/deleteProduct" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'product_id=1'
```

## Troubleshooting

1. **Port already in use**: Change the port number in the run command
2. **Module not found**: Ensure you're running from the correct directory and all dependencies are installed
3. **CORS errors**: The backend has CORS enabled for all origins, which may need to be restricted in production
4. **Database issues**: Delete `grocery_store.db` and restart the application to reset the database

## Notes

- The database initializes automatically on first run
- Sample UOM data is inserted on first initialization
- All timestamps are stored in ISO format
- The database uses SQLite3 which is file-based and doesn't require a separate server
