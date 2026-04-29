from dataclasses import dataclass
from typing import Optional


@dataclass
class Sx9SubtitlingJob:
    input_path: str
    media_type: str
    subtitle_mode: str
    background_image_path: Optional[str] = None
    whisper_model_size: str = "base"

    def __repr__(self):
        return f"Sx9SubtitlingJob(input_path='{self.input_path}', media_type='{self.media_type}', subtitle_mode='{self.subtitle_mode}', background_image_path='{self.background_image_path}', whisper_model_size='{self.whisper_model_size}')"
