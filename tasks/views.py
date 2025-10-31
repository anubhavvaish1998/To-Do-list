from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json

# ✅ Helper function: ensure table exists
def ensure_tasks_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                due_date TIMESTAMP,       
                status BOOLEAN DEFAULT FALSE
            );
        """)



@csrf_exempt
def tasks_api(request):
    """Handle GET (Read All) and POST (Create)"""
    ensure_tasks_table()  # ✅ Ensures table exists before any operation

    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, title, description, due_date, status FROM tasks ORDER BY id;")
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            tasks = [dict(zip(columns, row)) for row in rows]
        return JsonResponse(tasks, safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        title = data.get("title")
        description = data.get("description", "")
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO tasks (title, description) VALUES (%s, %s) RETURNING id;",
                [title, description]
            )
            task_id = cursor.fetchone()[0]
        return JsonResponse({"message": "Task created successfully", "id": task_id}, status=201)

    return JsonResponse({"error": "Invalid HTTP method"}, status=405)


@csrf_exempt
def task_detail_api(request, task_id):
    """Handle GET (Read One), PUT (Update), DELETE (Delete)"""
    ensure_tasks_table()  # ✅ Ensures table exists before any single-task action

    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, title, description, is_completed FROM tasks WHERE id = %s;", [task_id])
            row = cursor.fetchone()
            if not row:
                return JsonResponse({"error": "Task not found"}, status=404)
            columns = [col[0] for col in cursor.description]
            task = dict(zip(columns, row))
        return JsonResponse(task)

    elif request.method == 'PUT':
        data = json.loads(request.body)
        title = data.get("title")
        description = data.get("description")
        is_completed = data.get("is_completed", False)
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE tasks
                SET title = %s, description = %s, is_completed = %s
                WHERE id = %s RETURNING id;
                """,
                [title, description, is_completed, task_id]
            )
            updated = cursor.fetchone()
        if not updated:
            return JsonResponse({"error": "Task not found"}, status=404)
        return JsonResponse({"message": "Task updated successfully"})

    elif request.method == 'DELETE':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM tasks WHERE id = %s RETURNING id;", [task_id])
            deleted = cursor.fetchone()
        if not deleted:
            return JsonResponse({"error": "Task not found"}, status=404)
        return JsonResponse({"message": "Task deleted successfully"})

    return JsonResponse({"error": "Invalid HTTP method"}, status=405)
