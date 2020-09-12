import AsyncStorage from '@react-native-community/async-storage';
import {API} from '../src/components/common/Global';
import {Alert, PermissionsAndroid} from 'react-native';

// Storing object value User Login
export const storeUserLogin = async loginUserInfo => {
  try {
    const jsonValue = JSON.stringify(loginUserInfo);
    await AsyncStorage.setItem('@userLogin', jsonValue);
  } catch (error) {
    console.log(error.message);
  }
  console.log('Login session added');
};

// Reading object value User Login
export const readUserSession = async () => {
  try {
    const jsonValue = await AsyncStorage.getItem('@userLogin');
    return jsonValue != null ? JSON.parse(jsonValue) : null;
  } catch (error) {
    console.log(error.message);
  }
};

// Removes item for a key
export const removeUserInfo = async () => {
  try {
    await AsyncStorage.removeItem('@userLogin');
  } catch (error) {
    console.log(error.message);
  }
  console.log('Removed login session');
};

// Get the user session
export async function getUserSessions(email, password) {
  try {
    let response = await fetch('https://api.heobs.org/account/session', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        'X-API-Key': API.API_KEY,
      },
      body: JSON.stringify({
        type: 'JSON',
        email_address: email,
        password: password,
      }),
    });
    let responseJson = await response.json();
    return responseJson;
  } catch (error) {
    console.log(error);
  }
}

/////////////////////////////////////////////////////////////////////////
// '54c571c1-9dac-11ea-9e35-0007cb040bcc'
// Fetch the list of reports submitted by the user
export async function getUserReportList(authentication) {
  const url = 'https://api.heobs.org/har/report';
  try {
    let response = await fetch(url, {
      method: 'GET',
      headers: {
        'X-API-Key': API.API_KEY,
        'X-Authentication': authentication,
      },
    });
    let json = await response.json();
    return json;
  } catch (error) {
    console.error(error);
  }
}

// Storing object value User Report List
export const storeUserReportList = async UserReportList => {
  try {
    const jsonValue = JSON.stringify(UserReportList);
    await AsyncStorage.setItem('@userReportList', jsonValue);
  } catch (error) {
    console.log(error.message);
  }
  console.log('Report List Storages Successful');
};

// Reading object value User Login
export const readUserReportList = async () => {
  try {
    const jsonValue = await AsyncStorage.getItem('@userReportList');
    return jsonValue != null ? JSON.parse(jsonValue) : null;
  } catch (error) {
    console.log(error.message);
  }
};

export const removeUserReportList = async () => {
  try {
    await AsyncStorage.removeItem('@userReportList');
  } catch (error) {
    console.log(error.message);
  }
  console.log('Removed User Report List');
};

// Delete the report list
export async function deleteReportItem(authentication, report_id) {
  try {
    let url = 'https://api.heobs.org/har/report/'.concat(report_id);
    console.log(url);
    await fetch(url, {
      method: 'DELETE',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        'X-API-Key': API.API_KEY,
        'X-Authentication': authentication,
      },
    });
    console.log(report_id, 'Delete Successfully');
  } catch (error) {
    throw error;
  }
}

export const requestLocationPermission = async () => {
  try {
    const granted = await PermissionsAndroid.request(
      PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
      {
        title: 'Location Permission',
        message: 'Give the granted Location permission',
        buttonNeutral: 'Ask Me Later',
        buttonNegative: 'Cancel',
        buttonPositive: 'OK',
      },
    );
    if (granted === PermissionsAndroid.RESULTS.GRANTED) {
      console.log('Location Granted');
    } else {
      console.log('Location permission denied');
    }
  } catch (err) {
    console.warn(err);
  }
};
