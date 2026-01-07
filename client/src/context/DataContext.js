import { createContext, useContext, useEffect, useState } from "react";

export const DataContext = createContext();

export function DataProvider({ children }) {
  const [courses, setCourses] = useState([]);
  const [students, setStudents] = useState([{
    courses: [{
      enrollments: []
    }]
  }]);

  useEffect(() => {
    fetch("/courses").then((r) => r.json()).then(setCourses);
    fetch("/students").then((r) => r.json()).then(setStudents);
  }, []);

  return (
    <DataContext.Provider
      value={{
        courses,
        setCourses,
        students,
        setStudents,
      }}
    >
      {children}
    </DataContext.Provider>
  );
}

export function useData() {
  return useContext(DataContext);
}