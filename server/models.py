# models.py
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from config import db


class Enrollment(db.Model, SerializerMixin):
    __tablename__ = "enrollments"

    
    serialize_rules = (
        "-student",
        "-course",
    )

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)

    year = db.Column(db.Integer)
    term = db.Column(db.String)

    student = db.relationship("Student", back_populates="enrollments")
    course = db.relationship("Course", back_populates="enrollments")


class Course(db.Model, SerializerMixin):
    __tablename__ = "courses"

    serialize_rules = (
        "-students",
    )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.Text)

    enrollments = db.relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    students = db.relationship("Student", secondary="enrollments", viewonly=True, back_populates="courses")

    @validates("title")
    def validate_title(self, key, value):
        if value is None or value == "":
            raise ValueError("title is required")
        return value

    @validates("description")
    def validate_description(self, key, value):
        if value is None or value == "":
            raise ValueError("description is required")
        return value


class Student(db.Model, SerializerMixin):
    __tablename__ = "students"

    serialize_rules = (
        "-enrollments",
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)

    enrollments = db.relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")
    courses = db.relationship("Course", secondary="enrollments", viewonly=True, back_populates="students")

    @validates("name")
    def validate_name(self, key, value):
        if value is None or value == "":
            raise ValueError("name is required")
        return value

    @validates("email")
    def validate_email(self, key, value):
        if value is None or value == "":
            raise ValueError("email is required")
        if "@" not in value:
            raise ValueError("Invalid email")
        return value
    