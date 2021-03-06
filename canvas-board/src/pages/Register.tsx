import React, { useState } from "react";
import "./Register.css";
import logo from "./background_register.png";
import { IonButton, IonText, IonContent } from "@ionic/react";
import { Link, useHistory } from "react-router-dom";
import { api } from "../config";

const Register: React.FC = () => {
  const [username, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const history = useHistory();

  const registerUser = (event: any) => {
    event.preventDefault();
    const data = {
      username: username,
      password: password,
      email: email,
    };

    fetch(`${api}/register`, {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((msg) => {
        console.log(msg);
        history.push("/login");
      });
  };

  return (
    <IonContent>
      <div className="register">
        <img alt="" src={logo} />
        {/* <IonText className="welcome__text">Welcome to Web Board</IonText> */}
        <form className="register__form">
          <IonText>Username</IonText>
          <input
            value={username}
            onChange={(e) => setUserName(e?.target.value)}
            className="register__formInput"
            type="text"
          />
          <IonText>Email</IonText>
          <input
            value={email}
            onChange={(e) => setEmail(e?.target.value)}
            className="register__formInput"
            type="email"
          />
          <IonText>Password</IonText>
          <input
            value={password}
            onChange={(e) => setPassword(e?.target.value)}
            className="register__formInput"
            type="password"
          />
          <IonButton onClick={registerUser} className="register__submit">
            register
          </IonButton>
        </form>
        <Link to="/login">
          <h5>
            Already a member? <u>Login here</u>
          </h5>
        </Link>
      </div>
    </IonContent>
  );
};

export default Register;
