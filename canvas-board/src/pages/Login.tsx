import React, { useState } from "react";
import "./Login.css";
import logo from "./background_login.png";
import { IonButton, IonContent, IonText } from "@ionic/react";
import { Link, useHistory } from "react-router-dom";
import { api } from "../config";

const Login: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const history = useHistory();

  const loginUser = () => {
    const data = {
      email: email,
      password: password,
    };

    fetch(`${api}/login`, {
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
    <IonContent>
      <div className="login">
        <img alt="" src={logo} />
        {/* <IonText className="welcome__text">Welcome back to Web Board</IonText> */}
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
          <h5>
            New here? <u>Sign Up Instead</u>
          </h5>
        </Link>
      </div>
    </IonContent>
  );
};

export default Login;
