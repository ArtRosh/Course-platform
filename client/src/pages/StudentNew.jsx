// client/src/pages/StudentNew.jsx
import { useNavigate } from "react-router-dom";
import { useFormik } from "formik";
import * as yup from "yup";
import { useData } from "../context/DataContext";

function StudentNew() {
  const navigate = useNavigate();
  const {students, setStudents} = useData()

  const formSchema = yup.object().shape({
    name: yup.string().required("Must enter a name"),
    email: yup.string().email("Invalid email").required("Must enter email"),
  });

  const formik = useFormik({
    initialValues: {
      name: "",
      email: "",
    },
    validationSchema: formSchema,
    onSubmit: (values) => {

      fetch("/students", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(values, null, 2),
      })
        .then(res => res.json())
        .then(data => {
          console.log(data)

          console.log(students)
        })
        
          navigate("/students");
        
    },
  });

  return (
    <div className="container mt-4" style={{ maxWidth: 500 }}>
      <h2 className="mb-3">New Student</h2>

      <div className="card p-4">
        <form onSubmit={formik.handleSubmit}>
          <div className="mb-3">
            <label className="form-label" htmlFor="name">
              Name
            </label>
            <input
              id="name"
              name="name"
              className="form-control"
              onChange={formik.handleChange}
              value={formik.values.name}
            />
            <p className="text-danger">{formik.errors.name}</p>
          </div>

          <div className="mb-4">
            <label className="form-label" htmlFor="email">
              Email
            </label>
            <input
              id="email"
              name="email"
              className="form-control"
              onChange={formik.handleChange}
              value={formik.values.email}
            />
            <p className="text-danger">{formik.errors.email}</p>
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

export default StudentNew;