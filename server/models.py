from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

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

# --- has many Courses ---
class Instructor(db.Model, SerializerMixin):
    __tablename__ = 'instructors'

    serialize_rules = ("-courses.instructor",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)

    courses = db.relationship("Course", back_populates="instructor")

# --- belongs to Instructor, has many Lessons, has many Enrollments  ---
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

    # --- proxy to get students belongs to the course through Enrollment ---
    students = association_proxy(
        "enrollments",
        "student",
        # --- add new student to the course ---
        creator=lambda student_obj: Enrollment(student=student_obj)
        )

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

    # --- proxy to get courses belongs to the student through Enrollment ---
    courses = association_proxy(
        "enrollments",
        "course",
        # --- add new course to the student ---
        creator=lambda course_obj: Enrollment(course=course_obj)
    )

