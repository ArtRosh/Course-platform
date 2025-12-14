#!/usr/bin/env python3

from flask import request
from flask_restful import Resource

from config import app, db, api
from models import Instructor, Course, Lesson, Student, Enrollment


# ------ INSTRUCTORS ------

class Instructors(Resource):
    def get(self):
        instructors = Instructor.query.all()
        return [i.to_dict(only=("id", "name", "email")) for i in instructors], 200

    def post(self):
        data = request.get_json()

        instructor = Instructor(
            name=data.get("name"),
            email=data.get("email"),
        )

        try:
            db.session.add(instructor)
            db.session.commit()
            return instructor.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400


class InstructorById(Resource):
    def get(self, id):
        instructor = Instructor.query.get(id)
        if instructor is None:
            return {"error": "Instructor not found"}, 404
        return instructor.to_dict(), 200

    def patch(self, id):
        instructor = Instructor.query.get(id)
        if instructor is None:
            return {"error": "Instructor not found"}, 404

        data = request.get_json()

        for attr in data:
            setattr(instructor, attr, data[attr])

        try:
            db.session.commit()
            return instructor.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400

    def delete(self, id):
        instructor = Instructor.query.get(id)
        if instructor is None:
            return {"error": "Instructor not found"}, 404

        try:
            db.session.delete(instructor)
            db.session.commit()
            return {}, 204
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400



# ------ COURSES ------

class Courses(Resource):
    def get(self):
        courses = Course.query.all()
        return [c.to_dict() for c in courses], 200

    def post(self):
        data = request.get_json()

        if "instructor_id" not in data:
            return {"error": "instructor_id is required"}, 400

        instructor = Instructor.query.get(data["instructor_id"])
        if instructor is None:
            return {"error": "Instructor not found"}, 404

        course = Course(
            title=data.get("title"),
            description=data.get("description"),
            instructor_id=data["instructor_id"],
        )

        try:
            db.session.add(course)
            db.session.commit()
            return course.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400


class CourseById(Resource):
    def get(self, id):
        course = Course.query.get(id)
        if course is None:
            return {"error": "Course not found"}, 404
        return course.to_dict(), 200

    def patch(self, id):
        course = Course.query.get(id)
        if course is None:
            return {"error": "Course not found"}, 404

        data = request.get_json()

        for attr in data:
            setattr(course, attr, data[attr])

        try:
            db.session.commit()
            return course.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400

    def delete(self, id):
        course = Course.query.get(id)
        if course is None:
            return {"error": "Course not found"}, 404

        try:
            db.session.delete(course)
            db.session.commit()
            return {}, 204
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400


# ------ LESSONS ------

class Lessons(Resource):
    def get(self):
        lessons = Lesson.query.all()
        return [l.to_dict() for l in lessons], 200

    def post(self):
        data = request.get_json()

        if "course_id" not in data:
            return {"error": "course_id is required"}, 400

        course = Course.query.get(data["course_id"])
        if course is None:
            return {"error": "Course not found"}, 404

        lesson = Lesson(
            title=data.get("title"),
            content=data.get("content"),
            course_id=data["course_id"],
        )

        try:
            db.session.add(lesson)
            db.session.commit()
            return lesson.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400


class LessonById(Resource):
    def get(self, id):
        lesson = Lesson.query.get(id)
        if lesson is None:
            return {"error": "Lesson not found"}, 404
        return lesson.to_dict(), 200

    def patch(self, id):
        lesson = Lesson.query.get(id)
        if lesson is None:
            return {"error": "Lesson not found"}, 404

        data = request.get_json()

        for attr in data:
            setattr(lesson, attr, data[attr])

        try:
            db.session.commit()
            return lesson.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400

    def delete(self, id):
        lesson = Lesson.query.get(id)
        if lesson is None:
            return {"error": "Lesson not found"}, 404

        try:
            db.session.delete(lesson)
            db.session.commit()
            return {}, 204
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400


# ------ STUDENTS ------

class Students(Resource):
    def get(self):
        students = Student.query.all()
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


class StudentById(Resource):
    def get(self, id):
        student = Student.query.get(id)
        if student is None:
            return {"error": "Student not found"}, 404
        return student.to_dict(), 200

    def patch(self, id):
        student = Student.query.get(id)
        if student is None:
            return {"error": "Student not found"}, 404

        data = request.get_json()

        for attr in data:
            setattr(student, attr, data[attr])

        try:
            db.session.commit()
            return student.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400

    def delete(self, id):
        student = Student.query.get(id)
        if student is None:
            return {"error": "Student not found"}, 404

        try:
            db.session.delete(student)
            db.session.commit()
            return {}, 204
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400


# ------ ENROLLMENTS ------

class Enrollments(Resource):
    def get(self):
        enrollments = Enrollment.query.all()
        return [e.to_dict() for e in enrollments], 200

    def post(self):
        data = request.get_json()

        if "student_id" not in data or "course_id" not in data:
            return {"error": "student_id and course_id are required"}, 400

        student = Student.query.get(data["student_id"])
        if student is None:
            return {"error": "Student not found"}, 404

        course = Course.query.get(data["course_id"])
        if course is None:
            return {"error": "Course not found"}, 404

        enrollment = Enrollment(
            student_id=data["student_id"],
            course_id=data["course_id"],
            progress=data.get("progress"),
            status=data.get("status"),
        )

        try:
            db.session.add(enrollment)
            db.session.commit()
            return enrollment.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400


class EnrollmentById(Resource):
    def get(self, id):
        enrollment = Enrollment.query.get(id)
        if enrollment is None:
            return {"error": "Enrollment not found"}, 404
        return enrollment.to_dict(), 200

    def patch(self, id):
        enrollment = Enrollment.query.get(id)
        if enrollment is None:
            return {"error": "Enrollment not found"}, 404

        data = request.get_json()

        for attr in data:
            setattr(enrollment, attr, data[attr])

        try:
            db.session.commit()
            return enrollment.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400

    def delete(self, id):
        enrollment = Enrollment.query.get(id)
        if enrollment is None:
            return {"error": "Enrollment not found"}, 404

        try:
            db.session.delete(enrollment)
            db.session.commit()
            return {}, 204
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400


# ------ ROUTES ------

api.add_resource(Instructors, "/instructors")
api.add_resource(InstructorById, "/instructors/<int:id>")

api.add_resource(Courses, "/courses")
api.add_resource(CourseById, "/courses/<int:id>")

api.add_resource(Lessons, "/lessons")
api.add_resource(LessonById, "/lessons/<int:id>")

api.add_resource(Students, "/students")
api.add_resource(StudentById, "/students/<int:id>")

api.add_resource(Enrollments, "/enrollments")
api.add_resource(EnrollmentById, "/enrollments/<int:id>")


if __name__ == "__main__":
    app.run(port=5555, debug=True)