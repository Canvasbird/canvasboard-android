import React from "react";
import "./ClassItem.css";

export default function ClassItem({ facultyName, subject, date_time }) {
  return (
    <div className="classItem">
      <h4>{facultyName}</h4>
      <h4>{subject}</h4>
      <h4>{date_time}</h4>
    </div>
  );
}
