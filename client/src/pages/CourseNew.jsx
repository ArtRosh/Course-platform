// client/src/pages/CourseNew.jsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useFormik } from "formik";
import * as yup from "yup";
import { useData } from "../context/DataContext";

function CourseNew() {
  const navigate = useNavigate();
  const { setCourses } = useData();
  const [serverError, setServerError] = useState("");

  const formSchema = yup.object().shape({
    title: yup.string().required("Must enter a title"),
    description: yup.string().required("Must enter a description"),
  });

  const formik = useFormik({
    initialValues: {
      title: "",
      description: "",
    },
    validationSchema: formSchema,
    onSubmit: (values) => {
      setServerError("");

      fetch("/courses", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(values, null, 2),
      })
        .then((res) => res.json().then((data) => ({ res, data })))
        .then(({ res, data }) => {
          if (!res.ok || data?.error) {
            setServerError(data?.error || "Failed to create course");
            return;
          }

          setCourses((prev) => [data, ...prev]);
          navigate("/courses");
        });
    },
  });

  return (
    <div className="container mt-4" style={{ maxWidth: 700 }}>
      <h2 className="mb-3">New Course</h2>

      {serverError ? (
        <div className="alert alert-danger">{serverError}</div>
      ) : null}

      <div className="card p-4">
        <form onSubmit={formik.handleSubmit}>
          <label className="form-label" htmlFor="title">
            Title
          </label>
          <input
            id="title"
            name="title"
            className="form-control mb-1"
            onChange={formik.handleChange}
            value={formik.values.title}
          />
          <p className="text-danger">{formik.errors.title}</p>

          <label className="form-label" htmlFor="description">
            Description
          </label>
          <textarea
            id="description"
            name="description"
            className="form-control mb-1"
            onChange={formik.handleChange}
            value={formik.values.description}
          />
          <p className="text-danger">{formik.errors.description}</p>

          <button type="submit" className="btn btn-primary">
            Create
          </button>
          <button
            type="button"
            className="btn btn-outline-secondary ms-2"
            onClick={() => navigate(-1)}
          >
            Cancel
          </button>
        </form>
      </div>
    </div>
  );
}

export default CourseNew;