#!/usr/bin/env python3

from flask import request
from flask_restful import Resource

from config import app, db, api
from models import Course, Student, Enrollment


# ------ COURSES (GET, POST) ------

class Courses(Resource):
    def get(self):
        courses = Course.query.all()
        return [c.to_dict(only=("id", "title", "description")) for c in courses], 200

    def post(self):
        data = request.get_json() or {}

        course = Course(
            title=data.get("title"),
            description=data.get("description"),
        )

        try:
            db.session.add(course)
            db.session.commit()
            return course.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400


# ------ STUDENTS (GET, POST) ------

class Students(Resource):
    def get(self):
        students = Student.query.all()

        [[setattr(course, "enrollments", [e for e in course.enrollments if e.student_id == student.id]) 
            for course in student.courses] 
            for student in students]

        return [s.to_dict() for s in students], 200



    def post(self):
        data = request.get_json()

        student = Student(
            name=data.get("name"),
            email=data.get("email"),
        )

        try:
            db.session.add(student)
            db.session.commit()
            return student.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400



# ------ ENROLLMENTS (FULL CRUD) ------

class Enrollments(Resource):
    def post(self):
        data = request.get_json()

        if not data:
            return {"error": "No data provided"}, 400

        if not data.get("student_id"):
            return {"error": "student_id is required"}, 400
        if not data.get("course_id"):
            return {"error": "course_id is required"}, 400
        if not data.get("term"):
            return {"error": "term is required"}, 400
        if not data.get("year"):
            return {"error": "year is required"}, 400

        if not Student.query.get(data["student_id"]):
            return {"error": "Student not found"}, 404

        if not Course.query.get(data["course_id"]):
            return {"error": "Course not found"}, 404

        enrollment = Enrollment(
            student_id=data["student_id"],
            course_id=data["course_id"],
            term=data["term"],
            year=data["year"],
        )

        try:
            db.session.add(enrollment)
            db.session.commit()
            return enrollment.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400


class EnrollmentById(Resource):

    def patch(self, id):
        enrollment = Enrollment.query.get(id)
        if enrollment is None:
            return {"error": "Enrollment not found"}, 404

        data = request.get_json() or {}
        allowed = {"term", "year"}

        for attr, value in data.items():
            if attr in allowed:
                setattr(enrollment, attr, value)

        try:
            db.session.commit()
            return enrollment.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400

    def delete(self, id):
        e = Enrollment.query.get(id)
        if not e:
            return {"error": "Enrollment not found"}, 404

        try:
            db.session.delete(e)
            db.session.commit()
            return {}, 204

        except Exception as err:
            db.session.rollback()
            return {"error": str(err)}, 400
        




# ------ ROUTES ------

api.add_resource(Courses, "/courses")

api.add_resource(Students, "/students")

api.add_resource(Enrollments, "/enrollments")
api.add_resource(EnrollmentById, "/enrollments/<int:id>")



if __name__ == "__main__":
    app.run(port=5555, debug=True)
