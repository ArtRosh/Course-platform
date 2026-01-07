// client/src/pages/EnrollmentEdit.jsx
import { useNavigate, useParams } from "react-router-dom";
import { useFormik } from "formik";
import * as yup from "yup";
import { useData } from "../context/DataContext";

const TERMS = ["Spring", "Summer", "Fall", "Winter"];

function EnrollmentEdit() {
  const { id, student_id, course_id } = useParams();
  const enrollmentId = Number(id);
  const navigate = useNavigate();

  const { courses, students, setStudents } = useData();

  const student = students.find(s => s.id === parseInt(student_id))
  // if (student) {
    
  // }
  const course = student.courses.find(c => c.id === parseInt(course_id))

  const enrollment = course.enrollments.find(e => e.id === parseInt(id))
  
  // let enrollment = null
  
  // let course = null
  
  // let student = null
  

  // for (const s of students) {
  //   for (const c of s.courses) {
  //     for (const e of c.enrollments) {
  //       if (e.id === enrollmentId) {
  //         enrollment = e
  //         course = c
  //         student = s
  //         break
  //       }
  //     }
  //     if (enrollment) break
  //   }
  //   if (enrollment) break
  // }
  // console.log(enrollment)
  // console.log(course)
  // console.log(student)

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
    enableReinitialize: true,
    initialValues: enrollment
      ? {
          course_id: String(enrollment.course_id),
          student_id: String(enrollment.student_id),
          year: String(enrollment.year),
          term: enrollment.term,
        }
      : {
          course_id: "",
          student_id: "",
          year: "",
          term: "Fall",
        },
    validationSchema: formSchema,
    onSubmit: (values) => {
      
      fetch(`/enrollments/${enrollmentId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          course_id: Number(values.course_id),
          student_id: Number(values.student_id),
          year: Number(values.year),
          term: values.term,
        }),
      })
      .then(res => res.json())
      .then((data) => {
        console.log(data)
        // console.log(values)

        const adjustCourse = {...course, enrollments: course.enrollments.map(e => e.id === data.id ? data : e)}
        // console.log(adjustCourse)
        const adjustCourses = student.courses.map(c => c.id === adjustCourse.id ? adjustCourse : c)
        // console.log(adjustCourses)
        const adjustStudent = {...student, courses: adjustCourses}
        // console.log(adjustStudent)
        const adjustStudents = students.map(s => s.id === adjustStudent.id ? adjustStudent : s)
        console.log(adjustStudents)
        setStudents(adjustStudents)

          navigate(-1);
        
      });
    },
  });

  if (!enrollment) return <p>Enrollment not found</p>;

  return (
    <div className="container mt-4" style={{ maxWidth: 720 }}>
      <h2 className="mb-3">Edit Enrollment</h2>

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
              Save
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

export default EnrollmentEdit;