import React, {PureComponent} from 'react';
import {createStackNavigator} from '@react-navigation/stack';

import Connection from '../src/components/pages/connection/Connection';
import ReportList from '../src/components/pages/reportList/ReportList';
import ReportCreation from '../src/components/pages/reportCreation/ReportCreation';
import ReportSubmission from '../src/components/pages/reportSubmission/ReportSubmission';

const Stack = createStackNavigator();

export default class Navigator extends PureComponent {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <Stack.Navigator
        screenOptions={{headerShown: false}}
        initialRouteName="Connection">
        {this.props.userToken ? (
          <>
            <Stack.Screen name="ReportList">
              {props => <ReportList {...props} extraData={this.props} />}
            </Stack.Screen>
            <Stack.Screen name="ReportCreation">
              {props => <ReportCreation {...props} extraData={this.props} />}
            </Stack.Screen>
            <Stack.Screen name="ReportSubmission">
              {props => <ReportSubmission {...props} extraData={this.props} />}
            </Stack.Screen>
          </>
        ) : (
          <Stack.Screen name="Connection">
            {props => <Connection {...props} extraData={this.props} />}
          </Stack.Screen>
        )}
      </Stack.Navigator>
    );
  }
}