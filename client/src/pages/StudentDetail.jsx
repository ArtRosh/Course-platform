import { Link, useParams, useNavigate } from "react-router-dom";
import { useData } from "../context/DataContext";

function StudentDetail() {
  
  const { students } = useData();
 
  const { id } = useParams();
 
  const navigate = useNavigate();
  
  const student = students.find((s) => s.id === Number(id));
  
  if (!student) {
    return <p>Loading...</p>;
  }
  
  return (
    <div className="container mt-4">
      <button className="btn btn-outline-secondary mb-3" onClick={() => navigate(-1)}>
        Back
      </button>

      <h2 className="m-0">{student.name}</h2>
      <div className="text-muted mb-4">{student.email}</div>

      <h4 className="mb-2">Courses</h4>

      {student.courses.length === 0 ? (
        <p>No courses yet.</p>
      ) : (
        <ul className="list-group">
          {student.courses.map((course) => (
            <li
              key={course.id}
              className="list-group-item d-flex justify-content-between align-items-center"
            >
              <span className="fw-semibold">{course.title}</span>

              <Link
                className="btn btn-outline-secondary btn-sm"
                to={`/students/${id}/courses/${course.id}/enrollments`}
              >
                View Enrollments
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default StudentDetail;