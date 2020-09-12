import React, {PureComponent} from 'react';
import {View, StyleSheet, Image, KeyboardAvoidingView} from 'react-native';
import {LOGO_PATH_NAME} from '../../common/Global';
import LoginForm from './LoginForm';
import PropTypes from 'prop-types';

export default class Connection extends PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      email: 'Invalid',
    };
  }
  static propTypes = {
    extraData: PropTypes.object.isRequired,
    navigation: PropTypes.object.isRequired,
  };

  render() {
    const {
      emailInput,
      onEmailChange,
      passwordInput,
      onPasswordChange,
      onUserTokenChange,
      userReportList,
      onUserReportListChange,
    } = this.props.extraData;
    return (
      <View style={styles.container}>
        <KeyboardAvoidingView behavior="padding" style={styles.home}>
          <Image style={styles.logo} source={LOGO_PATH_NAME} />
          <LoginForm
            emailInput={emailInput}
            onEmailChange={onEmailChange}
            passwordInput={passwordInput}
            onPasswordChange={onPasswordChange}
            onUserTokenChange={onUserTokenChange}
            userReportList={userReportList}
            onUserReportListChange={onUserReportListChange}
            navigation={this.props.navigation}
          />
        </KeyboardAvoidingView>
      </View>
    );
  }
}
//

const styles = StyleSheet.create({
  container: {
    height: '100%',
    alignItems: 'center',
    backgroundColor: '#DC3C44',
  },
  home: {
    paddingLeft: 20,
    paddingRight: 20,
    width: '100%',
  },

  logo: {
    width: 162,
    height: 176,
    alignSelf: 'center',
  },
});
