import React from "react";
import "./Main.css";

import { Link } from "react-router-dom";

export default function Main() {
  return (
    <div className="main">
      <div className="btn-container">
        <button type="button" className="btn">
          <Link className="link__btn" to="/camera">
            Start live class
          </Link>
        </button>

        <button type="button" className="btn">
          <Link className="link__btn" to="/schedule">
            Schedule a class
          </Link>
        </button>
        <button type="button" className="btn">
          <Link className="link__btn" to="/classes">
            View scheduled classes
          </Link>
        </button>
      </div>
    </div>
  );
}
