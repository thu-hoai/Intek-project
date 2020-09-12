import React, {PureComponent} from 'react';
import PropTypes from 'prop-types';
import {View, StyleSheet, Text, TouchableOpacity} from 'react-native';
import {COLORS} from './Global';
import Logo from './Logo';

export default class Header extends PureComponent {
  constructor(props) {
    super(props);
  }
  static propTypes = {
    navigation: PropTypes.object.isRequired,
  };

  onPressCancelButton = () => {
    console.log('Navigate back to Report List');
    this.props.navigation.navigate('ReportList');
  };

  render() {
    return (
      <View style={styles.header}>
        <Logo
          navigation={this.props.navigation}
          onUserTokenChange={this.props.onUserTokenChange}
        />
        <TouchableOpacity
          activeOpacity={0.5}
          onPress={this.onPressCancelButton}>
          <View style={styles.button}>
            <Text style={styles.buttonText}>Cancel</Text>
          </View>
        </TouchableOpacity>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  header: {
    padding: 8,
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  button: {
    padding: 7,
    backgroundColor: COLORS.BUTTON_COLOR,
    borderColor: COLORS.WHITE,
    borderRadius: 3,
  },
  buttonText: {
    color: COLORS.WHITE,
    fontSize: 12,
  },
});
