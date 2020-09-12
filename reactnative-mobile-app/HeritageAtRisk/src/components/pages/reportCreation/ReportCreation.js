import React, {PureComponent} from 'react';
import PropTypes from 'prop-types';
import {
  View,
  StyleSheet,
  FlatList,
  Image,
  TouchableOpacity,
  Text,
} from 'react-native';
import Geolocation from 'react-native-geolocation-service';
import {Icon} from 'react-native-elements';
import {COLORS} from '../../common/Global';
import Header from './../../common/Header';
import Footer from './../../common/Footer';
import Camera from './Camera';
import Map from './Map';
import {requestLocationPermission} from './../../../ApiCall';

export default class ReportCreation extends PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      photosList: [],
      position: {latitude: 0, longitude: 0},
    };
  }
  static propTypes = {
    navigation: PropTypes.object.isRequired,
    extraData: PropTypes.object.isRequired,
  };

  onPhotoListChange = photo => {
    this.setState(previousState => {
      let photoList = previousState.photosList;
      return {
        photosList: [...photoList, photo],
      };
    });
  };

  onPositionChangeSuccess = position => {
    this.setState({
      position: {
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
      },
    });
  };

  componentDidMount = () => {
    requestLocationPermission();
    Geolocation.getCurrentPosition(
      this.onPositionChangeSuccess,
      error => {
        console.log(error);
      },
      {enableHighAccuracy: true, timeout: 15000, maximumAge: 10000},
    );
    this.watchID = Geolocation.watchPosition(
      this.onPositionChangeSuccess,
      error => {
        console.log(error);
      },
      {enableHighAccuracy: true, timeout: 15000, maximumAge: 10000},
    );
  };

  componentWillUnmount = () => {
    Geolocation.clearWatch(this.watchID);
  };

  render() {
    const buttonText = 'Continue';
    return (
      <View style={styles.container}>
        <Header
          navigation={this.props.navigation}
          onUserTokenChange={this.props.extraData.onUserTokenChange}
        />
        <View style={styles.flexContainer}>
          <Camera
            style={styles.frameCamera}
            photosList={this.state.photosList}
            onPhotoListChange={this.onPhotoListChange}
          />
          <View style={styles.framePhoto}>
            <FlatList
              data={this.state.photosList}
              keyExtractor={item => item.photoUrl}
              horizontal={true}
              ListEmptyComponent={
                <>
                  <View style={styles.photoPlaceholder}>
                    <Icon
                      name={'camera'}
                      type="font-awesome"
                      color="#8F2227"
                      size={40}
                    />
                  </View>
                </>
              }
              renderItem={({item, index}) => (
                <TouchableOpacity>
                  <View style={styles.photoContainer}>
                    <Text style={styles.removeImage}>x</Text>
                    <Image
                      style={styles.photoQueue}
                      source={{uri: item.photoUrl}}
                    />
                  </View>
                </TouchableOpacity>
              )}
            />
          </View>
          <View style={styles.frameMap}>
            <Map position={this.state.position} />
          </View>
        </View>
        <Footer navigation={this.props.navigation} buttonText={buttonText} />
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.MAIN_RED,
    height: '100%',
    padding: 8,
  },
  flexContainer: {
    flex: 1,
  },

  frameCamera: {
    flex: 4,
  },
  framePhoto: {
    flex: 1,
    position: 'relative',
  },
  frameMap: {
    flex: 1,
    backgroundColor: 'pink',
  },
  photoPlaceholder: {
    flex: 1,
    borderWidth: 1,
    borderColor: '#8F2227',
    borderRadius: 4,
    width: 80,
    paddingBottom: 20,
    paddingTop: 20,
    marginBottom: 2,
    marginTop: 2,
  },
  photoQueue: {
    height: 88,
    width: 80,
  },
  photoContainer: {
    margin: 2,
    backgroundColor: 'black',
  },
  removeImage: {
    position: 'absolute',
    right: 0,
    top: 0,
    color: 'white',
    fontSize: 28,
  },
});
