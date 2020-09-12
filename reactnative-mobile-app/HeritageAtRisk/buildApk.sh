#/user/bin/env bash

BASEDIR=$PWD
APK_FILE_PATH="android/app/build/outputs/apk/debug/app-debug.apk"
# Build android
react-native bundle \
  --platform android \
  --dev false \
  --entry-file index.js \
  --bundle-output android/app/src/main/assets/index.android.bundle \
  --assets-dest android/app/src/main/res &&
./android/./gradlew -p ./android  assembleDebug;

# Remove build file
rm "$BASEDIR/android/app/src/main/assets/index.android.bundle";
rm "$BASEDIR/android/app/src/main/res/drawable-hdpi"/*;
rm "$BASEDIR/android/app/src/main/res/drawable-mdpi"/*;
rm "$BASEDIR/android/app/src/main/res/drawable-xhdpi"/*;
rm "$BASEDIR/android/app/src/main/res/drawable-xxhdpi"/*;
rm "$BASEDIR/android/app/src/main/res/drawable-xxxhdpi"/*;
rm "$BASEDIR/android/app/src/main/res/raw/app.json";

# your_project-> android-> app-> build-> outputs-> apk-> debug-> app-debug.apk
mv "$BASEDIR/$APK_FILE_PATH" .
# adb install "$BASEDIR/$APK_FILE_PATH" && rm "$BASEDIR/$APK_FILE_PATH";