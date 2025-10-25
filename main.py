# ============================================================================
# IMPORTS - Bringing in the tools we need
# ============================================================================

from fastapi import FastAPI, Path, HTTPException, status
# FastAPI: The main framework for building our API
# Path: For validating path parameters (like task_id in /tasks/{task_id})
# HTTPException: For returning proper error responses
# status: Contains HTTP status code constants (like 404, 201, etc.)

from pydantic import BaseModel, Field
# BaseModel: Base class for creating data models with validation
# Field: Adds extra validation rules to model fields (like max_length, min, max)

from typing import Optional, Literal, List
# Optional: Makes a field optional (can be None)
# Literal: Restricts values to specific options (like "low", "medium", "high")
# List: For specifying that something is a list of items


# ============================================================================
# APP INITIALIZATION
# ============================================================================

app = FastAPI()
# Creates your FastAPI application instance
# This is the main object that handles all your routes and requests


# ============================================================================
# IN-MEMORY STORAGE (Temporary - will be replaced with database later)
# ============================================================================

tasks = []
# Empty list to store all our tasks
# Currently stores data in RAM (memory)
# WARNING: All data is lost when server restarts!

task_id_counter = 1
# Keeps track of the next ID to assign to a new task
# Starts at 1, increments each time we create a task
# Example: First task gets ID 1, second gets ID 2, etc.


# ============================================================================
# DATA MODELS (Blueprints for our data)
# ============================================================================

class TaskCreate(BaseModel):
    """
    Model for CREATING a new task
    Used when user sends data to POST /tasks
    Does NOT include 'id' because we assign that automatically
    """
    title: str
    # Task title (required, must be a string)
    
    description: Optional[str] = None
    # Task description (optional, defaults to None if not provided)
    
    completed: bool = False
    # Whether task is done (optional, defaults to False)
    
    priority: Literal["low", "medium", "high"] = "medium"
    # Priority level (optional, defaults to "medium")
    # Can ONLY be one of: "low", "medium", or "high"
    # Pydantic automatically rejects other values!


class TaskResponse(BaseModel):
    """
    Model for RETURNING task data
    Used when we send task data back to the user
    Includes 'id' because we've assigned one
    """
    id: int
    # Unique task identifier (required, integer)
    
    title: str
    # Task title (required, string)
    
    description: Optional[str] = Field(None, max_length=300)
    # Task description (optional, max 300 characters)
    # Field() adds validation - if description is longer than 300 chars, error!
    
    completed: bool = False
    # Completion status (defaults to False)
    
    priority: Literal["low", "medium", "high"] = "medium"
    # Priority level (only accepts "low", "medium", or "high")



@app.get("/")
def read_root():

    return {"message": "Welcome to the Task Manager API"}


# ----------------------------------------------------------------------------
# SEARCH ENDPOINT - Example of query parameters
# ----------------------------------------------------------------------------

@app.get("/search")
def search(q: str, limit: int = 10):

    return {
        "query": q,
        "limit": limit,
        # List comprehension to generate fake results
        "results": [f"Result {i} for '{q}'" for i in range(1, limit + 1)]
    }


# ----------------------------------------------------------------------------
# CREATE TASK - POST endpoint
# ----------------------------------------------------------------------------

@app.post(
    "/tasks", 
    response_model=TaskResponse,  # Tells FastAPI what shape the response has
    status_code=status.HTTP_201_CREATED  # Returns 201 instead of default 200
)
def create_task(task: TaskCreate):

    global task_id_counter
    # 'global' keyword lets us modify the variable outside this function
    # Without 'global', Python would create a NEW local variable instead
    
    # Create a new TaskResponse object with all fields
    new_task = TaskResponse(
        id=task_id_counter,         # Assign current counter value as ID
        title=task.title,           # Copy title from input
        description=task.description,  # Copy description (might be None)
        completed=task.completed,   # Copy completed status
        priority=task.priority      # Copy priority level
    )
    
    # Increment counter for next task
    task_id_counter += 1
    # Now next task will get ID 2, then 3, etc.
    
    # Add the new task to our list
    tasks.append(new_task)
    
    # Return the created task
    # FastAPI automatically converts this to JSON
    return new_task


# ----------------------------------------------------------------------------
# GET ALL TASKS
# ----------------------------------------------------------------------------

@app.get("/tasks", response_model=List[TaskResponse])
def get_all_tasks():

    return tasks
    # Simply return the entire tasks list
    # FastAPI handles converting it to JSON


