import React, { Component } from 'react';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';

class InputForm extends Component {

  constructor(props) {
    super(props);

    this.state = {
      // isLoading: this.props.isLoading,
      formData: {
        startingLocation: '',
        dateOfTravel: '',
        timeOfTravel: ''
      }
    };
  }

  handleChange = (event) => {
    const value = event.target.value;
    const name = event.target.name;
    var formData = this.state.formData;
    formData[name] = value;
    this.setState({
      formData
    });
  }

  handleSurpriseClick = (handleRequest, event) => {
    const formData = this.state.formData;
    // this.setState({ isLoading: true });
    console.log("Before POST request");
    handleRequest(formData);
  }

  handleCancelClick = (event) => {
    this.setState({ formData: {startingLocation: "", dateOfTravel: "", timeOfTravel: ""} });
  }

  render() {
    // const isLoading = this.state.isLoading;
    const formData = this.state.formData;
    const {onSubmit, isLoading} = this.props;

    return (
      <Form>
        <Form.Group>
          <Form.Label>Your Starting Location</Form.Label>
          <Form.Control
            type="text"
            placeholder="Starting Location"
            name="startingLocation"
            value={formData.startingLocation}
            onChange={this.handleChange} />
          <Form.Label>Date of Travel</Form.Label>
            <Form.Control
              type="date"
              name="dateOfTravel"
              value={formData.dateOfTravel}
              onChange={this.handleChange} />
          <Form.Label>Time of Travel</Form.Label>
            <Form.Control
              type="time"
              name="timeOfTravel"
              value={formData.timeOfTravel}
              onChange={this.handleChange} />
          <Form.Label>SB-Be Crazy Meter!**</Form.Label>
          <div class="slidecontainer">
            <input type="range" min="1" max="100" defaultValue="50" class="slider" id="myRange" />
          </div>
        </Form.Group>
          <Col>
            <Button
              block
              disabled={isLoading}
              onClick={!isLoading ? () => {this.handleSurpriseClick(onSubmit)} : null}>
              { isLoading ? 'Hold your breath!' : 'Surprise Me!' }
            </Button>
          </Col>
      </Form>
    );
  }

}

export default InputForm;