#!/usr/bin/env python3

# Standard library imports
from random import randint, choice

# Remote library imports
from faker import Faker

# Local imports
from config import app, db
from models import Instructor, Course, Lesson, Student, Enrollment

fake = Faker()

STATUSES = ["active", "completed", "dropped", "paused"]


def clear_data():
    # Delete in FK-safe order
    db.session.query(Enrollment).delete()
    db.session.query(Lesson).delete()
    db.session.query(Course).delete()
    db.session.query(Student).delete()
    db.session.query(Instructor).delete()
    db.session.commit()


def seed_instructors(n=5):
    instructors = []
    for _ in range(n):
        inst = Instructor(
            name=fake.name(),
            email=fake.unique.email(),
        )
        instructors.append(inst)
    db.session.add_all(instructors)
    db.session.commit()
    return instructors


def seed_students(n=20):
    students = []
    for _ in range(n):
        st = Student(
            name=fake.name(),
            email=fake.unique.email(),
        )
        students.append(st)
    db.session.add_all(students)
    db.session.commit()
    return students


def seed_courses(instructors, n=8):
    courses = []
    for i in range(n):
        c = Course(
            title=f"{fake.word().capitalize()} {fake.word().capitalize()}",
            description=fake.text(max_nb_chars=240),
            instructor=choice(instructors),
        )
        courses.append(c)
    db.session.add_all(courses)
    db.session.commit()
    return courses


def seed_lessons(courses, lessons_per_course=(3, 7)):
    lessons = []
    for course in courses:
        count = randint(*lessons_per_course)
        for i in range(1, count + 1):
            l = Lesson(
                title=f"Lesson {i}: {fake.sentence(nb_words=4).rstrip('.')}",
                content=fake.text(max_nb_chars=600),
                course=course,
            )
            lessons.append(l)
    db.session.add_all(lessons)
    db.session.commit()
    return lessons


def seed_enrollments(students, courses, per_student=(1, 4)):
    enrollments = []
    for student in students:
        how_many = randint(*per_student)
        chosen_courses = {choice(courses) for _ in range(how_many)}  # avoid duplicates
        for course in chosen_courses:
            e = Enrollment(
                student=student,
                course=course,
                progress=randint(0, 100),
                status=choice(STATUSES),
            )
            enrollments.append(e)

    db.session.add_all(enrollments)
    db.session.commit()
    return enrollments


if __name__ == "__main__":
    with app.app_context():
        print("Starting seed...")

        clear_data()

        instructors = seed_instructors(n=5)
        students = seed_students(n=25)
        courses = seed_courses(instructors, n=10)
        seed_lessons(courses, lessons_per_course=(3, 8))
        seed_enrollments(students, courses, per_student=(1, 4))

        print("Seed complete.")