# ----------------------------------------------------------------------------
# GET COMPLETED TASKS (SPECIFIC ROUTE - MUST BE BEFORE /{task_id})
# ----------------------------------------------------------------------------

@app.get("/tasks/completed", response_model=List[TaskResponse])
def get_completed_tasks():

    completed_list = []
    # Create empty list to collect completed tasks
    
    # Loop through ALL tasks
    for pakadneka in tasks:
        # pakadneka = one task object from the list
        # (you named it "pakadneka" which means "to catch/grab" - creative! 😄)
        
        if pakadneka.completed:
            # If this task's completed field is True
            # Note: We use .completed (object property), NOT ["completed"] (dict key)
            
            completed_list.append(pakadneka)
            # Add this task to our results list
    
    return completed_list
    # Return all completed tasks we found


# ----------------------------------------------------------------------------
# GET TASKS BY PRIORITY (SPECIFIC ROUTE - MUST BE BEFORE /{task_id})
# ----------------------------------------------------------------------------

@app.get("/tasks/priority/{priority_level}", response_model=List[TaskResponse])
def get_tasks_by_priority(priority_level: str):

    
    # List of valid priority values
    valid_priorities = ["low", "medium", "high"]
    
    # Check if user's input is valid
    if priority_level.lower() not in valid_priorities:
        # .lower() makes it case-insensitive
        # So "HIGH", "High", and "high" all work
        
        # If invalid, raise an HTTP 400 Bad Request error
        raise HTTPException(
            status_code=400,  # 400 = Bad Request (user's fault)
            detail=f"Invalid priority. Must be one of: {valid_priorities}"
        )
    
    # Create empty list to collect matching tasks
    priority_list = []
    
    # Loop through all tasks
    for pakadneka in tasks:
        # Compare priorities (case-insensitive)
        if pakadneka.priority.lower() == priority_level.lower():
            # Both converted to lowercase for comparison
            # So "High" == "high" works!
            
            priority_list.append(pakadneka)
            # Add matching task to results
    
    return priority_list
    # Return all tasks with matching priority



@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task_by_id(
    task_id: int = Path(..., description="The ID of the task to get", gt=0)
):

    
    # Search through all tasks
    for task in tasks:
        # task = current task we're examining
        
        if task.id == task_id:
            # Does this task's ID match what we're looking for?
            # Using .id (object property), not ["id"] (dict key)
            
            return task
            # Found it! Return immediately (exits function)
    
    # If we reach here, loop finished without finding the task
    # Raise 404 Not Found error
    raise HTTPException(
        status_code=404,  # 404 = Not Found
        detail="Task not found"
    )


# ----------------------------------------------------------------------------
# MARK TASK AS COMPLETE
# ----------------------------------------------------------------------------

@app.put("/tasks/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: int):
  
    # Search for the task
    for pakadneka in tasks:
        if pakadneka.id == task_id:
            # Found the task!
            
            pakadneka.completed = True
            # Change completed property to True
            # This modifies the actual object in the tasks list
            
            return pakadneka
            # Return the updated task
    
    # Task not found - raise 404 error
    # IMPORTANT: This is OUTSIDE the loop (proper indentation!)
    raise HTTPException(
        status_code=404, 
        detail="Task not found"
    )


# ----------------------------------------------------------------------------
# UPDATE TASK PRIORITY
# ----------------------------------------------------------------------------

@app.put("/tasks/{task_id}/priority", response_model=TaskResponse)
def update_task_priority(
    task_id: int, 
    priority: Literal["low", "medium", "high"]
):
 
    
    # Search for the task
    for pakadneka in tasks:
        if pakadneka.id == task_id:
            # Found it!
            
            pakadneka.priority = priority
            # Update the priority property
            
            return pakadneka
            # Return updated task
    
    # Task not found
    # IMPORTANT: Outside the loop!
    raise HTTPException(
        status_code=404, 
        detail="Task not found"
    )


# ----------------------------------------------------------------------------
# DELETE TASK
# ----------------------------------------------------------------------------

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    global tasks
    # Need 'global' because we're reassigning the entire tasks list
    
    # Remember how many tasks we have before deletion
    initial_length = len(tasks)
    
    # List comprehension to keep all tasks EXCEPT the one we're deleting
    tasks = [t for t in tasks if t.id != task_id]
    # Translation: "Keep task 't' only if its id is NOT the one we're deleting"
    
    # Check if anything was actually removed
    if len(tasks) == initial_length:
        raise HTTPException(
            status_code=404, 
            detail="Task not found"
        )
    
    # Return nothing (204 No Content means success with no response body)
    return {"message": "Task deleted successfully"}  # Optional message




