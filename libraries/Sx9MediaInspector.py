from pathlib import Path

from PIL import Image


class Sx9MediaInspector:
    AUDIO_EXTENSIONS = {
        ".mp3",
        ".wav",
        ".m4a",
        ".aac",
        ".flac",
        ".ogg",
        ".wma",
    }

    VIDEO_EXTENSIONS = {
        ".mp4",
        ".mov",
        ".mkv",
        ".avi",
        ".webm",
        ".m4v",
    }

    IMAGE_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".bmp",
    }

    def get_media_type(self, path: str) -> str:
        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        extension = file_path.suffix.lower()

        if extension in self.AUDIO_EXTENSIONS:
            return "audio"

        if extension in self.VIDEO_EXTENSIONS:
            return "video"

        raise ValueError(f"Unsupported media file type: {extension}")

    def validate_image(self, path: str) -> None:
        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(f"Image file not found: {path}")

        if file_path.suffix.lower() not in self.IMAGE_EXTENSIONS:
            raise ValueError(f"Unsupported image file type: {file_path.suffix}")

        with Image.open(file_path) as image:
            width, height = image.size

        if width <= 0 or height <= 0:
            raise ValueError("Image dimensions are invalid.")

    def is_roughly_16x9(self, path: str, tolerance: float = 0.05) -> bool:
        with Image.open(path) as image:
            width, height = image.size

        ratio = width / height
        expected = 16 / 9

        return abs(ratio - expected) <= tolerance

    def __repr__(self):
        return f"Sx9MediaInspector()"