import React from "react";

import { Form, Button, Container, Col, Row, Image } from "react-bootstrap";
import styled from "styled-components";

import AuthNavbar from "../Components/AuthNavBar";
import logimg from "../Assets/log.jpg";

const Styles = styled.div`
  .demo-img {
    top: 6rem;
    position: absolute;
    height: 450px;
    width: 600px;
  }
  .sign-in-form {
    position: absolute;
    height: 400px;
    width: 300px;
    top: 17rem;
    left: 63rem;
    font-size: 1rem;
    text-anchor: middle;
    color: #252827;
    font-family: "Open Sans", sans-serif;
    font-weight: "bold";
    font-size: 1.02rem;
  }

  .btn-form {
    padding-left: 1.5rem;
    position: relative;
    top: 3rem;
  }

  .sign-in-btn {
    background-color: #f8cf2c;
    color: #000000;
    font-family: "Open Sans", sans-serif;
    position: relative;
    width: 250px;

    &: hover {
      color: white;
    }
  }

  .register-btn {
    color: #000000;
    font-family: "Open Sans", sans-serif;
    top: 5rem;
  }
`;

const Login = () => {
  return (
    <div>
      <AuthNavbar />
      <Styles>
        <Container>
          <Row>
            <Col xs={6} xs={4}>
              <Image src={logimg} rounded className="demo-img" />
            </Col>
          </Row>
        </Container>
        <Container className="demo-form">
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
            </Form>
          </Form>
        </Container>
      </Styles>
    </div>
  );
};

export default Login;
