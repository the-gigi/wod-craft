import fetch from 'isomorphic-fetch'

export const REQUEST_SCORES = 'REQUEST_SCORES';
function requestScores(user) {
  return {
    type: REQUEST_SCORES,
    user: user
  }
}

export const RECEIVE_SCORES = 'RECEIVE_SCORES';
function receiveScores(user, json) {
  return {
    type: RECEIVE_SCORES,
    user: user,
    scores: json.result,
    receivedAt: Date.now()
  }
}


export function fetchScores(user) {

  // Thunk middleware knows how to handle functions.
  // It passes the dispatch method as an argument to the function,
  // thus making it able to dispatch actions itself.

  return function (dispatch) {

    // First dispatch: the app state is updated to inform
    // that the API call is starting.

    dispatch(requestScores(user));

    // The function called by the thunk middleware can return a value,
    // that is passed on as the return value of the dispatch method.

    // In this case, we return a promise to wait for.
    // This is not required by thunk middleware, but it is convenient for us.
    var url = 'http://localhost:8888/api/v1.0/scores';
    return fetch(url)
      .then(response => response.json())
      .then(json =>

        // We can dispatch many times!
        // Here, we update the app state with the results of the API call.

        dispatch(receiveScores(user, json))
      );

      // In a real world app, you also want to
      // catch any error in the network call.
  }
}
