import React, {PureComponent} from 'react';
import PropTypes from 'prop-types';
import {View, StyleSheet} from 'react-native';
import {COLORS} from '../../common/Global';
import Header from './../../common/Header';
import Footer from './../../common/Footer';

export default class ReportSubmission extends PureComponent {
  static propTypes = {
    navigation: PropTypes.object.isRequired,
    extraData: PropTypes.object.isRequired,
  };
  constructor(props) {
    super(props);
  }

  render() {
    const buttonText = 'Submission';
    return (
      <View style={styles.container}>
        <Header
          navigation={this.props.navigation}
          onUserTokenChange={this.props.extraData.onUserTokenChange}
        />
        <Footer navigation={this.props.navigation} buttonText={buttonText} />
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    // flex: 1,
    backgroundColor: COLORS.MAIN_RED,
    height: '100%',
    padding: 8,
  },
});
