// client/src/pages/Students.jsx
import { Link } from "react-router-dom";
import { useData } from "../context/DataContext";

function Students() {
  const { students } = useData();

  if (students.length === 0) {
    return <p>No students yet.</p>;
  }

  return (
    <div>
      <div className="d-flex justify-content-between mb-3">
        <h2>Students</h2>
        <Link className="btn btn-primary" to="/students/new">
          New Student
        </Link>
      </div>

      <ul className="list-group">
        {students.map((s) => (
          <li
            key={s.id}
            className="list-group-item d-flex justify-content-between"
          >
            <div>
              <div>{s.name}</div>
              {s.email && <div className="text-muted">{s.email}</div>}
            </div>

            <Link
              className="btn btn-outline-secondary btn-sm"
              to={`/students/${s.id}`}
            >
              View Courses
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Students;