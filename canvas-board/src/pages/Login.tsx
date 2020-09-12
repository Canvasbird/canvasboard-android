import React from "react";
import "./Login.css";
import logo from "./logo.png";
import { IonButton, IonText } from "@ionic/react";
import { Link } from "react-router-dom";

const Login: React.FC = () => {
  return (
    <div className="login">
      <img src={logo} />
      <IonText className="welcome__text">Welcome back to Web Board</IonText>
      <form className="login__form">
        <IonText>Email</IonText>
        <input className="login__formInput" type="text" />
        <IonText>Password</IonText>
        <input className="login__formInput" type="text" />
        <IonButton className="login__submit">login</IonButton>
      </form>
      <Link to="/register">
        <small>dont have account ?</small>
      </Link>
    </div>
  );
};

export default Login;
