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

#update product
def update_product(product_id, product_name, product_price, product_description, product_image_link, product_quantity):
    """
    Updates the details of an existing product.
    :param product_id: ID of the product to update.
    :param product_name: Updated product name.
    :param product_price: Updated price.
    :param product_description: Updated description.
    :param product_image_link: Updated image link.
    :param product_quantity: Updated quantity.
    :return: Result message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            update_query = """
            UPDATE product 
            SET product_name = %s, product_price = %s, product_description = %s, 
                product_image_link = %s, product_quantity = %s 
            WHERE id = %s;
            """
            cursor.execute(update_query, (product_name, product_price, product_description,
                                          product_image_link, product_quantity, product_id))

            connection.commit()

            if cursor.rowcount == 0:
                return {"error": "Product not found"}

            return {"message": "Product updated successfully"}

        except Exception as e:
            connection.rollback()
            return {"error": str(e)}

        finally:
            cursor.close()
            connection.close()

#delete product 
def delete_product(product_id):
    """
    Deletes a product by ID.
    :param product_id: ID of the product to delete.
    :return: Result message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            delete_query = "DELETE FROM product WHERE id = %s;"
            cursor.execute(delete_query, (product_id,))

            connection.commit()

            if cursor.rowcount == 0:
                return {"error": "Product not found"}

            return {"message": "Product deleted successfully"}

        except Exception as e:
            connection.rollback()
            return {"error": str(e)}

        finally:
            cursor.close()
            connection.close()
#place order
def place_order(user_id, product_id, quantity):
    """
    Places an order for a product.
    :param user_id: ID of the user placing the order.
    :param product_id: ID of the product.
    :param quantity: Quantity of the product to order.
    :return: Order confirmation.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            insert_query = """
            INSERT INTO orders (user_id, product_id, quantity, status) 
            VALUES (%s, %s, %s, 'Pending');
            """
            cursor.execute(insert_query, (user_id, product_id, quantity))

            connection.commit()
            return {"message": "Order placed successfully"}

        except Exception as e:
            connection.rollback()
            return {"error": str(e)}

        finally:
            cursor.close()
            connection.close()
#get all orders
def get_all_orders():
    """
    Retrieves all orders placed in the marketplace.
    :return: List of orders.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            select_query = "SELECT * FROM orders;"
            cursor.execute(select_query)
            orders = cursor.fetchall()

            return orders

        except Exception as e:
            return {"error": str(e)}

        finally:
            cursor.close()
            connection.close()
