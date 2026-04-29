from libraries.Sx9FFmpeg import Sx9FFmpeg


class Sx9SubtitleRenderer:
    def __init__(self, ffmpeg: Sx9FFmpeg):
        self.ffmpeg = ffmpeg

    def apply_subtitles(
        self,
        input_video_path: str,
        vtt_path: str,
        output_video_path: str,
        mode: str,
        subtitle_force_style: str | None = None,
    ) -> str:
        normalized_mode = mode.lower().strip()

        if normalized_mode == "burn":
            return self.ffmpeg.burn_subtitles(
                input_video_path=input_video_path,
                vtt_path=vtt_path,
                output_video_path=output_video_path,
                subtitle_force_style=subtitle_force_style,
            )

        if normalized_mode == "embed":
            return self.ffmpeg.embed_subtitles(
                input_video_path=input_video_path,
                vtt_path=vtt_path,
                output_video_path=output_video_path,
            )

        raise ValueError(f"Unsupported subtitle mode: {mode}")

    def __repr__(self):
        return f"Sx9SubtitleRenderer(ffmpeg={self.ffmpeg})"