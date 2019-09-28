import React, { Component } from 'react';
import './App.css';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import InputForm from "./components/InputForm";

class App extends Component {

  constructor(props) {
    super(props);

    this.state = {
      isLoading: false,
      formData: {
        startingLocation: ''
      },
      result: ""
    };
  }

  handleSurpriseRequest = (formData, event) => {
    fetch('http://127.0.0.1:5000/prediction/',
      {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': '*',
          'Access-Control-Allow-Methods': '*',
        },
        method: 'POST',
        body: JSON.stringify(formData)
      })
      .then(response => response.json()
        .then(response => {
          console.log(response)
          this.setState({
            result: response.result,
            isLoading: false
          });
          console.log("blblbl")
        })
      )
      .catch((error)=> {console.log("ERROR"); console.log(error)})
  }

  render() {
    const isLoading = this.state.isLoading;
    const formData = this.state.formData;
    const result = this.state.result;

    return (
      <div class="section-center">
        <div class="container">
          <div class="row">
            <div class="col-md-7 col-md-push-5">
              <div class="booking-cta">
                <h1>Where will we take you next?</h1>
                <p>Enter the destination you would like to start from, pick a date and pack your bags to travel to a surpirse destination for upto 70% less!
                </p>
              </div>
            </div>
            <div class="col-md-4 col-md-pull-7">
              <div class="booking-form">
                <InputForm
                  onSubmit={this.handleSurpriseRequest}
                  isLoading={this.state.isLoading} />
                {result === "" ? null :
                  (<Row>
                    <Col className="result-container">
                      <h5 id="result">{result}</h5>
                    </Col>
                  </Row>)
                }
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default App;