import React, {PureComponent} from 'react';
import {readUserSession, removeUserReportList} from './src/ApiCall';
import {NavigationContainer} from '@react-navigation/native';
import Navigator from './src/Navigation';

class App extends PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      emailInput: '',
      passwordInput: '',
      userToken: null,
      userReportList: [],
    };
  }
  onEmailChange = email => {
    this.setState({emailInput: email});
  };

  onPasswordChange = password => {
    this.setState({passwordInput: password});
  };
  onUserTokenChange = object => {
    this.setState({userToken: object});
  };
  onUserReportListChange = list => {
    this.setState({userReportList: list});
  };

  componentDidMount = async () => {
    const userToken = await readUserSession();
    this.setState({userToken: userToken});
    // removeUserReportList();
  };

  render() {
    return (
      <NavigationContainer>
        <Navigator
          emailInput={this.state.emailInput}
          onEmailChange={this.onEmailChange}
          passwordInput={this.state.passwordInput}
          onPasswordChange={this.onPasswordChange}
          userToken={this.state.userToken}
          onUserTokenChange={this.onUserTokenChange}
          onUserReportListChange={this.onUserReportListChange}
          userReportList={this.state.userReportList}
        />
      </NavigationContainer>
    );
  }
}

export default App;
