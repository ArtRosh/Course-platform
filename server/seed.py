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

# --- IT-focused seed content ---
INSTRUCTORS_PRESET = [
    {"name": "Alex Morgan", "email": "alex.morgan@school.dev"},
    {"name": "Priya Nair", "email": "priya.nair@school.dev"},
    {"name": "Diego Santos", "email": "diego.santos@school.dev"},
    {"name": "Mina Park", "email": "mina.park@school.dev"},
    {"name": "Jordan Lee", "email": "jordan.lee@school.dev"},
]

COURSE_CATALOG = [
    {
        "title": "JavaScript Fundamentals",
        "description": "Variables, functions, arrays/objects, scope, conditionals, loops, and debugging. Build small interactive UI features with DOM basics.",
        "lessons": [
            ("JS Setup & Tooling", "Project structure, npm scripts, dev server basics, and how to read browser console errors."),
            ("Variables, Types, and Operators", "Primitive types, coercion, truthy/falsey, and common pitfalls."),
            ("Functions and Scope", "Function declarations/expressions, arrow functions, scope rules, and closures."),
            ("Arrays and Objects", "CRUD operations, iteration patterns, and choosing the right data structure."),
            ("DOM Basics", "Querying elements, handling events, and rendering lists safely."),
            ("Fetch Basics", "Request/response cycle, JSON parsing, error handling, and async flow."),
        ],
    },
    {
        "title": "React Basics",
        "description": "Components, props, state, rendering lists, and basic forms. Learn how UI updates from state changes and how to structure a small SPA.",
        "lessons": [
            ("JSX and Components", "JSX rules, splitting UI into components, and organizing files."),
            ("Props and Component Composition", "Passing data down, reusable components, and common patterns."),
            ("State and Re-renders", "useState, immutability, and how React decides to re-render."),
            ("Lists and Keys", "Rendering collections, stable keys, and avoiding key-related bugs."),
            ("Forms and Controlled Inputs", "Handling input state, submit flows, and simple validation."),
            ("useEffect for Data Fetching", "Loading states, dependency arrays, and handling fetch errors."),
        ],
    },
    {
        "title": "Node.js and Express API",
        "description": "Build REST endpoints with Express, validate input, handle errors, and connect to a database-ready architecture. Focus on practical request handling.",
        "lessons": [
            ("HTTP and REST Review", "Methods, status codes, request bodies, and designing clean endpoints."),
            ("Express Routing", "Route handlers, params, query strings, and middleware basics."),
            ("Validation and Error Handling", "Input checks, centralized error middleware, and predictable responses."),
            ("Authentication Overview", "Sessions vs tokens, password hashing concept, and security basics (high level)."),
            ("API Testing", "Using Postman-like workflows, consistent payloads, and debugging server issues."),
            ("Deployment Basics", "Environment variables, build steps, and logging essentials."),
        ],
    },
    {
        "title": "SQL and Relational Data Modeling",
        "description": "Tables, relationships, joins, and designing schemas. Practice writing queries and modeling one-to-many and many-to-many relationships.",
        "lessons": [
            ("Tables and Constraints", "Primary keys, foreign keys, unique constraints, and why they matter."),
            ("SELECT and Filtering", "WHERE, ORDER BY, LIMIT, and basic aggregations."),
            ("Joins", "INNER/LEFT joins, reading join results, and avoiding duplication surprises."),
            ("Modeling Relationships", "One-to-many vs many-to-many and association tables."),
            ("Indexes and Performance", "What indexes do, when to add them, and tradeoffs."),
            ("Transactions", "Atomic updates and keeping data consistent."),
        ],
    },
    {
        "title": "Flask REST API with SQLAlchemy",
        "description": "Create a Flask backend with SQLAlchemy models, relationships, validations, and REST routes. Practice serialization and error responses.",
        "lessons": [
            ("Flask App Structure", "Blueprint-like organization, config, and request lifecycle."),
            ("SQLAlchemy Models", "Columns, relationships, and setting up a clean domain model."),
            ("Validations", "Required fields, ranges, and raising meaningful errors."),
            ("Serialization", "to_dict patterns, preventing recursion, and controlling nested output."),
            ("CRUD Routes", "GET/POST/PATCH/DELETE and consistent JSON responses."),
            ("Migrations and Seeding", "Schema changes, resets, and deterministic seed data."),
        ],
    },
    {
        "title": "Git and GitHub Workflow",
        "description": "Daily Git usage: commits, branching, pull requests, and resolving conflicts. Learn how to keep a repo clean and collaborate safely.",
        "lessons": [
            ("Core Commands", "init/clone, add/commit, status, log, and diff."),
            ("Branching", "Feature branches, merging, and avoiding direct main commits."),
            ("Pull Requests", "PR flow, code review basics, and clean commit history."),
            ("Conflict Resolution", "Why conflicts happen and how to resolve them correctly."),
            ("Commit Messages", "Writing meaningful messages and grouping changes logically."),
            ("Repo Hygiene", ".gitignore, environment files, and keeping secrets out of Git."),
        ],
    },
    {
        "title": "Testing and Debugging",
        "description": "Write basic tests and debug effectively. Practice reading stack traces, isolating failures, and building confidence in changes.",
        "lessons": [
            ("Debugging Strategy", "Reproduce, isolate, inspect, and confirm fixes."),
            ("Reading Errors", "Stack traces, line numbers, and common runtime mistakes."),
            ("Unit Testing Basics", "What to test, arranging data, and assertions."),
            ("API Testing", "Testing routes, status codes, and response shapes."),
            ("Mocking Overview", "When mocking helps and typical pitfalls."),
            ("Regression Prevention", "Keeping a bug from returning with targeted tests."),
        ],
    },
    {
        "title": "Web Fundamentals: HTML and CSS",
        "description": "Semantic HTML, layouts, responsive design, and styling patterns. Build clean, readable UI with practical CSS techniques.",
        "lessons": [
            ("Semantic HTML", "Accessible structure, forms, and meaningful elements."),
            ("CSS Box Model", "Margin/padding/border, sizing, and layout debugging."),
            ("Flexbox", "Common layout patterns and alignment tricks."),
            ("Grid Basics", "Two-dimensional layouts and practical templates."),
            ("Responsive Design", "Media queries, fluid typography, and mobile-first approach."),
            ("UI Polish", "Spacing, typography, and consistent component styling."),
        ],
    },
    {
        "title": "System Design for Beginners",
        "description": "A practical intro to designing small systems: API boundaries, data flow, scaling concepts, and tradeoffs. Keep it junior-friendly.",
        "lessons": [
            ("Requirements and Scope", "Functional vs non-functional requirements and defining MVP."),
            ("Data Flow", "Where data originates, how it moves, and how to avoid duplication."),
            ("API Boundaries", "Client/server responsibilities and stable interfaces."),
            ("Caching Concepts", "When caching helps and what can go wrong."),
            ("Basic Scalability", "Horizontal vs vertical scaling and bottlenecks."),
            ("Tradeoffs", "Choosing simplicity vs flexibility and documenting decisions."),
        ],
    },
    {
        "title": "TypeScript Essentials",
        "description": "Add types to JavaScript for safer code. Focus on types, interfaces, generics basics, and typing API data in frontend projects.",
        "lessons": [
            ("Why Types", "Common JS bugs that types prevent and how TS helps."),
            ("Core Types", "Primitives, arrays, unions, and narrowing."),
            ("Objects and Interfaces", "Typing objects, optional fields, and readonly."),
            ("Functions", "Typed params/returns and function overload idea."),
            ("Typing API Data", "DTO shapes, runtime vs compile-time checks."),
            ("React + TS Basics", "Typing props, state, and event handlers."),
        ],
    },
]


