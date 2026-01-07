import Layout from "./components/Layout";
import Home from "./pages/Home";
import ErrorPage from "./pages/ErrorPage";

import Courses from "./pages/Courses";
import CourseNew from "./pages/CourseNew";

import Students from "./pages/Students";
import StudentDetail from "./pages/StudentDetail";
import StudentNew from "./pages/StudentNew";

import EnrollmentNew from "./pages/EnrollmentNew";
import EnrollmentEdit from "./pages/EnrollmentEdit";
import StudentCourseEnrollments from "./pages/StudentCourseEnrollments";


const routes = [
  {
    path: "/",
    element: <Layout />,
    errorElement: <ErrorPage />,
    children: [
      { path: "", element: <Home /> },

      // Courses
      { path: "courses", element: <Courses /> },
      { path: "courses/new", element: <CourseNew /> },

      // Students
      { path: "students", element: <Students /> },
      { path: "students/new", element: <StudentNew /> },
      { path: "students/:id", element: <StudentDetail /> },

      // Enrollments
      { path: "enrollments/new", element: <EnrollmentNew /> },
      { path: "students/:student_id/courses/:course_id/enrollments/:id/edit", element: <EnrollmentEdit /> },
      { path: "courses/enrollments/new", element: <EnrollmentNew /> },
      {
        path: "students/:studentId/courses/:courseId/enrollments",
        element: <StudentCourseEnrollments />,
      }
      
    ],
  },
];

export default routes;