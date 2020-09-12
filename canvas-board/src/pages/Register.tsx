import React from 'react';
import "../App.css"

const Register: React.FC = () => {

    return(
        <div classNameNameName="container">
        <div classNameNameName="img-container">
            <div classNameNameName="text-center">
                <img src="logo.png" classNameNameName="rounded" alt="Logo"/>
            </div>
        </div>
        <div classNameNameName="txt-container">
          <h1 classNameNameName="display-4"> Get on Canvas Web Board!</h1>
        </div>
    </div>
    <div classNameNameName="container">
        <form classNameNameName="register-form">
          <div classNameName="row">
            <div classNameName="form-group col-lg-5 col-sm-5 col-md-6">
              <label classNameName="form-text"for="userName"> Username:</label>
              <input type="userName" classNameName="form-control" id="userName" placeholder="Create your username" name="userName">
            </div>
          </div>
          <div classNameName="row">
            <div classNameName="form-group col-lg-5 col-sm-5 col-md-6">
              <label classNameName="form-text"for="email">Email:</label>
              <input type="email" classNameName="form-control" id="email" placeholder="Enter email" name="email">
            </div>
          </div>
          <div classNameName="row">
            <div classNameName="form-group col-lg-5 col-sm-5 col-md-6">
              <label classNameName="form-text"for="passwrd">Password:</label>
              <input type="password" classNameName="form-control" id="password" placeholder="Create password" name="password">
            </div>
          </div>
          <div classNameName="submit-button">
              <button type="button" classNameName="btn btn-primary btn-lg">Sign Up</button>
          </div>
        </form>
      <h4 classNameName="member-login">I am already a member <u><a href="login.html" classNameName="login-link">Login</a></u> </h4>
    </div>

    );
};

export default Register;