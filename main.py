from fastapi import FastAPI, Path, HTTPException, Depends

from typing import Optional, List
from uuid import uuid4, UUID
from starlette import status

from pydantic import BaseModel

from schema import User, Gender, Role, UpdateUser

from database import get_db

import database
from database import Base
from sqlalchemy.orm import Session
import models
import schema
app = FastAPI()


# def create_tables():

Base.metadata.create_all(database.engine)

# db: List[User] = [

#     User(
#         id=UUID("b4fd8d17-dff8-4886-aa1d-a93c9e1c478e"),
#         first_name="lokesh",
#         last_name="gawande",
#         gender=Gender.male,
#         role=[Role.user]


#     ), User(
#         id=UUID("a0f0b992-c15d-44fa-bc8e-fd205821c4fb"),
#         first_name="Ayush",
#         last_name="Gupta",
#         gender=Gender.male,
#         role=[Role.user]

#     ), User(
#         id=UUID("cb5441ac-429f-4eab-8a15-ef65e17770d7"),
#         first_name="Sid",
#         last_name="Dhiman",
#         gender=Gender.male,
#         role=[Role.admin, Role.user]

#     )


# ]


# print(Student)


# class Student(BaseModel):
#     name: str
#     age: int
#     courses: list


# students = {


#     1: {
#         "name": "John Doe",
#         "age": 30,
#         "courses": ["Math", "Physics"]

#     },
#     2: {
#         "name": "Jane Smith",
#         "age": 25,
#         "courses": ["Computer Science", "Chemistry"]

#     }
# }


# def dbConnection():

#     return "DB connected sucessfully"


@app.get('/hello')
def index():
    return {"msg": "hello world"}


@app.get('/api/v1/students')
def getAllStudents(db: Session = Depends(get_db)):

    try:
        # return db
        students = db.query(models.Student).all()
        return students
    except Exception as e:
        return {"msg": str(e), "status": 400}


@app.get("/api/v1/student/{id}")
def getStudentByID(id: int, db: Session = Depends(get_db)):

    try:
        print(type(id))
        student = db.query(models.Student).filter(
            (models.Student.id) == id).first()

        if student is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The id: {
                                id} you requested for does not exist")
        return student

    except Exception as e:
        return {"msg": str(e), "status": 400}

    # for i in db:
    #     # print(i.id, id)
    #     print(str(i.id) == id)
    #     print(type(i.id), type(id))
    #     if str(i.id) == id:
    #         return i

    # return {"msg": "Not Found", "status": 404}


@app.post("/api/v1/student/add/")
def addStudent(student: schema.User, db: Session = Depends(get_db)):

    # t = student.age
    # return {"msg": t}
    # print(t)
    # return {"age": t}
    # if t < 0:
    #     return {"msg": "Age cannot be negative", "status": 400}
    # s = type(t)
    # # s = type((student.age))
    # return {"msg": s}
    # if type(student.age) != int or student.age < 0:
    #     # raise Exception("Invalid age")
    #     return {"age": "invalid"}
    # id = User.id
    # print(User)
    try:
        # return {"msg": student.id}
        id = student.id
        if type(student.age) != int or student.age < 0:
            raise ValueError("Invalid Age")
            # raise Exception("Invalid age")
            # return {"age": "error"}
        # raise ValueError("Age must be a positive integer")
        # return {"type": type(id)}
        student_db = db.query(models.Student).filter(
            (models.Student.id) == id).first()

        if student_db is not None:
            raise HTTPException(
                status_code=409, detail="Conflict: ID already Exist")
    # db.append(student)
    # return {"msg": "Sucess", "id": student.id, "status": 202}

    # print(student is None)
    # if student is None:
    #     return {"msg": "None"}
        new_sudent = models.Student(**student.dict())
        db.add(new_sudent)
        db.commit()
        db.refresh(new_sudent)

        return [new_sudent]

    except Exception as e:
        return {"msg": str(e), "status": 400}


@app.delete("/api/v1/student/delete/{id}")
def deleteStuent(id: int, db: Session = Depends(get_db)):
    # for i in db:
    #     if str(i.id) == id:
    #         db.remove(i)
    #         return {"msg": "Delete Sucesss", "staus": 200}

    # return {"msg": "Not Found", "staus": 404}

    try:

        deleted_student = db.query(models.Student).filter(
            (models.Student.id) == id)

        if deleted_student.first() is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"The id: {id} you requested for does not exist")
        deleted_student.delete(synchronize_session=False)
        db.commit()
        return {"msg": "Student deleted sucessfully", "status": 200}
    except Exception as e:
        return {"msg": str(e), "status": 404}


