import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {View, StyleSheet, Text, TouchableOpacity} from 'react-native';
import {COLORS} from './Global';

export default class Footer extends Component {
  static propTypes = {
    navigation: PropTypes.object.isRequired,
  };
  constructor(props) {
    super(props);
  }

  onPressButton = () => {
    if (this.props.buttonText === 'Submission') {
      console.log('Navigate back to Report List');
      this.props.navigation.navigate('ReportList');
    } else if (this.props.buttonText === 'Continue') {
      console.log('Navigate back to Report List');
      this.props.navigation.navigate('ReportSubmission');
    }
  };

  render() {
    return (
      <View style={styles.footer}>
        <TouchableOpacity activeOpacity={0.5} onPress={this.onPressButton}>
          <View style={styles.button}>
            <Text style={styles.buttonText}>{this.props.buttonText}</Text>
          </View>
        </TouchableOpacity>
      </View>
    );
  }
}
const styles = StyleSheet.create({
  footer: {
    marginBottom: 0,
    position: 'relative',
  },
  button: {
    padding: 10,
    backgroundColor: COLORS.BUTTON_COLOR,
    borderColor: COLORS.WHITE,
    alignItems: 'center',
    borderRadius: 8,
  },
  buttonText: {
    color: COLORS.WHITE,
    fontSize: 16,
  },
});
