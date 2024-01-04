from fastapi import FastAPI, Path

from typing import Optional

from pydantic import BaseModel

from models import Student


app = FastAPI()

# print(Student)


# class Student(BaseModel):
#     name: str
#     age: int
#     courses: list


students = {


    1: {
        "name": "John Doe",
        "age": 30,
        "courses": ["Math", "Physics"]

    },
    2: {
        "name": "Jane Smith",
        "age": 25,
        "courses": ["Computer Science", "Chemistry"]

    }
}


@app.get('/hello')
def index():
    return {"msg": "hello world"}


@app.get("/all-students")
def getAllStudents():

    return students


@app.get("/student/{student_id}")
def getStudentById(student_id: int
                   #    = Path(None, "The id of the student")
                   ):
    if student_id in students:
        return students[student_id]
    else:
        return {"msg": "Not Found", "status": 404}


@app.get("/student-by-name")
def getStudentByName(name: Optional[str] = None):

    for student_id in students:
        if students[student_id]['name'] == name:
            return students[student_id]

    return {"msg": "Not found", "status": 404}


@app.get("/student-by-name-or-id/{student_id_req}")
def getStudentByNameOrID(*, student_id_req: int, name: Optional[str] = None):

    for student_id in students:
        if students[student_id]['name'] == name and student_id == student_id_req:
            return students[student_id]

    return {"msg": "Not found", "status": 404}


@app.post('/add-stduent/{student_id}')
def addStudent(student_id: int, student: Student):

    if student_id not in students:
        students[student_id] = student
        return {'msg': 'Student added', 'data': students[student_id]}
    else:
        return {'error': 'This ID already exists', "status": 400}


@app.delete('/delete/{student_id}')
def deleteStudent(student_id: int):
    if student_id not in students:
        return {"msg": "Not Found", "staus": 404}
    else:
        del students[student_id]
        return {"msg": "Student deleted sucessfully", "status": 200}


@app.put("/update")
def updateStudent(student_id: int, student: Student):
    if student_id in students:
        students[student_id].update(**student.dict())
        return students[student_id]
    else:
        return {"msg": "Record Not Found", "status": 404}
