import logo from './logo.svg';
import './App.css';
import React from 'react';

class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      screenState: 'login',
      currentUser: '',
      currentPass: ''
    }

    this.handleClick = this.handleClick.bind(this)
    this.handleChange = this.handleChange.bind(this)
  }

  handleClick () {
    this.setState({screenState: 'home'});
  }

  handleChange (val) {
    if (val.target.id=="user"){
      this.setState({currentUser: val.target.value});
    }
    else if (val.target.id=="pass"){
      this.setState({currentPass: val.target.value});
    }
  }

  render() {
    const { screenState } = this.state;

    if (screenState == 'login'){
      return (
        <center>
          <PNSTitle />
          <div>
            <div>
              <h2 style={{display: 'inline-block'}}>Username:</h2>
              <input type="text" id="user" name="user" onChange={this.handleChange} style={{marginLeft: '1em'}}></input>
            </div>
            <div>
              <h2 style={{display: 'inline-block'}}>Password:</h2>
              <input type="text" id="pass" name="pass" onChange={this.handleChange} style={{marginLeft: '1em'}}></input>
            </div>
            <button onClick={this.handleClick}>Login</button>
          </div> 
        </center>
      )
    }
    else {
      return (
        <center>
          <PNSTitle />
          <HomeScreen username = {this.state.currentUser} password = {this.state.currentPass} />
        </center>
      )
    }
  };
}

class HomeScreen extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      curDisplay: 'home',
      notifications: [],
      details: [],
      dataIsLoaded: false
    };

    this.fetchData = this.fetchData.bind(this)

    this.handleClick = this.handleClick.bind(this)
  }

  handleClick () {
    alert(this.state.details);
  }

  fetchData = () => {
    // Simple GET request using fetch
    fetch('https://547wxir4gi.execute-api.ap-southeast-2.amazonaws.com/First-Deployment?username='+this.props.username+'&password='+this.props.password, {
      method: "GET",
      dataType: "JSON",
      headers: {
        "Content-Type": "application/json;"
      }
    })
    .then(response => response.json())
    .then(response => this.setState({ curDisplay: 'home', notifications: response.notifications, details: response.patientData, dataIsLoaded: true }));
  }

  componentDidMount() {
    this.fetchData();
  }

  render() {
    return (
      <div>
      <h1>You be logged in</h1>
      <button onClick={this.handleClick}>See stuff</button>
      </div>
    )
  }
}

class PNSTitle extends React.Component {
  render() {
    return (
      <div>
      <h1>Patient Notifier System</h1>
      </div>
    )
  }
}

export default App;
