import { Link, useParams, useNavigate } from "react-router-dom";
import { useData } from "../context/DataContext";

function StudentCourseEnrollments() {
  // taking student and course id's, from URL
  const { studentId, courseId } = useParams();
  // console.log(studentId, courseId)
  const navigate = useNavigate();
  // entire data from DataContext
  const { students, setStudents } = useData();
  // find student by id from URL
  const student = students.find((s) => s.id === Number(studentId));
  // console.log(student)
  // let fetch student before read property of it
  if (!student) {
    return <p>Loading...</p>
  }
  // find course by id taken from URL
  const course = student.courses.find((c) => c.id === Number(courseId));
  // console.log(course)

  if (!course) {
    navigate(-1)
    return
  }
  
  function handleDelete(enrollmentId) {
    fetch(`/enrollments/${enrollmentId}`, {method: "DELETE"})
    .then(() => {
      const adjustCourse = {...course, enrollments: course.enrollments.filter(e => e.id !== enrollmentId)}

      const adjustCourses = adjustCourse.enrollments.length === 0 
      ? student.courses.filter(c => c.id !== adjustCourse.id)
      : student.courses.map(c => c.id === adjustCourse.id ? adjustCourse : c)

      const adjustStudent = {...student, courses: adjustCourses}

      const adjustStudents = students.map(s => s.id === adjustStudent.id ? adjustStudent : s)

      setStudents(adjustStudents)
    })
  }

  return (
    <div className="container mt-4">
      
      <div className="d-flex justify-content-between align-items-center mb-3">
          
        <h4 className="m-0">
          
          {student.name} • {course.title}
        </h4>

        <button className="btn btn-outline-secondary btn-sm" onClick={() => navigate(-1)}>
          Back
        </button>
      </div>

      <div className="mb-3">
        <Link
          className="btn btn-primary btn-sm"
          to="/enrollments/new"
          state={{ courseId: Number(courseId), studentId: Number(studentId) }}
        >
          New Enrollment
        </Link>
      </div>

      {course.enrollments.length === 0 ? (
        <p>No enrollments yet.</p>
      ) : (
        <ul className="list-group">
          {course.enrollments.map((e) => (
            <li
              key={e.id}
              className="list-group-item d-flex justify-content-between align-items-center"
            >
              <span>
                {e.term} {e.year}
              </span>

              <div className="d-flex gap-2">
                <Link
                  className="btn btn-outline-secondary btn-sm"
                  to={`/students/${e.student_id}/courses/${e.course_id}/enrollments/${e.id}/edit`}
                >
                  Edit
                </Link>
                <button
                  className="btn btn-outline-danger btn-sm"
                  onClick={() => handleDelete(e.id)}
                >
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default StudentCourseEnrollments;