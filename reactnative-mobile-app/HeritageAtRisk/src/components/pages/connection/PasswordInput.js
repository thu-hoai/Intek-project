import React, {PureComponent} from 'react';
import PropTypes from 'prop-types';
import {TextInput, View, StyleSheet, Text, Linking} from 'react-native';
import {Icon} from 'react-native-elements';
import {LOGINS, COLORS} from '../../common/Global';

export default class PasswordInput extends PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      borderColor: COLORS.RED_BORDER,
      isShowedPassword: true,
    };
  }

  static propTypes = {
    passwordInput: PropTypes.string.isRequired,
    onPasswordChange: PropTypes.func.isRequired,
    passText: PropTypes.string.isRequired,
    onPassTextChange: PropTypes.func.isRequired,
  };

  onFocusPass = () => this.setState({borderColor: COLORS.BLUE_BORDER});
  onBlurPass = () => this.setState({borderColor: COLORS.RED_BORDER});

  showPass = () => {
    const newState = !this.state.isShowedPassword;
    this.setState({
      isShowedPassword: newState,
    });
  };

  render() {
    const {passwordInput, onPasswordChange} = this.props;
    return (
      <View style={styles.container}>
        <View style={styles.container}>
          <TextInput // Password Input
            style={{
              ...styles.inputFrame,
              borderColor: this.state.borderColor,
            }}
            value={passwordInput}
            placeholder={LOGINS.PASSWORD}
            placeholderTextColor={COLORS.INITIAL_INPUT_TEXT}
            onChangeText={onPasswordChange}
            secureTextEntry={this.state.isShowedPassword}
            onFocus={this.onFocusPass}
            onBlur={this.onBlurPass}
          />
          <View style={styles.eyeFlash}>
            <Icon
              name={this.state.isShowedPassword ? 'md-eye-off' : 'md-eye'}
              type="ionicon"
              color="gray"
              onPress={this.showPass}
            />
          </View>
        </View>
        <Text style={styles.invalidPass}>{this.props.passText}</Text>
        <Text // Forgot Password
          style={styles.forgotPassword}
          onPress={() => Linking.openURL(LOGINS.URL)}>
          {LOGINS.FORGOT_PASSWORD}
        </Text>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    position: 'relative',
  },
  inputFrame: {
    position: 'relative',
    height: 40,
    backgroundColor: COLORS.WHITE,
    color: COLORS.BLACK,
    marginLeft: 10,
    marginRight: 10,
    marginBottom: 5,
    padding: 10,
    borderRadius: 5,
    borderWidth: 2,
  },

  eyeFlash: {
    position: 'absolute',
    right: 20,
    top: '20%',
  },
  forgotPassword: {
    position: 'absolute',
    color: COLORS.WHITE,
    top: 40,
    right: 20,
    fontSize: 12,
  },
  invalidPass: {
    position: 'absolute',
    color: COLORS.WHITE,
    fontSize: 12,
    top: 40,
    left: 20,
  },
});
