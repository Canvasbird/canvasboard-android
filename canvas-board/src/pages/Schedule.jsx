import React, { useState } from "react";
import "./Schedule.css";
import DateTimePicker from "react-datetime-picker";
import { api } from "../config";
import { useHistory } from "react-router-dom";
import { IonContent } from "@ionic/react";
import logo from "./schedule_class.png";

export default function Schedule() {
  const [value_date, onChange] = useState(new Date());
  const [subject, setSubject] = useState("");
  const [facultyName, setFacultyName] = useState("");
  const history = useHistory();

  const submitSchedule = (event) => {
    event.preventDefault();
    // console.log(subject);
    // console.log(facultyName);
    // console.log(value_date);
    const data = {
      subject: subject,
      faculty_name: facultyName,
      date_time: value_date,
    };

    fetch(`${api}/schedule`, {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        "Content-Type": "application/json",
      },
    })
      .then((res) => {
        return res.json();
      })
      .then((data_) => {
        console.log(data_);
        if (data_.msg === "Token has expired") {
          history.replace("/login");
        }
      })
      .catch((err) => history.replace("/login"));
  };

  return (
    <IonContent>
      <div className="schedule">
        {/* <h3>Schedule class</h3> */}
        <img src={logo} alt="" />
        <div className="schedule__form">
          <form>
            <h5>Subject</h5>
            <input
              onChange={(e) => setSubject(e.target.value)}
              type="text"
              className="schedule__formInput"
            />
            <h5>Faculty Name</h5>
            <input
              onChange={(e) => setFacultyName(e.target.value)}
              type="text"
              className="schedule__formInput"
            />
            <h5>Date</h5>
            <DateTimePicker
              onChange={onChange}
              value={value_date}
              className="schedule__formInput Date"
            />
            <div className="schedule__btn">
              <button
                type="submit"
                onClick={submitSchedule}
                className="schedule__formInputBtn"
              >
                Schedule Class
              </button>
            </div>
          </form>
        </div>
      </div>
    </IonContent>
  );
}
