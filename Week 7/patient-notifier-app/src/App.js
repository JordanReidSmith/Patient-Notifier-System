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
    this.resetScreen = this.resetScreen.bind(this)
  }

  handleClick () {
    this.setState({screenState: 'home'});
  }

  resetScreen (){
    this.setState({screenState: 'login'});
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
          <HomeScreen username = {this.state.currentUser} password = {this.state.currentPass} resetScreen = {this.resetScreen}/>
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
      unreadNotifications: 0,
      dataIsLoaded: false
    };

    this.fetchData = this.fetchData.bind(this)

    this.handleClick = this.handleClick.bind(this)
  }

  handleClick (selection) {
    if (selection == 'notis'){
      this.setState({unreadNotifications: 0});
    }
    this.setState({curDisplay: selection});
  }

  fetchData = () => {
    fetch('https://547wxir4gi.execute-api.ap-southeast-2.amazonaws.com/Stage-two/', {
      method: "POST",
      mode: "cors",
      dataType: "JSON",
      headers: {
        "Content-Type": "application/json;",
      },
      body: JSON.stringify({
          username: this.props.username,
          password: this.props.password
      })
    })
    .then(response => response.json())
    .then(response => this.setState({ curDisplay: 'home', notifications: response.notifications, details: response.patientData, unreadNotifications: response.newNotifications, dataIsLoaded: true }));
  }

  componentDidMount() {
    this.fetchData();
  }

  render() {
    if (!this.state.dataIsLoaded){
      return (
        <div>Loading...</div>
      )
    }
    else if (this.state.details == undefined){
      this.props.resetScreen();
    }
    else if (this.state.curDisplay == 'home'){
      return (
        <div>
          <h1>Hello {String(this.state.details).split(",")[0]}</h1>
          <button onClick={() => this.handleClick("details")} style={{display: 'inline-block'}}>details</button>
          <button onClick={() => this.handleClick("notis")} style={{display: 'inline-block'}}>notifications ({this.state.unreadNotifications})</button>
          <button onClick={() => this.handleClick("weights")}>weight entries</button>
          <button onClick={() => this.handleClick("steps")}>step entries</button>
        </div>
      )
    }
    else if (this.state.curDisplay == 'details'){
        return (
          <div>
            <button onClick={() => this.handleClick("home")} >back</button>
            <p>Name: {this.state.details[0][0]}</p>
            <p>E-mail: {this.state.details[0][1]}</p>
            <p>Age: {this.state.details[0][2]}</p>
          </div>
        )
    }
    else if (this.state.curDisplay == 'notis'){
      return (
        <div>
          <button onClick={() => this.handleClick("home")} >back</button>
          <ul className="list-group">
            {this.state.notifications.map(listitem => (
              <li className="list-group-item list-group-item-primary" key={listitem[0]}>
                Date: {listitem[0].slice(0, -6)}/{listitem[0].slice(-6, -4)}/{listitem[0].slice(-4)} - Type: {listitem[1]} - Advice: {listitem[2]}
              </li>
            ))}
          </ul>
        </div>
      )
    }
    else if (this.state.curDisplay == 'weights'){
      return (
        <div>
          <button onClick={() => this.handleClick("home")} >back</button>
          <ul className="list-group">
            {this.state.details[0][3].slice(1,-1).split(',').map(listitem => (
              <li className="list-group-item list-group-item-primary" key={listitem.split(':')[0].trim().slice(1, -1).replaceAll('//','/')}>
                Date: {listitem.split(':')[0].trim().slice(1, -1).replaceAll('//','/')} - Weight: {listitem.split(':')[1]}kg
              </li>
            ))}
          </ul>
        </div>
      )
    }
    else if (this.state.curDisplay == 'steps'){
      return (
        <div>
          <button onClick={() => this.handleClick("home")} >back</button>
          <ul className="list-group">
            {this.state.details[0][4].slice(1,-1).split(',').map(listitem => (
              <li className="list-group-item list-group-item-primary" key={listitem.split(':')[0].trim().slice(1, -1).replaceAll('//','/')}>
                Date: {listitem.split(':')[0].trim().slice(1, -1).replaceAll('//','/')} - Steps: {listitem.split(':')[1]}
              </li>
            ))}
          </ul>
        </div>
      )
    }
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
