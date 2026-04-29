$ffmpegBin = "C:\Users\sandi\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin"
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")

if ([string]::IsNullOrWhiteSpace($userPath)) {
    [Environment]::SetEnvironmentVariable("Path", $ffmpegBin, "User")
}
elseif ($userPath -notlike "*$ffmpegBin*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$ffmpegBin", "User")
}
