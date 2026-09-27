from pathlib import Path
import shutil

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
            keyPassword "havenmc-ci-store-password"
        }
    }
    buildTypes {''',
)
text = text.replace(
    '        release {\n            minifyEnabled false',
    '        release {\n            signingConfig signingConfigs.release\n            minifyEnabled false',
)
build.write_text(text)

# The Capacitor template ships with a generic adaptive icon. Replace it with
# density-specific HavenMC PNGs so the installed app shows the supplied brand.
res = Path('android/app/src/main/res')
for adaptive in ('mipmap-anydpi-v26/ic_launcher.xml', 'mipmap-anydpi-v26/ic_launcher_round.xml'):
    path = res / adaptive
    if path.exists():
        path.unlink()
for density in ('mdpi', 'hdpi', 'xhdpi', 'xxhdpi', 'xxxhdpi'):
    target = res / f'mipmap-{density}'
    target.mkdir(parents=True, exist_ok=True)
    icon = Path('android-icons') / f'ic_launcher_{density}.png'
    shutil.copyfile(icon, target / 'ic_launcher.png')
    shutil.copyfile(icon, target / 'ic_launcher_round.png')
manifest = Path('android/app/src/main/AndroidManifest.xml')
manifest_text = manifest.read_text().replace('android:roundIcon="@mipmap/ic_launcher_round"', 'android:roundIcon="@mipmap/ic_launcher"')
manifest.write_text(manifest_text)
print('Android Gradle configured: minSdk 24, arm64-v8a/armeabi-v7a, signed release, HavenMC launcher icons.')
