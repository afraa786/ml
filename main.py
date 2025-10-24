from fastapi import FastAPI, Path
from pydantic import BaseModel

# creates your fastapi instance
app = FastAPI()

# Sample data
items = {
    1: {
        "Student Allotted": 1,
        "name": "Java Book",
        "price": 10.0
    },
    2: {
        "Student Allotted": 2,
        "name": "Datawarehousing and Mining",
        "price": 12.5,
        "is_available": False
    },
}

# Pydantic model
class Item(BaseModel):
    name: str
    price: float
    is_available: bool = True


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/students")
def getAllStudents():
    return items

@app.get("/students/{student_id}")
def get_student(
    student_id: int = Path(..., description="The ID of the student to get", gt=0)
):
   
    if student_id not in items:
        return {"error": "Student not found"}
    return items[student_id]


