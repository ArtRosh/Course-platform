from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

# --- belongs to Course and belongs to Student ---
class Enrollment(db.Model):
    __tablename__ = 'enrollments'

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


# --- has many Courses ---
class Instructor(db.Model):
    __tablename__ = 'instructors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)


# --- belongs to Instructor, has many Lessons, has many Enrollments ---
class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.Text)

    instructor_id = db.Column(
        db.Integer,
        db.ForeignKey('instructors.id'),
        nullable=False
    )


# --- belongs to Course ---
class Lesson(db.Model):
    __tablename__ = 'lessons'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.Text)

    course_id = db.Column(
        db.Integer,
        db.ForeignKey('courses.id'),
        nullable=False
    )


# --- has many Enrollments ---
class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)