from database import get_sql_connection
from models import UOM


def get_uoms():
    """Get all units of measure"""
    connection = get_sql_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM uom"
    cursor.execute(query)
    response = []
    for uom_id, uom_name in cursor:
        response.append({"uom_id": uom_id, "uom_name": uom_name})
    return response
