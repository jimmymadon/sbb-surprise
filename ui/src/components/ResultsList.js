import React, { Component } from 'react';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Card from 'react-bootstrap/Card';
import Image from 'react-bootstrap/Image';
// import Grid from 'react-bootstrap/Grid';
import '../App.css'

class ResultsList extends Component {
  constructor(props) {
    super(props);

    this.state = {};
  }

  render() {
    const data = this.props.data;
    const {dest, start, priceTot, ret, picUrl} = data;
    console.log(data);
    const priceDecimal = (priceTot/100).toFixed(2);

    return (
      <div>
        {data === "" ? null :
          (
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
                    <Button variant="dark">{priceDecimal} CHF</Button>
                  </Col>
                </Row>
              </Card.Body>
            </Card>
          )
        }
      </div>
      

    );
  }

}

export default ResultsList;