import React, { Component } from "react";
import "./App.css";

class Form extends Component {
  constructor(props) {
    super(props);
    this.state = {
      page: "",
      ent: "",
      domain: "",
      narrative: "",
    };
  }

  handleentitynameChange = (event) => {
    this.setState({
      entity_name: event.target.value,
    });
  };

  handlesearchpageChange = (event) => {
    this.setState({
      searchpage: event.target.value,
    });
  };

  handlesearchdomainChange = (event) => {
    this.setState({
      searchdomain: event.target.value,
    });
  };

  handlecasenarrativeChange = (event) => {
    this.setState({
      casenarrative: event.target.value,
    });
  };

  render() {
    const { entity_name, searchpage, searchdomain, casenarrative } = this.state;
    return (
      <div class="app">
        <form
          onSubmit={this.handleSubmit}
          action="http://localhost:5000/details"
          method="GET"
        >
          <div class="header">
            <label>
              <h1> Entity Media analyser one stop search</h1>
            </label>
          </div>
          <br></br>
          <br></br>
          <div>
            <label>Enter the Entity name to search</label>
            &nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;
            &nbsp;
            <input
              type="text"
              name="ent"
              SIZE="50"
              value={entity_name}
              onChange={this.handleentitynameChange}
            />
          </div>
          <br></br>
          <div>
            <label>Select the number of page to search</label>
            &nbsp; &nbsp;&nbsp;&nbsp; &nbsp;
            <select
              value={searchpage}
              onChange={this.handlesearchpagechange}
              name="page"
            >
              <option value="5">5</option>
              <option value="10">10</option>
              <option value="15">15</option>
              <option value="20">20</option>
            </select>
            <br></br>
          </div>
          <br></br>
          <div>
            <label>select the country domain to search</label>
            &nbsp; &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;
            <select
              value={searchdomain}
              onChange={this.handlesearchdomainchange}
              name="domain"
            >
              <option value="USA">USA</option>
              <option value="GERMANY">GERMANY</option>
              <option value="SPAIN">SPAIN</option>
              <option value="INDIA">INDIA</option>
            </select>
          </div>
          <br></br>
          <div>
            <label>You want a case narrative of this entity</label>
            &nbsp; &nbsp;&nbsp;
            <select
              value={casenarrative}
              onChange={this.handlecasenarrativechange}
              name="narrative"
            >
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>

          <br></br>
          <button type="Submit">Submit</button>
        </form>
      </div>
    );
  }
}

export default Form;
