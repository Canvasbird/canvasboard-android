import React from "react";
import "./Register.css";
import logo from "./logo.png";
import { IonButton, IonText } from "@ionic/react";
import { Link } from "react-router-dom";

const Register: React.FC = () => {
  return (
    <div className="register">
      <img src={logo} />
      <IonText className="welcome__text">Welcome to Web Board</IonText>
      <form className="register__form">
        <IonText>Username</IonText>
        <input className="register__formInput" type="text" />
        <IonText>Email</IonText>
        <input className="register__formInput" type="text" />
        <IonText>Password</IonText>
        <input className="register__formInput" type="text" />
        <IonButton className="register__submit">register</IonButton>
      </form>
      <Link to="/login">
        <small>already a member ?</small>
      </Link>
    </div>
  );
};

export default Register;
