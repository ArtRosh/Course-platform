// client/src/pages/Courses.jsx
import { Link } from "react-router-dom";
import { useData } from "../context/DataContext";

function Courses() {
  const { courses } = useData();

  return (
    <div>
      <div className="d-flex justify-content-between align-items-start mb-4">
        <h2 className="m-0">Courses</h2>

        <div className="d-flex flex-column gap-2 align-items-end">
          <Link className="btn btn-primary" to="/courses/new">
            New Course
          </Link>
        </div>
      </div>
   

      {courses.length === 0 ? (
        <p>No courses yet.</p>
      ) : (
        <ul className="list-group">
          {courses.map((course) => (
            <li
              key={course.id}
              className="list-group-item d-flex justify-content-between align-items-start"
            >
              <div className="me-3">
                <div className="fw-semibold">{course.title}</div>
                {course.description ? (
                  <div className="text-muted small">{course.description}</div>
                ) : null}
              </div>

              
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Courses;