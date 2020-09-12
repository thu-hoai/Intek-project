import React, {PureComponent} from 'react';
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  Image,
  Alert,
  TouchableOpacity,
} from 'react-native';
import PropTypes from 'prop-types';
import {COLORS, CAMERA_PATH_NAME} from '../../common/Global';
import {Icon} from 'react-native-elements';
import Logo from '../../common/Logo';
import {
  readUserReportList,
  deleteReportItem,
  readUserSession,
  storeUserReportList,
} from '../../../ApiCall';

export default class ReportList extends PureComponent {
  static propTypes = {
    extraData: PropTypes.object.isRequired,
    navigation: PropTypes.object.isRequired,
  };

  constructor(props) {
    super(props);
  }
  onPressCamera = () => {
    console.log('Navigate to REPORT CREATION');
    this.props.navigation.navigate('ReportCreation');
  };

  render() {
    return (
      <View style={styles.container}>
        <View style={styles.header}>
          <Logo onUserTokenChange={this.props.extraData.onUserTokenChange} />
          <Icon name={'view-headline'} type="material" color="white" />
        </View>

        <FlatList
          data={this.props.extraData.userReportList}
          keyExtractor={item => item.report_id}
          renderItem={({item, index}) => {
            return (
              <FlatListItems
                item={item}
                index={index}
                onUserReportListChange={
                  this.props.extraData.onUserReportListChange
                }
              />
            );
          }}
        />
        <View style={styles.cameraView}>
          <TouchableOpacity
            activeOpacity={0.5}
            onPress={() => this.onPressCamera()}>
            <Image source={CAMERA_PATH_NAME} />
          </TouchableOpacity>
        </View>
      </View>
    );
  }
}

class FlatListItems extends PureComponent {
  onPressTrashIcon = () => {
    readUserSession().then(userSession => {
      const authentication = userSession.session_id;
      deleteReportItem(authentication, this.props.item.report_id)
        .then(() => {
          readUserReportList().then(reportList => {
            reportList.splice(this.props.index, 1);
            this.props.onUserReportListChange(reportList);
            storeUserReportList(reportList);
          });
        })
        .catch(error => {
          console.log('Delete Error', error);
          Alert.alert(
            'Report Deletion Failure',
            'Our servers cannot process your request at this time. Please try again later.',
            [
              {
                text: 'OK',
                onPress: () => console.log('Fail'),
              },
            ],
          );
        });
    });
  };

  render() {
    return (
      <View
        // eslint-disable-next-line react-native/no-inline-styles
        style={{
          flex: 1,
          backgroundColor:
            this.props.index % 2 === 0 ? COLORS.DARK_RED : COLORS.LIGHT_RED,
        }}>
        <View style={styles.frameReport}>
          <View style={styles.frameInfo}>
            <Text style={styles.nameText}>{this.props.item.place_name}</Text>
            <View style={styles.frameLocationDate}>
              <View style={styles.locateArea}>
                <Icon
                  name={'location-on'}
                  type="material"
                  color="white"
                  size={12}
                />
                <Text style={styles.locateText}>
                  {this.props.item.designation}
                </Text>
              </View>
              <View style={styles.dateArea}>
                <Icon name={'clock'} type="evilicon" color="white" size={13} />
                <Text style={styles.dateText}>
                  {this.props.item.creation_time.slice(0, 10)}
                </Text>
              </View>
            </View>
          </View>
          <View style={styles.frameTools}>
            <Icon
              name={'md-trash'}
              type="ionicon"
              color="white"
              onPress={this.onPressTrashIcon}
            />
            <Icon name={'ios-cloud-done'} type="ionicon" color="white" />
          </View>
        </View>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.MAIN_RED,
    height: '100%',
  },
  header: {
    padding: 8,
    flexDirection: 'row',
    justifyContent: 'space-between',
    borderBottomColor: COLORS.RED_BORDER,
    borderBottomWidth: 1,
  },
  frameReport: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    height: 58,
  },
  frameInfo: {
    margin: 8,
  },
  frameLocationDate: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: 330,
  },
  dateArea: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  locateArea: {
    flexDirection: 'row',
    marginBottom: 0,
    alignItems: 'center',
  },
  frameTools: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    right: 8,
    width: 43,
  },

  nameText: {
    color: COLORS.WHITE,
    fontFamily: 'Roboto',
    fontSize: 14,
    fontWeight: 'bold',
  },
  locateText: {
    color: COLORS.WHITE,
    fontFamily: 'Roboto',
    fontSize: 12,
  },
  dateText: {
    color: COLORS.WHITE,
    fontFamily: 'Roboto',
    fontSize: 12,
    marginLeft: 2,
  },
  cameraView: {
    position: 'absolute',
    bottom: 13,
    right: 13,
  },
});
