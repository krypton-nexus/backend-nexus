from connection import get_connection
import json  # To handle JSON serialization
from datetime import timedelta
#add products
def add_product(product_name, product_price, product_description, product_image_link, club_id, product_quantity):
    """
    Adds a new product to the marketplace.
    :param product_name: Name of the product.
    :param product_price: Price of the product.
    :param product_description: Description of the product.
    :param product_image_link: Image URL of the product.
    :param club_id: ID of the club associated with the product.
    :param product_quantity: Available quantity of the product.
    :return: Result message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            insert_query = """
            INSERT INTO product (product_name, product_price, product_description, 
                                product_image_link, club_id, product_quantity)
            VALUES (%s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (product_name, product_price, product_description,
                                          product_image_link, club_id, product_quantity))

            connection.commit()
            return {"message": "Product added successfully"}

        except Exception as e:
            connection.rollback()
            return {"error": str(e)}

        finally:
            cursor.close()
            connection.close()

#get all products
def get_all_products():
    """
    Retrieves all products available in the marketplace.
    :return: List of products.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            select_query = "SELECT * FROM product;"
            cursor.execute(select_query)
            products = cursor.fetchall()

            return products

        except Exception as e:
            return {"error": str(e)}

        finally:
            cursor.close()
            connection.close()

#get product by id
def get_product_by_id(product_id):
    """
    Retrieves a specific product by its ID.
    :param product_id: ID of the product.
    :return: Product details.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            select_query = "SELECT * FROM product WHERE id = %s;"
            cursor.execute(select_query, (product_id,))
            product = cursor.fetchone()

            if not product:
                return {"error": "Product not found"}

            return product

        except Exception as e:
            return {"error": str(e)}

        finally:
            cursor.close()
            connection.close()
