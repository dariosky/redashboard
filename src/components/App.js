import React, {Component} from 'react'
import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import {faSpinner} from '@fortawesome/fontawesome-free-solid'
import injectSheet from 'react-jss'

const styles = {
  header: {
    fontSize: '18pt',
  },
  logo: {
    width: "3em",
    verticalAlign: 'middle',
  },
  h1: {
    display: "inline-block",
    verticalAlign: 'middle',
  },
}

class App extends Component {
  render() {
    const {classes} = this.props
    return (
      <div className="App">
        <header className={classes.header}>
          <h1 className={classes.h1}>Reactive Real-Time Dashboard</h1>
          <FontAwesomeIcon className={classes.logo} icon={faSpinner} spin size="2x"/>
        </header>
        <p className="content">
          The content will arrive here
        </p>
      </div>
    )
  }
}

export default injectSheet(styles)(App)
