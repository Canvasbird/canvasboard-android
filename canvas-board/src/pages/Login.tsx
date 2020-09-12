import React from 'react';
import "./App.css";

const Login: React.FC = () => {

    return (
        <div className="container">
        <div className="img-container">
            <div className="text-center">
                <img src="logo.png" class="rounded" alt="Logo"/>
            </div>
        </div>
        <div className="txt-container">
          <h1 className="display-4">Hello there, Welcome Back!</h1>
        </div>
    </div>
    <div className="container">
      <form className="register-form">
        <div className="row">
          <div className="form-group col-lg-5 col-sm-5 col-md-6">
            <label className="form-text"for="userName"> Username:</label>
            <input type="userName" class="form-control" id="userName" placeholder="Create your username" name="userName">
          </div>
        </div>
        <div className="row">
          <div className="form-group col-lg-5 col-sm-5 col-md-6">
            <label className="form-text"for="passwrd">Password:</label>
            <input type="password" class="form-control" id="password" placeholder="Create password" name="password">
          </div>
        </div>
        <div className="submit-button">
            <button type="button" className="btn btn-primary btn-lg">Log In</button>
        </div>
      </form>
      <h4 className="member-login">New here? <u><a href="index.html" className="login-link">Sign Up Instead</a></u> </h4>
    );
};

export default Login;