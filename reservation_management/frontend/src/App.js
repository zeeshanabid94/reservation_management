import React, { Component } from 'react';
import { instanceOf } from 'prop-types';
import logo from './logo.svg';
import './App.css';
import Calendar from './components/calendar/calendar'
import { CookiesProvider, withCookies, Cookies } from 'react-cookie';
class App extends Component {
  static propTypes = {
    cookies: instanceOf(Cookies).isRequired
  };

  constructor(props) {
    super(props);
    const { cookies } = props;
    this.state = {
      csrftoken: cookies.get('csrftoken')
    };
    console.log(cookies);
  }

  render() {
    return (
      <CookiesProvider>
        <div className="App">
          <Calendar length={6} width={7}></Calendar>
        </div>
      </CookiesProvider>
    );
  }
}

export default withCookies(App);
