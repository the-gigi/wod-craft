/* Combine all available reducers to a single root reducer.
 *
 * CAUTION: When using the generators, this file is modified in some places.
 *          This is done via AST traversal - Some of your formatting may be lost
 *          in the process - no functionality should be broken though.
 *          This modifications only run once when the generator is invoked - if
 *          you edit them, they are not updated again.
 */


import { combineReducers } from 'redux'
import {
    REQUEST_SCORES,
    RECEIVE_SCORES
} from '../actions/actions'


function scores(state = {
    isFetching: false,
    items: []
}, action) {
    switch (action.type) {
        case REQUEST_SCORES:
            return Object.assign({}, state, {
                isFetching: true
            });
        case RECEIVE_SCORES:
            console.log('Yay! received scores');
            return Object.assign({}, state, {
                isFetching: false,
                items: action.scores
            });
        default:
            return state
    }
}

const rootReducer = combineReducers({
    scores
});

export default rootReducer
