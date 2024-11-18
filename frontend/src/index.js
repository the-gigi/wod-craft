//import 'core-js/fn/object/assign';
//import React from 'react';
//import ReactDOM from 'react-dom';
//import App from './components/Main';
//
//// Render the main component into the dom
//ReactDOM.render(<App />, document.getElementById('app'));


import thunkMiddleware from 'redux-thunk'
import createLogger from 'redux-logger'
import { createStore, applyMiddleware } from 'redux'
import { fetchScores } from './actions/actions'
import rootReducer from './reducers'

const loggerMiddleware = createLogger();

const store = createStore(
  rootReducer,
  applyMiddleware(
    thunkMiddleware, // lets us dispatch() functions
    loggerMiddleware // neat middleware that logs actions
  )
);

store.dispatch(fetchScores('gigi')).then(() =>
  console.log(store.getState())
);
