import React, { useState } from "react";
import "./Login.css";
import logo from "./logo.png";
import { IonButton, IonText } from "@ionic/react";
import { Link, useHistory } from "react-router-dom";

const Login: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const history = useHistory();

  const loginUser = () => {
    const data = {
      email: email,
      password: password,
    };

    fetch("http://localhost:5000/login", {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((token) => {
        localStorage.setItem("access_token", token.access_token);
        history.replace("/");
      })
      .catch((err) => history.replace("/login"));
  };

  return (
    <div className="login">
      <img src={logo} />
      <IonText className="welcome__text">Welcome back to Web Board</IonText>
      <form className="login__form">
        <IonText>Email</IonText>
        <input
          value={email}
          onChange={(e) => {
            setEmail(e.target.value);
          }}
          className="login__formInput"
          type="text"
        />
        <IonText>Password</IonText>
        <input
          value={password}
          onChange={(e) => {
            setPassword(e.target.value);
          }}
          className="login__formInput"
          type="password"
        />
        <IonButton onClick={loginUser} className="login__submit">
          login
        </IonButton>
      </form>
      <Link to="/register">
        <small>dont have account ?</small>
      </Link>
    </div>
  );
};

export default Login;
