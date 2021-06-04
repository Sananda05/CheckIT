import React from "react";

import { Form, Button } from "react-bootstrap";
import styled from "styled-components";

import AuthNavbar from "../Components/AuthNavBar";

const Styles = styled.div`
  .sign-in-form {
    position: absolute;
    height: 200px;
    width: 500px;
    top: 15rem;
    left: 32rem;
    font-size: 1rem;
    text-anchor: middle;
  }

  .btn-form {
    padding-left: 9rem;
    position : relative;
    top : 3rem;
  }

  .sign-in-btn {
    background-color: #f8cf2c;
    color: #000000;
    font-family: "Open Sans", sans-serif;
    position : relative;
    margin-right : 2rem;
    width : 105px;
  }

  .register-btn {
    color:#000000;
    font-family: "Open Sans", sans-serif;
    top : 5rem;
  }
`;

const Login = () => {
  return (
    <div>
      <AuthNavbar />
      <Styles>
        <Form className="sign-in-form">
          <Form.Group controlId="formGroupEmail">
            <Form.Label>Email address</Form.Label>
            <Form.Control type="email" placeholder="Enter email" />
          </Form.Group>
          <Form.Group controlId="formGroupPassword">
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" placeholder="Password" />
          </Form.Group>
          <Form inline className="btn-form">
            <Button variant="primary" className="sign-in-btn">
              Sign in
            </Button>
            <Button
              variant="outline-warning"className="register-btn"href="registration">
              Registration
            </Button>
          </Form>
        </Form>
      </Styles>
    </div>
  );
};

export default Login;
