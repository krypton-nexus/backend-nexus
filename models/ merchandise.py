from Database.connection import get_connection
import json

# ----------------------- Products -----------------------

def insert_product(data):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            insert_query = """
                INSERT INTO products 
                (club_id, product_name, product_description, product_price, product_quantity, product_images) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                data['club_id'],
                data['product_name'],
                data['product_description'],
                data['product_price'],
                data['product_quantity'],
                json.dumps(data.get('product_images', []))
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
            for product in results:
                product['product_images'] = json.loads(product['product_images']) if product['product_images'] else []
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
            for product in results:
                product['product_images'] = json.loads(product['product_images']) if product['product_images'] else []
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

