import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';


class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="App-header">
          <h2>Garbage, today!</h2>
        </div>
        <Search />
      </div>
    );
  }
}

class Search extends Component {
  render() {
    return (
      <div>
        <SearchForm />
        <SearchResults />
      </div>
    )
  }
}

class SearchForm extends Component {
  constructor(props) {
    super(props);
    this.url = `/dev/search/`;  // TODO: we get a _source in /complete, so this is superfluous
    this.autocomplete = `/dev/complete/`;
    this.state = {
      value: '',
      suggestions: []
    }
  }

  onChange = (event, { newValue }) => {
    this.setState({
      value: newValue
    });
  };

  onSuggestionsFetchRequested = ({ value }) => {
    const url = this.autocomplete;
    fetch(`${url}${value}`)
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        // TODO: always return an array or a real error
        if (Array.isArray(data)) {
          this.setState({suggestions: data});
        }
      })
  };

  render() {
    return (
      <div />
    )
  }
}

class SearchResults extends Component {
  render() {
    return (
      <div />
    )
  }
}

class Result extends Component {
  render() {
    return (
      <div />
    )
  }
}

export default App;
