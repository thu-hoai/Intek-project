import React, {PureComponent} from 'react';
import PropTypes from 'prop-types';
import {View, StyleSheet, Text, TouchableOpacity} from 'react-native';
import {LOGINS, ERROR_MESSAGES} from '../../common/Global';
import PasswordInput from './PasswordInput';
import EmailInput from './EmailInput';
import {
  storeUserLogin,
  getUserSessions,
  getUserReportList,
  storeUserReportList,
} from '../../../ApiCall';

export default class LoginForm extends PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      emailText: '',
      passText: '',
    };
  }
  static propTypes = {
    passwordInput: PropTypes.string.isRequired,
    onPasswordChange: PropTypes.func.isRequired,
    emailInput: PropTypes.string.isRequired,
    onEmailChange: PropTypes.func.isRequired,
    navigation: PropTypes.object.isRequired,
  };
  // Change email text to a wanning message
  onChangeEmailText = message => {
    this.setState({emailText: message});
  };
  // Change the given password text to a wanning message
  onChangePassText = message => {
    this.setState({passText: message});
  };
  validateInput = text => {
    let regex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    console.log(regex.test(text));
    return regex.test(text);
  };
  // Define action when press CONNECT button
  onPressButton = () => {
    if (this.props.passwordInput) {
      this.setState({passText: ''});
    } else {
      this.setState({passText: ERROR_MESSAGES.EMPTY_MESSAGE});
    }
    if (this.props.emailInput) {
      this.setState({emailText: ''});
    } else {
      this.setState({emailText: ERROR_MESSAGES.EMPTY_MESSAGE});
    }
    if (this.props.passwordInput && this.props.emailInput) {
      if (!this.validateInput(this.props.emailInput)) {
        this.setState({emailText: ERROR_MESSAGES.INVALID_EMAIL});
      }
      getUserSessions(this.props.emailInput, this.props.passwordInput).then(
        userSession => {
          if (userSession.error) {
            console.log('An error occurred', userSession.error);
            this.setState({passText: ERROR_MESSAGES.WRONG_PASSWORD});
          } else {
            console.log('Successful Login');
            storeUserLogin(userSession);
            this.props.onUserTokenChange(userSession);
            getUserReportList(userSession.session_id).then(userReportList => {
              if (userReportList.error) {
                console.log('An error occurred', userReportList.error);
              } else {
                const ReportList = userReportList.map(userReport => {
                  return {...userReport, isTransmitted: true};
                });
                let result = [];
                for (let obj of ReportList) {
                  if (obj.object_status !== 'deleted') {
                    result.push(obj);
                  }
                }
                this.props.onUserReportListChange(result);
                storeUserReportList(result);
              }
            });
            console.log('Navigate to REPORT LIST page');
          }
        },
      );
    }
  };

  render() {
    const {
      emailInput,
      onEmailChange,
      passwordInput,
      onPasswordChange,
    } = this.props;
    return (
      <View style={styles.loginForm}>
        <EmailInput
          emailInput={emailInput}
          onEmailChange={onEmailChange}
          emailText={this.state.emailText}
          onEmailTextChange={this.onChangeEmailText}
        />
        <Text>{this.state.EmptyText}</Text>

        <PasswordInput
          passwordInput={passwordInput}
          onPasswordChange={onPasswordChange}
          passText={this.state.passText}
          onPassTextChange={this.onChangePassText}
        />

        <TouchableOpacity // Button Connect
          style={styles.connectButton}
          activeOpacity={0.5}
          onPress={this.onPressButton}>
          <Text style={styles.buttonText}>Connect</Text>
        </TouchableOpacity>
        <Text style={styles.haveAccountText}>{LOGINS.HAVE_ACCOUNT_TEXT}</Text>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  loginForm: {
    width: '100%',
  },

  connectButton: {
    margin: 10,
    marginTop: 15,
    borderRadius: 5,
    padding: 10,
    backgroundColor: '#208AD4',
    borderColor: '#fff',
  },

  haveAccountText: {
    textAlign: 'center',
    fontSize: 13,
    color: '#fff',
    fontFamily: 'Roboto',
    marginBottom: 10,
  },

  buttonText: {
    color: '#fff',
    textAlign: 'center',
    fontWeight: 'bold',
  },
});