def clear_data():
    # Delete in FK-safe order
    db.session.query(Enrollment).delete()
    db.session.query(Lesson).delete()
    db.session.query(Course).delete()
    db.session.query(Student).delete()
    db.session.query(Instructor).delete()
    db.session.commit()


def seed_instructors(n=5):
    """
    Uses preset IT-ish instructors first, then fills the rest with Faker.
    """
    instructors = []

    for item in INSTRUCTORS_PRESET[:n]:
        inst = Instructor(name=item["name"], email=item["email"])
        instructors.append(inst)

    remaining = max(0, n - len(instructors))
    for _ in range(remaining):
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


def seed_courses(instructors, n=10):
    """
    Creates IT-focused courses from the catalog (up to n).
    If n is larger than the catalog, it will loop and re-use catalog items with slight suffixes.
    """
    courses = []
    if not instructors:
        raise ValueError("seed_courses: instructors list is empty")

    for i in range(n):
        item = COURSE_CATALOG[i % len(COURSE_CATALOG)]
        suffix = "" if i < len(COURSE_CATALOG) else f" (Section {i // len(COURSE_CATALOG) + 1})"

        c = Course(
            title=item["title"] + suffix,
            description=item["description"],
            instructor=choice(instructors),
        )
        courses.append(c)

    db.session.add_all(courses)
    db.session.commit()
    return courses


def seed_lessons(courses):
    """
    Creates lessons based on the course title by matching the catalog.
    If a course title includes a section suffix, we match by startswith.
    """
    lessons = []
    if not courses:
        return lessons

    # Map base title -> lessons
    catalog_map = {c["title"]: c["lessons"] for c in COURSE_CATALOG}

    for course in courses:
        base_title = course.title.split(" (Section")[0].strip()
        lesson_templates = catalog_map.get(base_title)

        # Fallback (shouldn't happen if courses came from COURSE_CATALOG)
        if not lesson_templates:
            lesson_templates = [
                ("Overview", "Course overview, goals, and expected outcomes."),
                ("Core Concepts", "Key concepts and practical examples."),
                ("Practice", "Hands-on exercises and review."),
            ]

        for idx, (lesson_title, lesson_content) in enumerate(lesson_templates, start=1):
            l = Lesson(
                title=f"Lesson {idx}: {lesson_title}",
                content=lesson_content,
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
        seed_lessons(courses)
        seed_enrollments(students, courses, per_student=(1, 4))

        print("Seed complete.")