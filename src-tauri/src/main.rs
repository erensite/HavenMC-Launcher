#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]
use std::{path::PathBuf, process::Command};
use tauri::api::path::app_data_dir;
use tauri::Config;

#[tauri::command]
fn launch_minecraft(version: String, loader: String, ram: u32, server: String, java_path: String, minecraft_dir: String) -> Result<String, String> {
    if version.trim().is_empty() || server.trim().is_empty() { return Err("Sürüm ve sunucu adresi zorunludur".into()); }
    let dir = if minecraft_dir.trim().is_empty() { std::env::var("APPDATA").map(|p| PathBuf::from(p).join(".minecraft")).unwrap_or_else(|_| PathBuf::from(".minecraft")) } else { PathBuf::from(minecraft_dir) };
    let java = if java_path.trim().is_empty() { "java" } else { java_path.trim() };
    // Native hook: once the profile has a downloaded classpath/jar, this command launches it.
    // Keeping the command here makes the UI functional without shelling out from JavaScript.
    let marker = dir.join("versions").join(&version).join(format!("{}.jar", version));
    if !marker.exists() { return Err(format!("Minecraft {} henüz indirilmemiş. İndirme motorunu etkinleştirmek için profil klasörüne oyun dosyalarını ekleyin.", version)); }
    let mut cmd = Command::new(java);
    cmd.current_dir(&dir).arg(format!("-Xmx{}M", ram)).arg("-jar").arg(marker).arg("--server").arg(server).arg("--loader").arg(loader);
    cmd.spawn().map(|_| "Minecraft başlatma işlemi gönderildi".into()).map_err(|e| format!("Java başlatılamadı: {}", e))
}

#[tauri::command]
fn app_data_path(config: Config) -> Result<String, String> { app_data_dir(&config).map(|p| p.to_string_lossy().into_owned()).ok_or_else(|| "Uygulama klasörü bulunamadı".into()) }

fn main() { tauri::Builder::default().invoke_handler(tauri::generate_handler![launch_minecraft, app_data_path]).run(tauri::generate_context!()).expect("error while running HavenMC Launcher"); }
