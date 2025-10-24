from fastapi import FastAPI, Path
from pydantic import BaseModel
from typing import Optional, Literal
from pydantic import Field
from fastapi import HTTPException


# creates your fastapi instance
app = FastAPI()

# Sample data
# items = {
#     1: {
#         "Student Allotted": 1,
#         "name": "Java Book",
#         "price": 10.0
#     },
#     2: {
#         "Student Allotted": 2,
#         "name": "Datawarehousing and Mining",
#         "price": 12.5,
#         "is_available": False
#     },
# }

tasks = []
task_id_counter = 1

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: Literal["low", "medium", "high"] = "medium"

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str = Field(None, max_length=300)
    completed: bool = False
    priority: Literal["low", "medium", "high"] = "medium"

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/students")
# def getAllStudents():
#     return items

# @app.get("/students/{student_id}")
# def get_student(
#     student_id: int = Path(..., description="The ID of the student to get", gt=0)
# ):
   
#     if student_id not in items:
#         return {"error": "Student not found"}
#     return items[student_id]


@app.get("/search")
def search(q: str, limit: int = 10):
    return {
        "query": q,
        "limit": limit,
        "results": [f"Result {i} for '{q}'" for i in range(1, limit + 1)]
    }

# @app.post("/users")
# def create_user(user: User):
#     return {
#         "message": "User created successfully",
#         "user": user,
#         "is_adult": user.age >= 18
#     }

@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Manager API"}

@app.get("/tasks")
def get_all_tasks():
    return {"tasks": tasks, "total": len(tasks)}

@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int = Path(..., description="The ID of the task to get", gt=0)):

# The loop says: "For each item in the tasks list, temporarily call it task and do something with it"
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found") 


@app.post("/tasks")
def create_tasks(object: Task):
    global task_id_counter # id pakad ke laye
    task.id = task_id_counter
    task_id_counter += 1 # le bhai teri id task ki
    tasks.append(object.dict())
    return {
        "message": "Task created successfully",
        "task": object
    }

@app.put("/tasks/{task_id}")
def complete_task(task_id: int):
    for pakadneka in tasks:
        if pakadneka.id == task_id:
            pakadneka.completed = True
            return {
                "message": "Task marked as completed",
                "task": pakadneka
            }
        
    return {"error": "Task not found"}
    
# Delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    tasks = [t for t in tasks if t.id != task_id]
    return {"message": f"Task {task_id} deleted"}

@app.get("/tasks/completed")
def completed_tasks():
    completed_list = []
    for pakadneka in tasks:
        if pakadneka.completed:
            completed_list.append(pakadneka)

    return completed_list

@app.get("/tasks/priority/{priority_level}")
def tasks_by_priority(priority_level: str):
    valid_priorities = ["low", "medium", "high"]
    if priority_level.lower() not in valid_priorities:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid priority. Must be one of: {valid_priorities}"
        )
    
    priority_list = []
    for pakadneka in tasks:
        if pakadneka.priority.lower() == priority_level.lower():
            priority_list.append(pakadneka)
    
    return priority_list

# /tasks/2/priority
# { 
#     "priority": "high"
# }

@app.put("/tasks/{task_id}/priority")
def update_task_priority(task_id: int, priority: str):
    for pakadneka in tasks:
        if pakadneka.id == task_id:
            pakadneka.priority = priority
            return {
                "message": "Task priority updated",
                "task": pakadneka
            }
        
raise HTTPException(status_code=404, detail="Task not found")
