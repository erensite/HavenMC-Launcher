from pathlib import Path

variables = Path('android/variables.gradle')
text = variables.read_text()
text = text.replace('minSdkVersion = 22', 'minSdkVersion = 24')
variables.write_text(text)

build = Path('android/app/build.gradle')
text = build.read_text()
text = text.replace(
    'targetSdkVersion rootProject.ext.targetSdkVersion\n',
    "targetSdkVersion rootProject.ext.targetSdkVersion\n        ndk { abiFilters 'arm64-v8a', 'armeabi-v7a' }\n",
)
text = text.replace(
    '    buildTypes {',
    '''    signingConfigs {
        release {
            storeFile file("../havenmc-ci-release.keystore")
            storePassword "havenmc-ci-store-password"
            keyAlias "havenmc"
            keyPassword "havenmc-ci-key-password"
        }
    }
    buildTypes {''',
)
text = text.replace(
    '        release {\n            minifyEnabled false',
    '        release {\n            signingConfig signingConfigs.release\n            minifyEnabled false',
)
build.write_text(text)
print('Android Gradle configured: minSdk 24, arm64-v8a/armeabi-v7a, signed release.')
