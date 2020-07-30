import React from "react";
import "./App.css";

function Dashboard(props) {
  return (
    <div className="Dashboard">
      <h3>{props.name}</h3>
      <p>{props.value}</p>
    </div>
  );
}

export default Dashboard;
