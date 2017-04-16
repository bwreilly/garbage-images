import React, { Component } from 'react';
import Autosuggest from 'react-autosuggest';
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
      suggestions: [],
      result: null
    }
  }

  onChange = (event, { newValue }) => {
    this.setState({
      value: newValue
    });
  };

  getSuggestionValue = suggestion => suggestion.text;

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
      });
  };

  onSuggestionsClearRequested = () => {
    this.setState({
      suggestions: []
    });
  };

  renderSuggestion = suggestion => (
    <div>
      <div>{suggestion.result.tags.join(', ')}</div>
      <img src={suggestion.result.image_url} />
    </div>
  );

  onSuggestionSelected = (event, suggestion) => (
    this.setState({result: suggestion.result.image_url})
  )

  render() {
    const { value, suggestions, result } = this.state;
    const inputProps = {
      placeholder: 'Search',
      value,
      onChange: this.onChange
    };
    return (
      <div>
        <Autosuggest
          alwaysRenderSuggestions={true}
          // onSuggestionSelected={this.onSuggestionSelected}
          suggestions={suggestions}
          onSuggestionsFetchRequested={this.onSuggestionsFetchRequested}
          onSuggestionsClearRequested={this.onSuggestionsClearRequested}
          getSuggestionValue={this.getSuggestionValue}
          renderSuggestion={this.renderSuggestion}
          inputProps={inputProps}
        />
        <img src={result} />
      </div>
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
