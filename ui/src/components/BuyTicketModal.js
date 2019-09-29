import React, { Component, Fragment } from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import {Transition} from 'react-transition-group';
import Spinner from 'react-bootstrap/Spinner';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import ModalHeader from 'react-bootstrap/ModalHeader';

const transitionStyles = {
  entering: { opacity: 1 },
  entered:  { opacity: 1 },
  exiting:  { opacity: 0 },
  exited:  { opacity: 0 },
};

class BuyTicketModal extends Component {

  constructor(props) {
    super(props);

    this.state = {loading: true}
  }

  fakeBuy = new Promise(function(resolve, reject) {
    setTimeout(function() {
      resolve('foo');
    }, 5000);
  });
  componentDidMount(){
    this.fakeBuy.then(()=>{
      this.setState({loading: false})
    });
  }
  
  render() {
    const loading = this.state.loading;
    return (
      <Modal
        {...this.props}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered
      >
        <Modal.Body style={{padding: 25}}>
          {/* <ModalHeader> */}
          <Modal.Title id="contained-modal-title-vcenter">
            Buying ticket...
          </Modal.Title>

          {/* </ModalHeader> */}
          {/* <Transition in={true} timeout={5000}>
            {state => (
              <div style={{
                ...transitionStyles[state]
              }}> */}
              {
                loading ? (
                  <Fragment>
                    <Row>
                      <Col md={4}></Col>
                      <Col md={4} style={{alignContent: 'center'}}>
                        <Spinner animation="border" variant="dark" />
                      </Col>
                      <Col md={4}></Col>
                    </Row>
                  </Fragment>
                ) : (
                  <Fragment>
                    <Row>
                    <h5>Purchase Complete!</h5>
                    </Row>
                    <Row>
                      Prepare your backpack ... you are going on an adventure!
                    </Row>
                  </Fragment>
                )
              }
                
              {/* </div>
            )}
          </Transition> */}
        </Modal.Body>
        <Modal.Footer>
          <Button class="btn" onClick={this.props.onHide}>Close</Button>
        </Modal.Footer>
      </Modal>
    );
  }
}

export default BuyTicketModal;