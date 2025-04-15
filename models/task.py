from Database.connection import get_connection
import json
import uuid

def create_task(data):
    """
    Creates a new task in the database.
    :param data: Dictionary containing task details.
    :return: Result message with created task or error.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            
    
            
            # SQL query to insert task
            insert_query = """
            INSERT INTO tasks (
            title, description, assignee_id, 
                club_id, due_date, priority, status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            
            cursor.execute(insert_query, (
             
                data['title'],
                data.get('description', ''),
                data['assignee_id'],
                data.get('club_id'),
                data['due_date'],
                data.get('priority', 'Medium'),
                data.get('status', 'To Do')
            ))
            
            connection.commit()
            
            # Return the created task
            return {
                "message": "Task created successfully",
                "task": {
                    "name": data['title'],
                    "description": data.get('description', ''),
                    "assignee": data['assignee_id'],
                    "club_id": data.get('club_id'),
                    "dueDate": data['due_date'],
                    "priority": data.get('priority', 'Medium'),
                    "status": data.get('status', 'To Do')
                }
            }
            
        except Exception as e:
            connection.rollback()
            return {"error": str(e)}
            
        finally:
            cursor.close()
            connection.close()

def get_task_by_id(task_id):
    """
    Retrieves a single task by ID.
    :param task_id: The ID of the task to retrieve.
    :return: Task details or error message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            
            select_query = """
            SELECT 
                t.task_id as id,
                t.title as name,
                t.description,
                m.student_id as assignee,
                t.club_id,
                t.due_date as dueDate,
                t.priority,
                t.status
            FROM tasks t
            LEFT JOIN membership m ON t.assignee_id = m.id
            WHERE t.task_id = %s;
            """
            
            cursor.execute(select_query, (task_id,))
            task = cursor.fetchone()
            
            if task:
                # Format to match frontend expectations
                task['dueDate'] = str(task['dueDate'])
                return task
            else:
                return {"error": "Task not found"}
                
        except Exception as e:
            return {"error": str(e)}
            
        finally:
            cursor.close()
            connection.close()

def get_all_tasks_for_memberid(member_id):
    """
    Gets all tasks for a specific member with complete member details
    :param member_id: The membership ID of the member
    :return: List of tasks with member details or error message
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT 
                t.task_id as id,
                t.title as name,
                t.description,
                t.club_id,
                t.due_date as dueDate,
                t.priority,
                t.status,
                m.id as membership_id,
                s.student_id,
                s.first_name,
                s.last_name,
                s.email,
                s.phone_number
            FROM tasks t
            JOIN membership m ON t.assignee_id = m.id
            JOIN student s ON m.student_id = s.email
            WHERE t.assignee_id = %s
            ORDER BY t.due_date;
            """
            
            cursor.execute(query, (member_id,))
            tasks = cursor.fetchall()
            
            # Format the results
            formatted_tasks = []
            for task in tasks:
                formatted_tasks.append({
                    "task": {
                        "id": task['id'],
                        "name": task['name'],
                        "description": task['description'],
                        "club_id": task['club_id'],
                        "dueDate": str(task['dueDate']),
                        "priority": task['priority'],
                        "status": task['status']
                    },
                    "member": {
                        "membership_id": task['membership_id'],
                        "student_id": task['student_id'],
                        "first_name": task['first_name'],
                        "last_name": task['last_name'],
                        "full_name": f"{task['first_name']} {task['last_name']}",
                        "email": task['email'],
                        "phone_number": task['phone_number']
                    }
                })
            
            return formatted_tasks
            
        except Exception as e:
            return {"error": str(e)}
            
        finally:
            cursor.close()
            connection.close()

def get_all_tasks_by_clubid(club_id):
    """
    Gets all tasks for a specific club with complete member details
    :param club_id: The ID of the club
    :return: List of tasks with member details or error message
    """
    connection = get_connection()
    if not connection:
        return {"error": "Database connection failed"}
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        query = """
        SELECT 
            t.task_id as task_id,
            t.title as task_title,
            t.description as task_description,
            t.club_id,
            t.due_date,
            t.priority as task_priority,
            t.status as task_status,
            m.id as membership_id,
            s.first_name,
            s.last_name,
            s.email,
            s.phone_number,
            c.title as club_name
        FROM tasks t
        JOIN membership m ON t.assignee_id = m.id
        JOIN student s ON m.student_id = s.email
        JOIN clubs c ON t.club_id = c.id
        WHERE t.club_id = %s;
        """
        
        cursor.execute(query, (club_id,))
        tasks = cursor.fetchall()
        
        if not tasks:
            return {"message": "No tasks found for this club"}
        
        # Format the results
        formatted_tasks = []
        for task in tasks:
            formatted_tasks.append({
                "task_id": task['task_id'],
                "title": task['task_title'],
                "description": task['task_description'],
                "club_id": task['club_id'],
                "club_name": task['club_name'],
                "due_date": str(task['due_date']),
                "priority": task['task_priority'],
                "status": task['task_status'],
                "assignee_details": {
                    "membership_id": task['membership_id'],
                    "first_name": task['first_name'],
                    "last_name": task['last_name'],
                    "full_name": f"{task['first_name']} {task['last_name']}",
                    "email": task['email'],
                    "phone": task['phone_number']
                }
            })
        
        return formatted_tasks
        
    except Exception as e:
        return {"error": f"Database error: {str(e)}"}
    finally:
        if connection:
            cursor.close()
            connection.close()

def update_task(task_id, data):
    """
    Updates an existing task.
    :param task_id: ID of the task to update.
    :param data: Dictionary of fields to update.
    :return: Updated task or error message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Build dynamic update query
            update_fields = []
            values = []
            
            allowed_fields = [
                'title', 'description', 'assignee_id', 
                 'due_date', 'priority', 'status'
            ]
            
            for field in allowed_fields:
                if field in data:
                    update_fields.append(f"{field} = %s")
                    values.append(data[field])
            
            if not update_fields:
                return {"error": "No valid fields provided for update"}
            
            update_query = f"""
            UPDATE tasks 
            SET {", ".join(update_fields)}
            WHERE task_id = %s
            RETURNING *;
            """
            
            values.append(task_id)
            cursor.execute(update_query, tuple(values))
            updated_task = cursor.fetchone()
            
            connection.commit()
            
            if updated_task:
                return {
                    "message": "Task updated successfully",
                    "task": {
                        "id": updated_task['task_id'],
                        "name": updated_task['title'],
                        "description": updated_task['description'],
                        "assignee": updated_task['assignee_id'],
                        "club_id": updated_task['club_id'],
                        "dueDate": str(updated_task['due_date']),
                        "priority": updated_task['priority'],
                        "status": updated_task['status']
                    }
                }
            else:
                return {"error": "Task not found"}
                
        except Exception as e:
            connection.rollback()
            return {"error": str(e)}
            
        finally:
            cursor.close()
            connection.close()

def delete_task(task_id):
    """
    Deletes a task from the database.
    :param task_id: ID of the task to delete.
    :return: Success or error message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            delete_query = "DELETE FROM tasks WHERE task_id = %s;"
            cursor.execute(delete_query, (task_id,))
            
            if cursor.rowcount == 0:
                return {"error": "Task not found"}
            
            connection.commit()
            return {"message": "Task deleted successfully"}
            
        except Exception as e:
            connection.rollback()
            return {"error": str(e)}
            
        finally:
            cursor.close()
            connection.close()
def get_admin_tasks(admin_email=None, club_id=None):
    """
    Gets admin tasks filtered by both admin email and club ID
    :param admin_email: Admin email (required)
    :param club_id: Club ID (required)
    :return: List of matching admin tasks or error message
    """
    if not admin_email or not club_id:
        return {"error": "Both admin_email and club_id parameters are required"}
    
    connection = get_connection()
    if not connection:
        return {"error": "Database connection failed"}
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        query = """
        SELECT * FROM admin_tasks 
        WHERE admin_email = %s AND club_id = %s
        """
        
        cursor.execute(query, (admin_email, club_id))
        tasks = cursor.fetchall()
        
        return tasks if tasks else []
        
    except Exception as e:
        return {"error": f"Database error: {str(e)}"}
    finally:
        if connection:
            cursor.close()
            connection.close()

def create_admin_task(admin_email, club_id, task_name):
    """
    Creates a new admin task.
    :param admin_email: Email of the admin
    :param club_id: ID of the club
    :param task_name: Name of the task
    :return: Result message with task ID or error.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            
            insert_query = """
            INSERT INTO admin_tasks (admin_email, club_id, task_name)
            VALUES (%s, %s, %s);
            """
            
            cursor.execute(insert_query, (admin_email, club_id, task_name))
            connection.commit()
            
            # Get the auto-generated ID
            task_id = cursor.lastrowid
            return {
                "message": "Admin task created successfully",
                "task_id": task_id
            }
            
        except Exception as e:
            connection.rollback()
            return {"error": str(e)}
            
        finally:
            cursor.close()
            connection.close()
