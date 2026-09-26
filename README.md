# HavenMC Launcher

HavenMC için **Windows EXE ve Android APK** üreten açık kaynak, ortak web-kod tabanlı launcher. Varsayılan sunucu: `havenmc.mangoohost.live`.

## Özellikler

- Mojang version manifestinden 1.17+ sürüm listesi: release, snapshot, beta ve alpha türleri
- Vanilla, Fabric, Forge ve NeoForge profil seçimi
- Profil oluşturma, seçme ve silme; sürüm, loader ve RAM ayarlarını profile kaydetme
- Modrinth API ile mod arama ve profile ekleme; CurseForge API anahtarı alanı
- Türkçe/English, Java yolu, Minecraft klasörü, RAM ve otomatik sunucu bağlantısı ayarları
- Veriler tarayıcı/uygulama localStorage'ında tutulur; API anahtarları depoya yazılmaz
- Tauri masaüstü kabuğu ve Capacitor Android kabuğu ile ortak `src/` kodu

## Geliştirme

```bash
npm install
# Web arayüzünü statik olarak src/index.html ile açabilir veya
npx tauri dev
```

Android için Android Studio/SDK gerekir:

```bash
npx cap add android
npx cap sync android
npx cap open android
```

## GitHub Actions

- Her `v*` etiketi Windows ve Android build'lerini çalıştırır.
- `HavenMC-Launcher-Windows` artifact'i içinde `HavenMC-Launcher.exe` kurulumu bulunur.
- `HavenMC-Launcher-Android` artifact'i içinde `HavenMC-Launcher.apk` (unsigned release APK) bulunur.
- Tag build'i GitHub Release oluşturur: `git tag v1.1.0 && git push origin v1.1.0`.
- `workflow_dispatch` ile de iki platform build'i başlatılabilir.

## Windows 7 notu

Tauri NSIS bundle WebView2 bootstrapper ile yapılandırılmıştır. Windows 7'de WebView2 kurulumu için internet ve TLS 1.2 gerekir. Windows 10/11'de WebView2 genellikle hazırdır.

## Açık kaynak / gerçek oyun motoru sınırı

Bu repository launcher UI'sı, sürüm/mod keşfi, profil ve native başlatma köprüsünü sağlar. Mojang hesabı/Microsoft OAuth, asset/library indirme, sürüm manifestindeki download URL'lerinden güvenli indirme ve Fabric/Forge installer zinciri lisans/dağıtım koşulları nedeniyle ayrı bir backend veya resmi launcher hesap akışı gerektirir. Native Tauri komutu, oyun jar'ı profile indirildiğinde Java ile çalıştırmayı dener; dosya yoksa kullanıcıya açık hata verir. Android'de Java Minecraft çalıştırma, cihazdaki JVM/oyun motoruna bağlı platform-native bir eklenti gerektirir.

## Lisans

MIT — üçüncü taraf Minecraft, Modrinth ve CurseForge markaları sahiplerine aittir.
