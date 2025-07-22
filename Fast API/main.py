# pip install fastapi uvicorn pydantic
# uvicorn main:app --reload

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
# -----------------------------------
# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# app = FastAPI()


# templates = Jinja2Templates(directory="templates")


# @app.get("/", response_class=HTMLResponse)
# async def read_html(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request, "name": "Kiran"})

# -----------------------------------------------------

# Simulated in-memory database
students_db = []

# Schema (Model) for student


class Student(BaseModel):
    id: int
    name: str
    age: int
    course: str


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI CRUD Example!"}

# Get all students


@app.get("/students", response_model=List[Student])
def get_students():
    return students_db

# Get single student


@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    for student in students_db:
        if student.id == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")

# Create student


@app.post("/students", response_model=Student)
def create_student(student: Student):
    for s in students_db:
        if s.id == student.id:
            raise HTTPException(
                status_code=400, detail="Student ID already exists")
    students_db.append(student)
    return student

# Update student


@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, updated_student: Student):
    for index, s in enumerate(students_db):
        if s.id == student_id:
            students_db[index] = updated_student
            return updated_student
    raise HTTPException(status_code=404, detail="Student not found")

# Delete student


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for index, student in enumerate(students_db):
        if student.id == student_id:
            del students_db[index]
            return {"message": "Student deleted successfully"}
    raise HTTPException(status_code=404, detail="Student not found")
