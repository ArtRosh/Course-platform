# Student Enrollment Management System

## Overview
This is a full-stack web application built as a final project that demonstrates how frontend and backend work together as a single, consistent system.  
The application focuses on managing students, courses, and enrollments, with an emphasis on relational data, controlled state updates, and data integrity across the stack.

The project reflects real-world full-stack behavior: the backend defines the data structure and guarantees correctness, while the frontend explicitly manages state updates based on backend responses.


---

## Running the Project Locally

Backend:
pipenv install  
pipenv shell  
flask db upgrade  
python app.py  

Frontend:
npm install  
npm start  

---

## Core Features
- View a list of students
- View courses associated with a student
- View enrollments associated with a course
- Create new enrollments
- Update frontend state without refetching the entire dataset
- Maintain consistent nested state across multiple relationship levels

---

## Data Model
The application is built around three core entities:
- Student
- Course
- Enrollment

### Relationships
- A student has many enrollments
- A course has many enrollments
- An enrollment belongs to one student and one course

These relationships are enforced at the database and model level and mirrored exactly on the frontend.

---

## Backend
Tech stack:
- Python
- Flask
- SQLAlchemy
- SQLite (development)

Responsibilities:
- Define relational data models
- Enforce data integrity through validations
- Handle foreign key constraints
- Return minimal, explicit responses for each request

Creating a new enrollment returns only the created object, not a full updated dataset. This design forces the frontend to manage state updates explicitly.

---

## Frontend
Tech stack:
- React
- JavaScript
- HTML
- CSS

State structure mirrors backend relationships:
students → courses → enrollments

Key concepts:
- Bottom-up state updates
- Strict immutability
- Explicit merging of backend responses into existing state
- Defensive handling of missing or not-yet-loaded data

Nested state updates follow a repeatable pattern:
1. Update enrollments for a specific course
2. Replace that course inside the student
3. Replace the student inside the students array
4. Update top-level state

Skipping any step results in broken state or missing re-renders.

---

## Validation Strategy
Validation is enforced on both sides.

Backend:
- Required fields
- Correct data types
- Valid foreign key relationships

Frontend:
- Input validation for user experience
- Data normalization before requests
- State updates only after successful server responses

Backend validation protects system integrity, while frontend validation improves usability.

---

## Key Learnings
- Backend data models directly define frontend complexity
- Frontend state must match backend responses exactly
- Relational data requires structured, repeatable update patterns
- Immutability is mandatory for reliable React state updates
- Full-stack development is about managing data flow, not screens



## Project Purpose
This project was built to demonstrate practical full-stack skills:
- Designing relational data models
- Managing nested frontend state
- Handling partial backend responses
- Maintaining correctness across frontend and backend boundaries

It reflects patterns commonly used in real production applications rather than simplified academic examples.