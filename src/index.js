import React from 'react'
import ReactDOM from 'react-dom'
import './index.css'
import App from './components/App'
import registerServiceWorker from './registerServiceWorker'

ReactDOM.render(<App/>, document.getElementById('root'))
registerServiceWorker()

if (module.hot) {
  // hot reloading (but state reset)
  module.hot.accept()
}
