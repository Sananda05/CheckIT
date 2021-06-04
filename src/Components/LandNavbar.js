import React from "react";
import { Nav, Navbar, Button, Form } from "react-bootstrap";
import styled from "styled-components";

const Styles = styled.div`
  .navbar {
    background-color: #252827;
  }

  .navbar-brand,
  .navbar-nav,
  .navbar-link {
    color: #f8cf2c;
    padding-left: 2rem;
    font-size: 1.5rem;
    font-family: "Open Sans", sans-serif;

    &: hover {
      color: white;
    }
  }

  .sign-in-form {
    padding-right: 1rem;
  }

  .sign-in-btn {
    background-color: #f8cf2c;
    color: #000000;
    font-family: "Open Sans", sans-serif;
  }

  .register-btn {
    color: #fffee6;
    font-family: "Open Sans", sans-serif;
  }
`;

export const NavigationBar = () => (
  <Styles>
    <Navbar expand="lg">
      <Navbar.Brand href="/">CheckIT ?</Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="mr-auto"></Nav>
        <Form inline className="sign-in-form">
          <Button variant="primary" className="sign-in-btn" href="login">
            Sign in
          </Button>
        </Form>
        <Form inline className="register-form">
          <Button
            variant="outline-warning"
            className="register-btn"
            href="registration"
          >
            Registration
          </Button>
        </Form>
      </Navbar.Collapse>
    </Navbar>
  </Styles>
);

export default NavigationBar;
