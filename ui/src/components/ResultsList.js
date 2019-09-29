import React, { Component, Fragment } from 'react';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Card from 'react-bootstrap/Card';
import Image from 'react-bootstrap/Image';
import BuyTicketModal from './BuyTicketModal';
import '../App.css'

const ResultsList = (props) => {
    const data = props.data;
    const {dest, start, priceTot, ret, picUrl} = data;
    console.log(data);
    const priceDecimal = (priceTot/100).toFixed(2);
    const [modalShow, setModalShow] = React.useState(false);
    return (
      <div>
        {data === "" ? null :
          (
            <Fragment>
              <Card style={{ width: '34rem' }} border="light">
                <Card.Img variant="top" src={picUrl} />
                <Card.Body>
                  <Card.Title style={{fontWeight: 800}}>{dest}</Card.Title>
                  <Row>
                    <Col md={5}>
                      <Card.Text>
                        Leave at {start}
                      </Card.Text>
                    </Col>
                    <Col md={5}>
                      <Card.Text>
                        Back at {ret}
                      </Card.Text>
                    </Col>
                    <Col md={2}>
                      <Button variant="dark"  onClick={() => setModalShow(true)}>{priceDecimal} CHF</Button>
                    </Col>
                  </Row>
              </Card.Body>
            </Card>
            <BuyTicketModal
              show={modalShow}
              onHide={() => setModalShow(false)}
            />
            </Fragment>
          )
        }
      </div>
      

    );
  }

export default ResultsList;