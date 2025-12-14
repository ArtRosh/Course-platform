from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates

from config import db


# --- belongs to Course and belongs to Student ---
class Enrollment(db.Model, SerializerMixin):
    __tablename__ = 'enrollments'

    serialize_rules = ("-course.enrollments", "-student.enrollments")

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey('students.id'),
        nullable=False
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey('courses.id'),
        nullable=False
    )

    progress = db.Column(db.Integer)
    status = db.Column(db.String)

    course = db.relationship("Course", back_populates="enrollments")
    student = db.relationship("Student", back_populates="enrollments")

    @validates("progress")
    def validate_progress(self, key, value):
        if value is not None and value < 0:
            raise ValueError("progress must be 0 or greater")
        return value

    @validates("status")
    def validate_status(self, key, value):
        if value is None or value == "":
            raise ValueError("status is required")
        return value


# --- has many Courses ---
class Instructor(db.Model, SerializerMixin):
    __tablename__ = 'instructors'

    serialize_rules = ("-courses.instructor",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)

    courses = db.relationship("Course", back_populates="instructor")

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


# --- belongs to Instructor, has many Lessons, has many Enrollments ---
class Course(db.Model, SerializerMixin):
    __tablename__ = 'courses'

    serialize_rules = (
        "-instructor.courses",
        "-lessons.course",
        "-enrollments.course",
        "-students"
    )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.Text)

    instructor_id = db.Column(
        db.Integer,
        db.ForeignKey('instructors.id'),
        nullable=False
    )

    instructor = db.relationship("Instructor", back_populates="courses")

    lessons = db.relationship("Lesson", back_populates="course")

    enrollments = db.relationship(
        "Enrollment",
        back_populates="course",
        cascade="all, delete-orphan"
    )

    students = association_proxy(
        "enrollments",
        "student",
        creator=lambda student_obj: Enrollment(student=student_obj)
    )

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


# --- belongs to Course ---
class Lesson(db.Model, SerializerMixin):
    __tablename__ = 'lessons'

    serialize_rules = ("-course.lessons",)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.Text)

    course_id = db.Column(
        db.Integer,
        db.ForeignKey('courses.id'),
        nullable=False
    )

    course = db.relationship("Course", back_populates="lessons")

    @validates("title")
    def validate_title(self, key, value):
        if value is None or value == "":
            raise ValueError("title is required")
        return value

    @validates("content")
    def validate_content(self, key, value):
        if value is None or value == "":
            raise ValueError("content is required")
        return value


# --- has many Enrollments ---
class Student(db.Model, SerializerMixin):
    __tablename__ = 'students'

    serialize_rules = (
        "-enrollments.student",
        "-courses"
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)

    enrollments = db.relationship(
        "Enrollment",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    courses = association_proxy(
        "enrollments",
        "course",
        creator=lambda course_obj: Enrollment(course=course_obj)
    )

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