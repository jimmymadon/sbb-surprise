import React, { Component, Fragment } from 'react';
import './App.css';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import InputForm from "./components/InputForm";
import ResultsList from './components/ResultsList';
import {SwitchTransition, Transition} from 'react-transition-group';
import { ToastContainer, toast } from 'react-toastify';

const transitionStyles = {
  entering: { opacity: 1 },
  entered:  { opacity: 1 },
  exiting:  { opacity: 0 },
  exited:  { opacity: 0 },
};

const BookingCTA = () => (
  <Fragment>
    <div class="booking-cta">
      <h1>Where will we take you next?</h1><br/>
      <p>Enter where you are,<br/>
      pick a date,<br/>
      and you'll be on your way to a<br/>
      <span>surprise destination</span> for upto 70% less!
      </p>
      <small>
        **Crazier the surprise, crazier the place and crazier the price!
      </small>
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
    this.setState({ isLoading: true, startFetching: true, result: {} });
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
          if (response.statusCode != 200) {
            throw new Error("Bad Response from API"); 
          }
          const { to, 
                  from, 
                  date, 
                  forward_dep_time, 
                  forward_arr_date, 
                  backward_dep_time,
                  backward_arr_time,
                  price_forward,
                  price_backward
                } = response;
          this.setState({
            result: {
              dest: to,
              start: forward_dep_time,
              ret: backward_arr_time,
              priceTot: price_forward+price_backward,
              priceF: price_forward,
              priceB: price_backward,
              picUrl: "https://www.adlittle.com/sites/default/files/locations/istock-523202645.jpg",
            },
            // MOCKUP
            // result: {
            //   dest: "Zurich",
            //   start: "10:22",
            //   ret: "20:00",
            //   price:"12.80 CHF",
            //   picUrl: "https://www.adlittle.com/sites/default/files/locations/istock-523202645.jpg",
            // },
            isLoading: false,
            startFetching: false,
            hasResult: true
          });
        })
      )
      .catch((error)=> {
        console.log("ERROR");
        console.log(error)
        this.setState( {isLoading: false, startFetching: false});
        toast.error("Sorry something went wrong... We couldn't find any trip four you Location and time!", {
          position: "bottom-center",
          autoClose: 4000,
          hideProgressBar: true,
          closeOnClick: false,
          pauseOnHover: true,
          draggable: true,
          });
      })
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
            <div class="col-md-8 col-md-push-5">
              {/* { hasResult ? ( */}
                <SwitchTransition>
                  <Transition in={hasResult} timeout={500} key={hasResult ? "result" : "cta"}
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
        <ToastContainer
          position="bottom-center"
          autoClose={4000}
          hideProgressBar={true}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnVisibilityChange
          draggable
          pauseOnHover
        />
        </div>
      </div>
    );
  }
}

export default App;