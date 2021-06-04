import React from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";

import Login from "./Authentication/Login";
import Register from "./Authentication/Register";
import LandPage from "./Pages/LandPage";
import Layout from "./Components/Layout";

function App() {
  return (
    <React.Fragment>
      <Router>
        <switch>
          <Route exact path="/" component={LandPage} />
          <Route path="/login" component={Login} />
          <Route path="/registration" component={Register} />
        </switch>
      </Router>
    </React.Fragment>
  );
}

export default App;
