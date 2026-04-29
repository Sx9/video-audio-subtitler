from pathlib import Path


class Sx9PathUtils:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()

    def ensure_output_folders(self) -> None:
        folders = [
            "output",
            "output/audio",
            "output/transcripts",
            "output/subtitles",
            "output/videos",
            "temp",
        ]

        for folder in folders:
            Path(folder).mkdir(parents=True, exist_ok=True)

    def get_stem(self, file_path: str) -> str:
        return Path(file_path).stem

    def audio_output_path(self, input_path: str) -> str:
        stem = self.get_stem(input_path)
        return str(Path("output/audio") / f"{stem}_audio.wav")

    def transcript_output_path(self, input_path: str) -> str:
        stem = self.get_stem(input_path)
        return str(Path("output/transcripts") / f"{stem}.txt")

    def vtt_output_path(self, input_path: str) -> str:
        stem = self.get_stem(input_path)
        return str(Path("output/subtitles") / f"{stem}.vtt")

    def base_video_output_path(self, input_path: str) -> str:
        stem = self.get_stem(input_path)
        return str(Path("output/videos") / f"{stem}_base.mp4")

    def final_video_output_path(self, input_path: str, subtitle_mode: str) -> str:
        stem = self.get_stem(input_path)
        safe_mode = subtitle_mode.lower().strip()
        return str(Path("output/videos") / f"{stem}_{safe_mode}_subtitles.mp4")

    def __repr__(self):
        return f"Sx9PathUtils(project_root='{self.project_root}')"
