import React from "react";
import { Nav, Navbar } from "react-bootstrap";
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
`;
export const AuthNavbar = () => (
  <Styles>
      <Navbar expand="lg">
        <Navbar.Brand href="/">CheckIT ?</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="mr-auto"></Nav>
        </Navbar.Collapse>
      </Navbar>
  </Styles>
);

export default AuthNavbar;
