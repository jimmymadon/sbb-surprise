import React, { Component, Fragment } from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import {Transition} from 'react-transition-group';
import Spinner from 'react-bootstrap/Spinner';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

const transitionStyles = {
  entering: { opacity: 1 },
  entered:  { opacity: 1 },
  exiting:  { opacity: 0 },
  exited:  { opacity: 0 },
};

class BuyTicketModal extends Component {

  constructor(props) {
    super(props);

    this.state = {loading: false}
  }

  onHide = ()=> {

  }
  
  render() {

    return (
      <Modal
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered
      >
        <Modal.Body centered>
          <Modal.Title id="contained-modal-title-vcenter">
            Buying ticket...
          </Modal.Title>
          <Transition in={true} timeout={5000}>
            {state => (
              <div style={{
                ...transitionStyles[state]
              }}>
                <Fragment>
                  <Row>
                    <Col md={4}></Col>
                    <Col md={4}>
                      <Spinner animation="border" variant="dark" />
                    </Col>
                    <Col md={4}></Col>
                  </Row>
                </Fragment>
              {/* <p>
                Cras mattis consectetur purus sit amet fermentum. Cras justo odio,
                dapibus ac facilisis in, egestas eget quam. Morbi leo risus, porta ac
                consectetur ac, vestibulum at eros.
              </p> */}
              </div>
            )}
          </Transition>
        </Modal.Body>
        <Modal.Footer>
          <Button class="booking-form submit-btn" onClick={this.onHide}>Close</Button>
        </Modal.Footer>
      </Modal>
    );
  }
}

export default BuyTicketModal;