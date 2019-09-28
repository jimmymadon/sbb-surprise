import React, { Component } from 'react';
import './App.css';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import InputForm from "./components/InputForm";
import 'bootstrap/dist/css/bootstrap.css';

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
      <Container>
        <div>
          <h1 className="title">SBB Surprise!</h1>
        </div>
        <div className="content">
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
      </Container>
    );
  }
}

export default App;