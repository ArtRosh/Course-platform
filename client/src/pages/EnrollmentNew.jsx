// src/pages/EnrollmentNew.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useFormik } from "formik";
import * as yup from "yup";
import { useData } from "../context/DataContext";

const TERMS = ["Spring", "Summer", "Fall", "Winter"];

function EnrollmentNew() {
  const navigate = useNavigate();
  const { students, courses, setStudents } = useData();

  

  const formSchema = yup.object().shape({
    course_id: yup.string().required("Course is required"),
    student_id: yup.string().required("Student is required"),
    year: yup
      .number()
      .integer()
      .required("Year is required")
      .typeError("Year must be a number"),
    term: yup.string().required("Term is required"),
  });

  const formik = useFormik({
    initialValues: {
      course_id: "",
      student_id: "",
      year: String(new Date().getFullYear()),
      term: "Fall",
    },
    validationSchema: formSchema,
    onSubmit: (values) => {
      fetch("/enrollments", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          course_id: Number(values.course_id),
          student_id: Number(values.student_id),
          year: Number(values.year),
          term: values.term,
        }),
      }).then((res) => res.json())
        .then((data) => {
          console.log(data)

          const student = students.find(s => s.id === data.student_id)

          const course = student.courses.find(c => c.id === Number(values.course_id))

          if (!course) {

            const course = courses.find(c => c.id === data.course_id)

            const adjustStudent = {...student, courses: [{...course, enrollments: [{...data}]}]}
            
            const adjustedStudents = students.map(s =>
              s.id === adjustStudent.id ? adjustStudent : s
          )
          setStudents(adjustedStudents)
          
          } else {

            const adjustCourse = {...course, enrollments: [...course.enrollments, data]}

            const adjustedCourses = student.courses.map(c => c.id === adjustCourse.id ? adjustCourse : c)

            const adjustStudent = {...student, courses: adjustedCourses}

            const adjustedStudents = students.map(s =>
              s.id === adjustStudent.id ? adjustStudent : s
            )
          setStudents(adjustedStudents)
          }

          navigate(
            `/students/${values.student_id}/courses/${values.course_id}/enrollments`
          );
          
        });
    },
  });

  return (
    <div className="container mt-4" style={{ maxWidth: 720 }}>
      <h2 className="mb-3">New Enrollment</h2>

      <div className="card p-4">
        <form onSubmit={formik.handleSubmit}>
          <div className="mb-3">
            <label className="form-label" htmlFor="course_id">
              Course
            </label>
            <select
              id="course_id"
              name="course_id"
              className="form-select"
              onChange={formik.handleChange}
              value={formik.values.course_id}
            >
              <option value="">Select course...</option>
              {courses.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.title}
                </option>
              ))}
            </select>
            <p className="text-danger">{formik.errors.course_id}</p>
          </div>

          <div className="mb-3">
            <label className="form-label" htmlFor="student_id">
              Student
            </label>
            <select
              id="student_id"
              name="student_id"
              className="form-select"
              onChange={formik.handleChange}
              value={formik.values.student_id}
            >
              <option value="">Select student...</option>
              {students.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name}
                </option>
              ))}
            </select>
            <p className="text-danger">{formik.errors.student_id}</p>
          </div>

          <div className="mb-3">
            <label className="form-label" htmlFor="year">
              Year
            </label>
            <input
              id="year"
              name="year"
              className="form-control"
              onChange={formik.handleChange}
              value={formik.values.year}
            />
            <p className="text-danger">{formik.errors.year}</p>
          </div>

          <div className="mb-4">
            <label className="form-label" htmlFor="term">
              Term
            </label>
            <select
              id="term"
              name="term"
              className="form-select"
              onChange={formik.handleChange}
              value={formik.values.term}
            >
              {TERMS.map((t) => (
                <option key={t} value={t}>
                  {t}
                </option>
              ))}
            </select>
            <p className="text-danger">{formik.errors.term}</p>
          </div>

          <div className="d-flex gap-2">
            <button type="submit" className="btn btn-primary">
              Create
            </button>
            <button
              type="button"
              className="btn btn-outline-secondary"
              onClick={() => navigate(-1)}
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default EnrollmentNew;