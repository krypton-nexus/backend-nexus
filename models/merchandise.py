from Database.connection import get_connection
import json
from service.emailservice import send_merch_order_email

# ----------------------- Products -----------------------

def insert_product(data):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            insert_query = """
                INSERT INTO products 
                (club_id, product_name, product_description, product_price, product_quantity, product_image_link) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                data['club_id'],
                data['product_name'],
                data['product_description'],
                data['product_price'],
                data['product_quantity'],
                data['product_image_link']
            ))
            connection.commit()
            return {"message": "Product inserted successfully"}
        except Exception as e:
            connection.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            connection.close()


def get_all_products():
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM products ORDER BY created_at DESC")
            results = cursor.fetchall()
            # for product in results:
            #     product['product_images'] = json.loads(product['product_images']) if product['product_images'] else []
            return results
        except Exception as e:
            return {"error": str(e)}
        finally:
            cursor.close()
            connection.close()


def get_products_by_club(club_id):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM products WHERE club_id = %s", (club_id,))
            results = cursor.fetchall()
            # for product in results:
            #     product['product_images'] = json.loads(product['product_images']) if product['product_images'] else []
            return results
        except Exception as e:
            return {"error": str(e)}
        finally:
            cursor.close()
            connection.close()


def update_product(product_id, data):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            fields = []
            values = []
            allowed = ['product_name', 'product_description', 'product_price', 'product_quantity', 'product_images']
            for key in allowed:
                if key in data:
                    fields.append(f"{key} = %s")
                    if key == "product_images":
                        values.append(json.dumps(data[key]))
                    else:
                        values.append(data[key])
            if not fields:
                return {"error": "No valid fields provided for update"}

            query = f"UPDATE products SET {', '.join(fields)} WHERE id = %s"
            values.append(product_id)
            cursor.execute(query, tuple(values))
            connection.commit()
            return {"message": "Product updated successfully"}
        except Exception as e:
            connection.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            connection.close()

def delete_product(product_id):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Check if product exists
            cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            if cursor.fetchone() is None:
                return {"error": "Product not found"}

            # Delete the product
            cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            connection.commit()
            return {"message": "Product deleted successfully"}
        except Exception as e:
            connection.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            connection.close()

# ----------------------- Orders -----------------------

def create_order(data):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            cursor.execute("SELECT product_quantity FROM products WHERE id = %s", (data['product_id'],))
            stock = cursor.fetchone()
            if not stock or stock[0] < data['product_quantity']:
                return {"error": "Insufficient stock"}

            insert_query = """
                INSERT INTO orders (product_id, club_id, product_quantity, order_amount, 
                customer_name, customer_email, customer_phone, customer_address)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                data['product_id'],
                data['club_id'],
                data['product_quantity'],
                data['order_amount'],
                data['customer_name'],
                data['customer_email'],
                data['customer_phone'],
                data['customer_address']
            ))

            cursor.execute(
                "UPDATE products SET product_quantity = product_quantity - %s WHERE id = %s",
                (data['product_quantity'], data['product_id'])
            )

            connection.commit()
            cursor.execute("SELECT product_quantity, product_name FROM products WHERE id = %s", (data['product_id'],))
            product_info = cursor.fetchone()
            product_name = product_info[1] 
            data['product_name']=product_name
            send_merch_order_email(data,"processing")
            return {"message": "Order created successfully"}
        except Exception as e:
            connection.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            connection.close()

def get_all_orders():
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT o.*, p.product_name 
                FROM orders o 
                JOIN products p ON o.product_id = p.id 
                ORDER BY o.created_at DESC
            """)
            return cursor.fetchall()
        except Exception as e:
            return {"error": str(e)}
        finally:
            cursor.close()
            connection.close()


def get_orders_by_club(club_id):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT o.*, p.product_name 
                FROM orders o 
                JOIN products p ON o.product_id = p.id 
                WHERE o.club_id = %s 
                ORDER BY o.created_at DESC
            """, (club_id,))
            return cursor.fetchall()
        except Exception as e:
            return {"error": str(e)}
        finally:
            cursor.close()
            connection.close()


def update_order_status(order_id, status):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE orders 
                SET order_status = %s, updated_at = CURRENT_TIMESTAMP 
                WHERE order_id = %s
            """, (status, order_id))
            connection.commit()
            return {"message": "Order status updated successfully"}
        except Exception as e:
            connection.rollback()
            return {"error": str(e)}
        finally:
            cursor.close()
            connection.close()


# ----------------------- Dashboard -----------------------

def get_dashboard_stats(club_id):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)

            cursor.execute("SELECT COUNT(*) AS total_products FROM products WHERE club_id = %s", (club_id,))
            total_products = cursor.fetchone()['total_products']

            cursor.execute("SELECT COUNT(*) AS total_orders FROM orders WHERE club_id = %s", (club_id,))
            total_orders = cursor.fetchone()['total_orders']

            cursor.execute("""
                SELECT order_status, COUNT(*) AS count 
                FROM orders 
                WHERE club_id = %s 
                GROUP BY order_status
            """, (club_id,))
            status_counts = cursor.fetchall()

            cursor.execute("""
                SELECT o.*, p.product_name 
                FROM orders o 
                JOIN products p ON o.product_id = p.id 
                WHERE o.club_id = %s 
                ORDER BY o.created_at DESC 
                LIMIT 5
            """, (club_id,))
            recent_orders = cursor.fetchall()

            return {
                'total_products': total_products,
                'total_orders': total_orders,
                'orders_by_status': status_counts,
                'recent_orders': recent_orders
            }
        except Exception as e:
            return {"error": str(e)}
        finally:
            cursor.close()
            connection.close()