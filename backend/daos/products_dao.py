from database import get_sql_connection


def get_all_products():
    """Get all products with their UOM information"""
    connection = get_sql_connection()
    cursor = connection.cursor()
    query = """
        SELECT products.product_id, products.name, products.uom_id, 
               products.price_per_unit, uom.uom_name 
        FROM products 
        INNER JOIN uom ON products.uom_id = uom.uom_id
    """
    cursor.execute(query)
    response = []
    for product_id, name, uom_id, price_per_unit, uom_name in cursor:
        response.append(
            {
                "product_id": product_id,
                "name": name,
                "uom_id": uom_id,
                "price_per_unit": price_per_unit,
                "uom_name": uom_name,
            }
        )
    return response


def insert_new_product(product):
    """Insert a new product"""
    connection = get_sql_connection()
    cursor = connection.cursor()
    query = """
        INSERT INTO products (name, uom_id, price_per_unit)
        VALUES (?, ?, ?)
    """
    data = (product["product_name"], product["uom_id"], product["price_per_unit"])
    cursor.execute(query, data)
    connection.commit()
    return cursor.lastrowid


def delete_product(product_id):
    """Delete a product by ID"""
    connection = get_sql_connection()
    cursor = connection.cursor()
    query = "DELETE FROM products WHERE product_id = ?"
    cursor.execute(query, (product_id,))
    connection.commit()
    return product_id
