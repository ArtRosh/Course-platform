import { NavLink } from "react-router-dom";

function NavBar() {
  return (
    <nav className="navbar navbar-expand navbar-light bg-light rounded px-3 mb-4">
      

      <div className="navbar-nav">
        
        <NavLink className="nav-link" to="/students">
          Students
        </NavLink>
        
        <NavLink className="nav-link" to="/courses">
          Courses
        </NavLink>

        <NavLink className="nav-link" to="/enrollments/new">
          Enrollments
        </NavLink>

        
      </div>
    </nav>
  );
}

export default NavBar;