import React, {PureComponent} from 'react';
import {View, StyleSheet, Image, TouchableOpacity, Alert} from 'react-native';
import {SMALL_LOGO_PATH_NAME} from './Global';
import {removeUserInfo, removeUserReportList} from './../../ApiCall';

export default class Logo extends PureComponent {
  constructor(props) {
    super(props);
  }

  onPressLogo = () => {
    Alert.alert('Log Out');
    removeUserInfo();
    removeUserReportList();
    console.log('Remove storages');
    this.props.onUserTokenChange('');
    console.log('Back to CONNECTION page');
  };
  render() {
    return (
      <View style={styles.header}>
        <TouchableOpacity onPress={() => this.onPressLogo()}>
          <Image style={styles.logo} source={SMALL_LOGO_PATH_NAME} />
        </TouchableOpacity>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  logo: {
    width: 24,
    height: 26,
    alignSelf: 'center',
  },
});
