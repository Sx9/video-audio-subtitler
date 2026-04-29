import subprocess
from pathlib import Path


class Sx9FFmpeg:
    def __init__(self, ffmpeg_command: str = "ffmpeg", ffprobe_command: str = "ffprobe"):
        self.ffmpeg_command = ffmpeg_command
        self.ffprobe_command = ffprobe_command

    def check_available(self) -> None:
        self._run_command([self.ffmpeg_command, "-version"])
        self._run_command([self.ffprobe_command, "-version"])

    def extract_audio_from_video(self, video_path: str, output_audio_path: str) -> str:
        Path(output_audio_path).parent.mkdir(parents=True, exist_ok=True)

        command = [
            self.ffmpeg_command,
            "-y",
            "-i",
            video_path,
            "-vn",
            "-acodec",
            "pcm_s16le",
            "-ar",
            "16000",
            "-ac",
            "1",
            output_audio_path,
        ]

        self._run_command(command)
        return output_audio_path

    def normalize_audio_for_whisper(self, audio_path: str, output_audio_path: str) -> str:
        Path(output_audio_path).parent.mkdir(parents=True, exist_ok=True)

        command = [
            self.ffmpeg_command,
            "-y",
            "-i",
            audio_path,
            "-acodec",
            "pcm_s16le",
            "-ar",
            "16000",
            "-ac",
            "1",
            output_audio_path,
        ]

        self._run_command(command)
        return output_audio_path

    def create_video_from_image_and_audio(
        self,
        image_path: str,
        audio_path: str,
        output_video_path: str,
    ) -> str:
        Path(output_video_path).parent.mkdir(parents=True, exist_ok=True)

        video_filter = (
            "scale=1920:1080:force_original_aspect_ratio=decrease,"
            "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,"
            "format=yuv420p"
        )

        command = [
            self.ffmpeg_command,
            "-y",
            "-loop",
            "1",
            "-i",
            image_path,
            "-i",
            audio_path,
            "-vf",
            video_filter,
            "-c:v",
            "libx264",
            "-tune",
            "stillimage",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            output_video_path,
        ]

        self._run_command(command)
        return output_video_path

    def burn_subtitles(
        self,
        input_video_path: str,
        vtt_path: str,
        output_video_path: str,
        subtitle_force_style: str | None = None,
    ) -> str:
        Path(output_video_path).parent.mkdir(parents=True, exist_ok=True)

        escaped_vtt_path = self._escape_subtitle_path_for_ffmpeg(vtt_path)

        subtitle_filter = f"subtitles='{escaped_vtt_path}'"

        if subtitle_force_style:
            escaped_style = self._escape_subtitle_style_for_ffmpeg(subtitle_force_style)
            subtitle_filter = f"{subtitle_filter}:force_style='{escaped_style}'"

        command = [
            self.ffmpeg_command,
            "-y",
            "-i",
            input_video_path,
            "-vf",
            subtitle_filter,
            "-c:a",
            "copy",
            output_video_path,
        ]

        self._run_command(command)
        return output_video_path

    def embed_subtitles(
        self,
        input_video_path: str,
        vtt_path: str,
        output_video_path: str,
    ) -> str:
        Path(output_video_path).parent.mkdir(parents=True, exist_ok=True)

        command = [
            self.ffmpeg_command,
            "-y",
            "-i",
            input_video_path,
            "-i",
            vtt_path,
            "-c:v",
            "copy",
            "-c:a",
            "copy",
            "-c:s",
            "mov_text",
            "-metadata:s:s:0",
            "language=eng",
            output_video_path,
        ]

        self._run_command(command)
        return output_video_path

    def _run_command(self, command: list[str]) -> None:
        print()
        print("Running command:")
        print(" ".join(command))
        print()

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=False,
        )

        if result.returncode != 0:
            print("STDOUT:")
            print(result.stdout)
            print("STDERR:")
            print(result.stderr)
            raise RuntimeError(f"Command failed with exit code {result.returncode}")

    def _escape_subtitle_path_for_ffmpeg(self, path: str) -> str:
        resolved_path = str(Path(path).resolve())
        return resolved_path.replace("\\", "/").replace(":", "\\:")

    def __repr__(self):
        return f"Sx9FFmpeg(ffmpeg_command='{self.ffmpeg_command}')"
