import React, { Component, Fragment } from 'react';
import './App.css';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import InputForm from "./components/InputForm";
import ResultsList from './components/ResultsList';
import {SwitchTransition, Transition} from 'react-transition-group';

const transitionStyles = {
  entering: { opacity: 1 },
  entered:  { opacity: 1 },
  exiting:  { opacity: 0 },
  exited:  { opacity: 0 },
};

const BookingCTA = () => (
  <Fragment>
    <div class="booking-cta">
      <h1>Where will we take you next?</h1>
      <p>Enter the destination you would like to start from, pick a date and pack your bags to travel to a surprise destination for upto 70% less!
      </p>
    </div>
  </Fragment>
)

class App extends Component {

  constructor(props) {
    super(props);

    this.state = {
      isLoading: false,
      hasResult: false,
      startFetching: false,
      formData: {
        startingLocation: ''
      },
      result: ""
    };
  }

  handleSurpriseRequest = (formData, event) => {
    this.setState({ isLoading: true, startFetching: true });
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
            // result: response.result,
            result: {
              dest: "Zurich",
              start: "10:22",
              ret: "20:00",
              price:"12.80 CHF",
              picUrl: "https://www.adlittle.com/sites/default/files/locations/istock-523202645.jpg",
            },
            isLoading: false,
            startFetching: false,
            hasResult: true
          });
        })
      )
      .catch((error)=> {console.log("ERROR"); console.log(error)})
  }

  render() {
    // const isLoading = this.state.isLoading;
    const formData = this.state.formData;
    const result = this.state.result;
    const {isLoading, startFetching, hasResult} = this.state;

    return (
      <div class="section-center">
        <div class="container">
          <div class="row">
            <div class="col-md-7 col-md-push-5">
              {/* { hasResult ? ( */}
                <SwitchTransition>
                  <Transition in={hasResult} timeout={7000} key={hasResult ? "result" : "cta"}
                addEndListener={(node, done) => node.addEventListener("transitionend", done, false)}
                classNames='fade'>
                  {hasResult ?
                      <ResultsList data={result} key="result" /> :
                      <BookingCTA key="CTA" />
                  }
                </Transition>
                </SwitchTransition>
                
                {/* ) :(
                  <Transition in={!isLoading} timeout={7000} unmountOnExit enter={false}>
                    {state => (
                      <div style={{
                        ...transitionStyles[state]
                      }}>
                        <BookingCTA />
                      </div>
                    )}
                  </Transition>
                ) */}
              {/* } */}
            </div>
            <div class="col-md-4 col-md-pull-7">
              <div class="booking-form">
                <InputForm
                  onSubmit={this.handleSurpriseRequest}
                  isLoading={this.state.isLoading} />
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default App;