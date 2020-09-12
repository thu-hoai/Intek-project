'use strict';
import React, {PureComponent} from 'react';
import {StyleSheet, TouchableOpacity, View} from 'react-native';
import {RNCamera} from 'react-native-camera';
import {Icon} from 'react-native-elements';

class Camera extends PureComponent {
  render() {
    return (
      <View style={styles.container}>
        <RNCamera
          ref={ref => {
            this.camera = ref;
          }}
          style={styles.preview}
          type={RNCamera.Constants.Type.back}
          flashMode={RNCamera.Constants.FlashMode.on}
          androidCameraPermissionOptions={{
            title: 'Permission to use camera',
            message: 'We need your permission to use your camera',
            buttonPositive: 'Ok',
            buttonNegative: 'Cancel',
          }}
          captureAudio={false}
        />

        <View style={styles.capture}>
          <TouchableOpacity
            onPress={this.takePicture.bind(this)}
            style={styles.capture}>
            <Icon name={'circle'} type="font-awesome" color="white" size={48} />
          </TouchableOpacity>
        </View>
      </View>
    );
  }

  onUpdateList = (photos, str) => {
    let jsonString = {};
    jsonString.photoUrl = str;
    photos.push(jsonString);
    return photos;
  };

  takePicture = async () => {
    if (this.camera) {
      const options = {quality: 0.5, base64: true};
      const data = await this.camera.takePictureAsync(options);
      this.props.onPhotoListChange({photoUrl: data.uri});
    }
  };
}

const styles = StyleSheet.create({
  container: {
    flex: 4,
    flexDirection: 'column',
  },
  preview: {
    flex: 1,
    justifyContent: 'flex-end',
    alignItems: 'center',
    overflow: 'hidden',
  },
  capture: {
    position: 'absolute',
    bottom: 16,
    alignItems: 'center',
    width: '100%',
  },
});

export default Camera;
