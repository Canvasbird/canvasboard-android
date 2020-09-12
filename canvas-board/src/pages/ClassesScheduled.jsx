import React, { useEffect, useState } from "react";
import "./ClassesScheduled.css";

import ClassItem from "../components/ClassItem";
import { api } from "../config";

import { useHistory } from "react-router-dom";

export default function ClassesScheduled() {
  const [classes, setClasses] = useState([]);
  const history = useHistory();

  useEffect(() => {
    fetch(`${api}/classes`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
    })
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        console.log(data);
        if (data.msg === "Token has expired") {
          history.replace("/login");
        }
        setClasses(data);
      });
  }, []);

  const renderClasses = () => {
    return classes.map((element, i) => {
      return (
        <ClassItem
          key={i}
          facultyName={element.faculty_name}
          subject={element.subject}
          date_time={element.date_time}
        />
      );
    });
  };

  return (
    <div className="classesScheduled">
      <h2>Upcomming Live classes</h2>
      <div className="classesScheduled__list">{renderClasses()}</div>
    </div>
  );
}
