import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

class PNSTitle extends React.Component {
  render() {
    return (
      <div>
      <h1>Patient Notifier System</h1>
      </div>
    )
  }
}

class AddNotification extends React.Component {
  render() {
    return (
      <div>
        <div>
          <h2 style={{display: 'inline-block', marginLeft: '2.3em'}}>Notifier Title:</h2>
          <input type="text" id="fname" name="fname" style={{marginLeft: '1em'}}></input>
        </div>
        <div>
          <h2 style={{display: 'inline-block', marginLeft: '-1em'}}>Notifier Description:</h2>
          <input type="text" id="fname" name="fname" style={{marginLeft: '1em'}}></input>
        </div>
        <button>Add</button>
      </div> 
    )
  }
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <center>
    <PNSTitle />
    <AddNotification />
  </center>
);

reportWebVitals();
