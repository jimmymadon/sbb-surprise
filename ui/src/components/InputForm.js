import React, { Component } from 'react';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.css';


class InputForm extends Component {

  constructor(props) {
    super(props);

    this.state = {
      // isLoading: this.props.isLoading,
      formData: {
        startingLocation: ''
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
    this.setState({ isLoading: true });
    console.log(formData);
    handleRequest(formData);
  }

  handleCancelClick = (event) => {
    this.setState({ formData: {startingLocation: ""} });
  }

  render() {
    // const isLoading = this.state.isLoading;
    const formData = this.state.formData;
    const {onSubmit, isLoading} = this.props;

    return (
      <Form>
        <Form.Row>
          <Form.Group as={Col}>
            <Form.Label>Starting Location</Form.Label>
            <Form.Control 
              type="text" 
              placeholder="Starting Location" 
              name="startingLocation"
              value={formData.startingLocation}
              onChange={this.handleChange} />
          </Form.Group>
        </Form.Row>
        <Row>
          <Col>
            <Button
              block
              variant="success"
              disabled={isLoading}
              onClick={!isLoading ? () => {this.handleSurpriseClick(onSubmit)} : null}>
              { isLoading ? 'Loading' : 'Surprise Me!' }
            </Button>
          </Col>
          <Col>
            <Button
              block
              variant="danger"
              disabled={isLoading}
              onClick={!isLoading ? this.handleCancelClick : null}>
              { isLoading ? 'Loading' : 'Reset' }
            </Button>
          </Col>
        </Row>
      </Form>
    );
  }

}

export default InputForm;