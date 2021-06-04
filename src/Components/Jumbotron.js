import React from "react";
import { Jumbotron, Container, Image, Row } from "react-bootstrap";
import styled from "styled-components";

import Img from "../Assets/landpage.jpg";

const Styles = styled.div`
  .jumbo {
    background-color: #252827;
    background-size: cover;
    color: #f8cf2c;
    height: 400px;
    top: 10rem;
    position: relative;
    z-index: -2;
  }
  .next-line {
    color: #fffee6;
    
  }

  .overlay {
    position: absolute;
    top: -1.5rem;
    left: 58rem;
    right: 7rem;
    z-index: -2;
  }
`;

const Jumbo = () => (
  <Styles>
    <Jumbotron fluid className="jumbo">
      <Container>
        <h1 className="heading">Welcome !</h1>
        <p className="next-line">
          Easier and Effiect way to check your answer scripts and save some
          valuable time!
        </p>
        <div className="overlay">
          <Row>
            <Image src={Img} roundedCircle />
          </Row>
        </div>
      </Container>
    </Jumbotron>
  </Styles>
);

export default Jumbo;
