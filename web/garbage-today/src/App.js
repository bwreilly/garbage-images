import React, { Component } from 'react';
import Autosuggest from 'react-autosuggest';
import _ from 'lodash';
import logo from './logo.png';
import './App.css';


class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="App-header">
          <span>
            <img className='Logo' src={logo} />
            <h1>Garbage, today!</h1>
          </span>
        </div>
        <Search />
        <Footer />
      </div>
    );
  }
}

class Footer extends Component {
  render() {
    const small = {fontSize: 'small'}
    return (
      <footer className='Footer'>
        <span style={small}>
          <a href='mailto:admin@garbage.today'>Contact</a> for submissions and attribution/takedown requests.
        </span>
      </footer>
    )
  }
}

class Search extends Component {
  render() {
    return (
      <div>
        <SearchForm />
      </div>
    )
  }
}

class SearchForm extends Component {
  constructor(props) {
    super(props);
    this.autocomplete = `https://iibg6hc573.execute-api.us-west-1.amazonaws.com/dev/complete/`;
    this.state = {
      value: '',
      suggestions: [],
      result: null
    };
    this.debouncedLoadSuggestions = _.debounce(this.loadSuggestions, 200);
  }

  onChange = (event, { newValue }) => {
    this.setState({
      value: newValue
    });
  };

  getSuggestionValue = suggestion => suggestion.text;

  loadSuggestions(value) {
    this.onSuggestionsClearRequested();
    const url = this.autocomplete;
    fetch(`${url}${value}`)
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        if (Array.isArray(data)) {
          this.setState({suggestions: data});
        }
      });
  }

  onSuggestionsFetchRequested = ({ value }) => {
    this.debouncedLoadSuggestions(value);
  };

  onSuggestionsClearRequested = () => {
    this.setState({
      suggestions: []
    });
  };

  renderSuggestion = suggestion => (
    <div className="Result" id={suggestion.result.name}>
      <div>{suggestion.result.tags.join(', ')}</div>
      <img className="Image-preview"
           src={suggestion.result.image_url}
           alt={suggestion.result.name} />
    </div>
  );

  onSuggestionSelected = (e, {suggestion}) => (
    this.setState({result: suggestion.result.image_url})
  )

  onFocus = e => {
    this.setState({result: null})
  }

  render() {
    const { value, suggestions, result } = this.state;
    const inputProps = {
      placeholder: 'Search',
      value,
      onChange: this.onChange,
      onFocus: this.onFocus,
      className: 'Search-input'
    };
    return (
      <div>
        <Autosuggest
          onSuggestionSelected={this.onSuggestionSelected}
          suggestions={suggestions}
          onSuggestionsFetchRequested={this.onSuggestionsFetchRequested}
          onSuggestionsClearRequested={this.onSuggestionsClearRequested}
          getSuggestionValue={this.getSuggestionValue}
          renderSuggestion={this.renderSuggestion}
          inputProps={inputProps}
        />
        <Result result={result} />
      </div>
    )
  }
}

const urlParser = (url) => {
  // creating a new unused element, that's a cool trick
  // https://gist.github.com/jlong/2428561
  let parser = document.createElement('a');
  parser.href = url;
  return parser;
}

const replaceDomain = (url, domain = 'img.garbage.today') => {
  const parsed = urlParser(url);
  const oldDomain = parsed.hostname;
  return url.replace(oldDomain, domain);
}

class Result extends Component {

  select(e) {
    e.target.select();
  }

  render() {
    if (this.props.result) {
      const correctedUrl = replaceDomain(this.props.result)
      return (
        <div>
          <img src={this.props.result} />
          <input
            autoFocus={true}
            onFocus={this.select}
            className='Copy-field'
            type="text"
            value={correctedUrl} />
        </div>
      )
    } else {
      return null;
    }
  }
}

export default App;