@app.put("/api/v1/student/update/{id}")
def updateStudent(user: schema.User, id: int, db: Session = Depends(get_db)):
    # for i in db:
    #     if str(i.id) == id:
    #         i.__dict__.update(user.__dict__)
    #         return i

    # raise HTTPException(

    #     status_code=404,
    #     detail="User not found"

    # )
    try:
        updated_student = db.query(models.Student).filter(
            (models.Student.id) == id).first()

        if updated_student.first() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"The id:{id} does not exist")
        updated_student.update(user.dict(), synchronize_session=False)
        db.commit()

        return updated_student.first()
    except Exception as e:
        return {"msg": str(e), "status": 400}

    # return {"msg": "Not Found", "staus": 404}


@app.patch("/api/v1/student/update_full/{id}")
def partialStudentUpdate(id: int, user: UpdateUser, db: Session = Depends(get_db)):

    try:

        # with Session(engine) as session:
        db_student = db.query(models.Student).filter(
            (models.Student.id) == id).first()
        # return db_student
        if db_student is None:
            # return {"msg": "Not found"}
            raise HTTPException(status_code=404, detail="Student not found")
        student_data = user.model_dump(exclude_unset=True)
        if student_data.get("name") is not None:
            db_student.name = student_data.get("name")

        if student_data.get("age") is not None:
            db_student.age = student_data.get("age")

        if student_data.get("role") is not None:
            db_student.role = student_data.get('role')

        db.add(db_student)
        db.commit()
        db.refresh(db_student)

        return db_student

    except Exception as e:
        return {"msg": str(e), "status": 400}
    # db_student.update(student_data, syncronize=False)
    # db.execute(db_student.update().values(**student_data))
    # for key, value in student_data.items():
    #     setattr(db_student, key, value)
    # db.add(db_student)
    # db.commit()
    # db.refresh(db_student)
    # return db_student
    # try:
    # for i in db:
    #     print(i.id, id)
    #     if (i.id) == id:
    #         if user.name is not None:
    #             i.name = user.name

    #         if user.age is not None:
    #             i.age = user.age

    #         if user.role is not None:
    #             i.role = user.role

    #         return {"msg": "Updated sucessfully", "status": 200}

    # raise HTTPException(
    #     status_code=404,
    #     detail="Detial Not Found!"

    # )
    # except Exception as e:
    #     return {"msg": str(e), "status": 400}


# @app.get("/all-students")
# def getAllStudents():

#     return students


# @app.get("/student/{student_id}")
# def getStudentById(student_id: int
#                    #    = Path(None, "The id of the student")
#                    ):
#     if student_id in students:
#         return students[student_id]
#     else:
#         return {"msg": "Not Found", "status": 404}


# @app.get("/student-by-name")
# def getStudentByName(name: Optional[str] = None):

#     for student_id in students:
#         if students[student_id]['name'] == name:
#             return students[student_id]

#     return {"msg": "Not found", "status": 404}


# @app.get("/student-by-name-or-id/{student_id_req}")
# def getStudentByNameOrID(*, student_id_req: int, name: Optional[str] = None):

#     for student_id in students:
#         if students[student_id]['name'] == name and student_id == student_id_req:
#             return students[student_id]

#     return {"msg": "Not found", "status": 404}


# @app.post('/add-stduent/{student_id}')
# def addStudent(student_id: int, student: Student):

#     if student_id not in students:
#         students[student_id] = student
#         return {'msg': 'Student added', 'data': students[student_id]}
#     else:
#         return {'error': 'This ID already exists', "status": 400}

# @app.delete('/delete/{student_id}')
# def deleteStudent(student_id: int):
#     if student_id not in students:
#         return {"msg": "Not Found", "staus": 404}
#     else:
#         del students[student_id]
#         return {"msg": "Student deleted sucessfully", "status": 200}
# @app.put("/update")
# def updateStudent(student_id: int, student: Student):
#     if student_id in students:
#         students[student_id].update(**student.dict())
#         return students[student_id]
#     else:
#         return {"msg": "Record Not Found", "status": 404}
# async def init():
#     await dbConnection()
#     # print(s)
#     return "Db connected succesfully"
# if __name__ == "__main__":
#     dbConnection()
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
    # create_tables()
