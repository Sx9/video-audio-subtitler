from pathlib import Path

from libraries.Sx9FFmpeg import Sx9FFmpeg
from libraries.Sx9MediaInspector import Sx9MediaInspector
from libraries.Sx9PathUtils import Sx9PathUtils
from libraries.Sx9SubtitleRenderer import Sx9SubtitleRenderer
from libraries.Sx9VTTGenerator import Sx9VTTGenerator
from libraries.Sx9Whisper import Sx9Whisper


def main() -> None:
    print("===================================")
    print("Video / Audio Subtitler")
    print("===================================")
    print()

    path_utils = Sx9PathUtils()
    path_utils.ensure_output_folders()

    media_inspector = Sx9MediaInspector()
    ffmpeg = Sx9FFmpeg()
    subtitle_renderer = Sx9SubtitleRenderer(ffmpeg)
    vtt_generator = Sx9VTTGenerator()

    print("Checking FFmpeg...")
    ffmpeg.check_available()
    print("FFmpeg is available.")
    print()

    input_path = ask_existing_file("Enter audio or video file path: ")
    media_type = media_inspector.get_media_type(input_path)

    print()
    print(f"Detected media type: {media_type}")
    print()

    whisper_model_size = ask_whisper_model_size()
    subtitle_mode = ask_subtitle_mode()

    normalized_audio_path = path_utils.audio_output_path(input_path)

    if media_type == "video":
        print()
        print("Extracting audio from video...")
        audio_path_for_transcription = ffmpeg.extract_audio_from_video(
            video_path=input_path,
            output_audio_path=normalized_audio_path,
        )
        base_video_path = input_path
    else:
        print()
        print("Normalizing audio for transcription...")
        audio_path_for_transcription = ffmpeg.normalize_audio_for_whisper(
            audio_path=input_path,
            output_audio_path=normalized_audio_path,
        )

        background_image_path = ask_existing_file("Enter 16:9 background image path: ")
        media_inspector.validate_image(background_image_path)

        if not media_inspector.is_roughly_16x9(background_image_path):
            print()
            print("Warning: image is not exactly 16:9.")
            print("FFmpeg will scale and pad it to 1920x1080.")
            print()

        base_video_path = path_utils.base_video_output_path(input_path)

        print("Creating video from image and audio...")
        ffmpeg.create_video_from_image_and_audio(
            image_path=background_image_path,
            audio_path=input_path,
            output_video_path=base_video_path,
        )

    whisper = Sx9Whisper(model_size=whisper_model_size)

    print()
    segments = whisper.transcribe(audio_path_for_transcription)

    transcript_path = path_utils.transcript_output_path(input_path)
    print()
    print("Writing transcript...")
    whisper.write_plain_text_transcript(
        segments=segments,
        output_path=transcript_path,
    )

    vtt_path = path_utils.vtt_output_path(input_path)
    print("Writing VTT subtitles...")
    vtt_generator.generate_vtt(
        segments=segments,
        output_vtt_path=vtt_path,
    )

    final_video_path = path_utils.final_video_output_path(
        input_path=input_path,
        subtitle_mode=subtitle_mode,
    )

    print()
    print(f"Applying subtitles using mode: {subtitle_mode}")
    subtitle_renderer.apply_subtitles(
        input_video_path=base_video_path,
        vtt_path=vtt_path,
        output_video_path=final_video_path,
        mode=subtitle_mode,
    )

    print()
    print("Done.")
    print()
    print(f"Transcript: {Path(transcript_path).resolve()}")
    print(f"VTT file:   {Path(vtt_path).resolve()}")
    print(f"Video:      {Path(final_video_path).resolve()}")


def ask_existing_file(prompt: str) -> str:
    while True:
        value = input(prompt).strip().strip('"')

        if not value:
            print("Please enter a file path.")
            continue

        path = Path(value)

        if path.exists() and path.is_file():
            return str(path)

        print(f"File not found: {value}")


def ask_whisper_model_size() -> str:
    valid_models = {
        "1": "tiny",
        "2": "base",
        "3": "small",
        "4": "medium",
        "5": "large-v3",
    }

    print("Choose Whisper model:")
    print("1. tiny     - fastest, lowest accuracy")
    print("2. base     - good for testing")
    print("3. small    - better quality")
    print("4. medium   - slower, better quality")
    print("5. large-v3 - slowest, best quality")
    print()

    while True:
        choice = input("Choose model [2]: ").strip()

        if not choice:
            return "base"

        if choice in valid_models:
            return valid_models[choice]

        print("Invalid choice. Choose 1, 2, 3, 4, or 5.")


def ask_subtitle_mode() -> str:
    print()
    print("Subtitle mode:")
    print("1. Burn subtitles into video")
    print("2. Embed subtitles as selectable track")
    print()

    while True:
        choice = input("Choose subtitle mode [1]: ").strip()

        if not choice or choice == "1":
            return "burn"

        if choice == "2":
            return "embed"

        print("Invalid choice. Choose 1 or 2.")


if __name__ == "__main__":
    main()