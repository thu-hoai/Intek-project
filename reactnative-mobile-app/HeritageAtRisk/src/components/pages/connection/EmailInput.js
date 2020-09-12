import React, {PureComponent} from 'react';
import PropTypes from 'prop-types';
import {TextInput, View, StyleSheet, Text} from 'react-native';
import {LOGINS, COLORS, ERROR_MESSAGES} from '../../common/Global';

export default class EmailInput extends PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      borderColor: '#8F2227',
    };
  }
  static propTypes = {
    emailInput: PropTypes.string.isRequired,
    onEmailChange: PropTypes.func.isRequired,
    emailText: PropTypes.string.isRequired,
    onEmailTextChange: PropTypes.func.isRequired,
  };

  // Email Input validation
  validateInput = text => {
    let regex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    return regex.test(text);
  };

  // Focus and Blur handling
  onFocus = () => this.setState({borderColor: '#208AD4'});
  onBlur = () => {
    this.setState({borderColor: '#8F2227'});
    if (this.validateInput(this.props.emailInput)) {
      this.props.onEmailTextChange('');
    } else {
      this.props.onEmailTextChange(ERROR_MESSAGES.INVALID_EMAIL);
    }
  };

  render() {
    const {emailInput, onEmailChange} = this.props;
    return (
      <View style={styles.container}>
        <TextInput
          style={{
            ...styles.inputFrame,
            borderColor: this.state.borderColor,
          }}
          value={emailInput}
          onChangeText={onEmailChange}
          placeholder={LOGINS.EMAIL}
          placeholderTextColor={COLORS.INITIAL_INPUT_TEXT}
          onFocus={this.onFocus}
          onBlur={this.onBlur}
        />
        <Text style={styles.invalidEmail}>{this.props.emailText}</Text>
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
    marginTop: 10,
    marginBottom: 5,
    padding: 10,
    borderRadius: 5,
    borderWidth: 1,
  },
  invalidEmail: {
    position: 'absolute',
    color: COLORS.WHITE,
    fontSize: 12,
    top: 50,
    left: 20,
  },
});
