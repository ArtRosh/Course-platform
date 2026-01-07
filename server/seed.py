#!/usr/bin/env python3

from random import randint, choice
from faker import Faker

from config import app, db
from models import Course, Student, Enrollment

fake = Faker()

TERMS = ["Fall", "Spring", "Summer"]

COURSE_CATALOG = [
    {
        "title": "JavaScript Fundamentals",
        "description": "Variables, functions, arrays/objects, scope, conditionals, loops, and debugging. Build small interactive UI features with DOM basics.",
    },
    {
        "title": "React Basics",
        "description": "Components, props, state, rendering lists, and basic forms. Learn how UI updates from state changes and how to structure a small SPA.",
    },
    {
        "title": "Node.js and Express API",
        "description": "Build REST endpoints with Express, validate input, handle errors, and connect to a database-ready architecture. Focus on practical request handling.",
    },
    {
        "title": "SQL and Relational Data Modeling",
        "description": "Tables, relationships, joins, and designing schemas. Practice writing queries and modeling one-to-many and many-to-many relationships.",
    },
    {
        "title": "Flask REST API with SQLAlchemy",
        "description": "Create a Flask backend with SQLAlchemy models, relationships, validations, and REST routes. Practice serialization and error responses.",
    },
    {
        "title": "Git and GitHub Workflow",
        "description": "Daily Git usage: commits, branching, pull requests, and resolving conflicts. Learn how to keep a repo clean and collaborate safely.",
    },
    {
        "title": "Testing and Debugging",
        "description": "Write basic tests and debug effectively. Practice reading stack traces, isolating failures, and building confidence in changes.",
    },
    {
        "title": "Web Fundamentals: HTML and CSS",
        "description": "Semantic HTML, layouts, responsive design, and styling patterns. Build clean, readable UI with practical CSS techniques.",
    },
    {
        "title": "System Design for Beginners",
        "description": "A practical intro to designing small systems: API boundaries, data flow, scaling concepts, and tradeoffs. Keep it junior-friendly.",
    },
    {
        "title": "TypeScript Essentials",
        "description": "Add types to JavaScript for safer code. Focus on types, interfaces, generics basics, and typing API data in frontend projects.",
    },
]


def clear_data():
    db.session.query(Enrollment).delete()
    db.session.query(Course).delete()
    db.session.query(Student).delete()
    db.session.commit()


def seed_students(n=1):
    students = []
    for _ in range(n):
        students.append(
            Student(
                name=fake.name(),
                email=fake.unique.email(),
            )
        )
    db.session.add_all(students)
    db.session.commit()
    return students


def seed_courses(n=10):
    courses = []
    for i in range(n):
        item = COURSE_CATALOG[i % len(COURSE_CATALOG)]
        courses.append(
            Course(
                title=item["title"],
                description=item["description"],
            )
        )
    db.session.add_all(courses)
    db.session.commit()
    return courses


def seed_enrollments(students, courses, per_student=(1, 4)):
    enrollments = []
    for student in students:
        how_many = randint(*per_student)
        chosen_courses = {choice(courses) for _ in range(how_many)}

        for course in chosen_courses:
            enrollments.append(
                Enrollment(
                    student=student,
                    course=course,
                    term=choice(TERMS),
                    year=randint(2021, 2025),
                )
            )

    db.session.add_all(enrollments)
    db.session.commit()
    return enrollments


if __name__ == "__main__":
    with app.app_context():
        print("Starting seed...")

        clear_data()

        students = seed_students(n=10)
        courses = seed_courses(n=10)
        seed_enrollments(students, courses)

        print("Seed complete.")