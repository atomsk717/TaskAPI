"""
Simple client for TaskAPI.
Run the API first (uvicorn main:app --reload --port 8001),
then run this script in another terminal.
"""

import requests

BASE_URL = "http://127.0.0.1:8001"

def print_response(label, response):
    print(f"\n=== {label} ===")
    print(f"Status: {response.status_code}")
    try:
        print(response.json())
    except:
        print(response.text)

# 1. Create a task
print("Creating a new task...")
new_task = {
    "title": "Finish Day 02 TaskAPI",
    "description": "Build, test, and document the API"
}
response = requests.post(f"{BASE_URL}/tasks", json=new_task)
print_response("CREATE TASK", response)
created = response.json()
task_id = created["id"]

# 2. Get all tasks
print("\nFetching all tasks...")
response = requests.get(f"{BASE_URL}/tasks")
print_response("GET ALL TASKS", response)

# 3. Get one task
print(f"\nFetching task {task_id}...")
response = requests.get(f"{BASE_URL}/tasks/{task_id}")
print_response("GET ONE TASK", response)

# 4. Update the task (mark as completed)
print(f"\nUpdating task {task_id}...")
update_data = {"completed": True, "description": "Completed successfully"}
response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=update_data)
print_response("UPDATE TASK", response)

# 5. Delete the task
print(f"\nDeleting task {task_id}...")
response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
print_response("DELETE TASK", response)

print("\nClient finished.")
