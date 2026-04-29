import subprocess
from pathlib import Path

from PIL import Image

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

    input_path = ask_existing_path("Enter audio/video file path or folder path: ")
    media_paths = find_supported_media_files(input_path, media_inspector)

    if not media_paths:
        print()
        print("No supported audio or video files were found.")
        return

    print()
    print(f"Found {len(media_paths)} supported media file(s).")
    print()

    whisper_model_size = ask_whisper_model_size()
    whisper = Sx9Whisper(model_size=whisper_model_size)

    for index, media_path in enumerate(media_paths, start=1):
        print()
        print("===================================")
        print(f"Processing {index} of {len(media_paths)}")
        print(media_path)
        print("===================================")

        try:
            process_media_file(
                input_path=media_path,
                media_inspector=media_inspector,
                ffmpeg=ffmpeg,
                subtitle_renderer=subtitle_renderer,
                vtt_generator=vtt_generator,
                whisper=whisper,
            )
        except Exception as error:
            print()
            print(f"Failed to process: {media_path}")
            print(f"Error: {error}")
            print("Continuing with the next file.")

    print()
    print("All done.")


def process_media_file(
    input_path: str,
    media_inspector: Sx9MediaInspector,
    ffmpeg: Sx9FFmpeg,
    subtitle_renderer: Sx9SubtitleRenderer,
    vtt_generator: Sx9VTTGenerator,
    whisper: Sx9Whisper,
) -> None:
    source_path = Path(input_path)
    media_type = media_inspector.get_media_type(str(source_path))

    output_paths = get_output_paths(source_path)

    if all(path.exists() for path in output_paths.values()):
        print()
        print("All output files already exist. Skipping.")
        print_outputs(output_paths)
        return

    working_folder = source_path.parent / "temp"
    working_folder.mkdir(parents=True, exist_ok=True)

    normalized_audio_path = working_folder / f"{source_path.stem}-whisper.wav"

    if media_type == "video":
        print()
        print("Extracting audio from video for transcription...")
        audio_path_for_transcription = ffmpeg.extract_audio_from_video(
            video_path=str(source_path),
            output_audio_path=str(normalized_audio_path),
        )
        base_video_path = str(source_path)

        print()
        print("Creating MP3 audio file...")
        export_audio_as_mp3(
            ffmpeg=ffmpeg,
            input_path=str(source_path),
            output_audio_path=str(output_paths["audio"]),
        )
    else:
        print()
        print("Normalizing audio for transcription...")
        audio_path_for_transcription = ffmpeg.normalize_audio_for_whisper(
            audio_path=str(source_path),
            output_audio_path=str(normalized_audio_path),
        )

        print()
        print("Creating MP3 audio file...")
        export_audio_as_mp3(
            ffmpeg=ffmpeg,
            input_path=str(source_path),
            output_audio_path=str(output_paths["audio"]),
        )

        background_image_path = find_matching_background_image(source_path)

        if background_image_path is None:
            background_image_path = create_gray_background_image(source_path)

        media_inspector.validate_image(str(background_image_path))

        if not media_inspector.is_roughly_16x9(str(background_image_path)):
            print()
            print("Warning: image is not exactly 16:9.")
            print("FFmpeg will scale and pad it to 1920x1080.")
            print()

        base_video_path = str(working_folder / f"{source_path.stem}-base.mp4")

        print("Creating video from image and audio...")
        ffmpeg.create_video_from_image_and_audio(
            image_path=str(background_image_path),
            audio_path=str(source_path),
            output_video_path=base_video_path,
        )

    print()
    print(f"Detected media type: {media_type}")
    print("Transcribing...")
    segments = whisper.transcribe(audio_path_for_transcription)

    print()
    print("Writing transcript...")
    whisper.write_plain_text_transcript(
        segments=segments,
        output_path=str(output_paths["transcript"]),
    )

    print("Writing VTT subtitles...")
    vtt_generator.generate_vtt(
        segments=segments,
        output_vtt_path=str(output_paths["subtitles"]),
    )

    print()
    print("Creating burned-subtitles video...")
    subtitle_renderer.apply_subtitles(
        input_video_path=base_video_path,
        vtt_path=str(output_paths["subtitles"]),
        output_video_path=str(output_paths["burned_video"]),
        mode="burn",
    )

    print()
    print("Creating optional-subtitles video...")
    subtitle_renderer.apply_subtitles(
        input_video_path=base_video_path,
        vtt_path=str(output_paths["subtitles"]),
        output_video_path=str(output_paths["optional_video"]),
        mode="embed",
    )

    print()
    print("Done.")
    print_outputs(output_paths)


def ask_existing_path(prompt: str) -> str:
    while True:
        value = input(prompt).strip().strip('"')

        if not value:
            print("Please enter a file or folder path.")
            continue

        path = Path(value)

        if path.exists():
            return str(path)

        print(f"Path not found: {value}")


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


def find_supported_media_files(
    input_path: str,
    media_inspector: Sx9MediaInspector,
) -> list[str]:
    path = Path(input_path)

    if path.is_file():
        try:
            media_inspector.get_media_type(str(path))
            return [str(path)]
        except ValueError:
            return []

    supported_extensions = {
        *media_inspector.AUDIO_EXTENSIONS,
        *media_inspector.VIDEO_EXTENSIONS,
    }

    media_files = []

    for child_path in path.rglob("*"):
        if not child_path.is_file():
            continue

        if child_path.suffix.lower() in supported_extensions:
            media_files.append(str(child_path))

    return sorted(media_files)


def get_output_paths(source_path: Path) -> dict[str, Path]:
    output_folder = source_path.parent
    stem = source_path.stem

    return {
        "burned_video": output_folder / f"{stem}-burned-subtitles.mp4",
        "optional_video": output_folder / f"{stem}-optional-subtitles.mp4",
        "transcript": output_folder / f"{stem}-transcript.txt",
        "audio": output_folder / f"{stem}-audio.mp3",
        "subtitles": output_folder / f"{stem}-subtitles.vtt",
    }


def find_matching_background_image(source_path: Path) -> Path | None:
    for extension in [".jpg", ".jpeg", ".png"]:
        image_path = source_path.with_suffix(extension)

        if image_path.exists() and image_path.is_file():
            return image_path

    return None


def create_gray_background_image(source_path: Path) -> Path:
    temp_folder = source_path.parent / "temp"
    temp_folder.mkdir(parents=True, exist_ok=True)

    image_path = temp_folder / f"{source_path.stem}-gray-background.png"

    if image_path.exists():
        return image_path

    image = Image.new("RGB", (1920, 1080), color=(128, 128, 128))
    image.save(image_path)

    return image_path


def export_audio_as_mp3(
    ffmpeg: Sx9FFmpeg,
    input_path: str,
    output_audio_path: str,
) -> str:
    Path(output_audio_path).parent.mkdir(parents=True, exist_ok=True)

    command = [
        ffmpeg.ffmpeg_command,
        "-y",
        "-i",
        input_path,
        "-vn",
        "-codec:a",
        "libmp3lame",
        "-q:a",
        "2",
        output_audio_path,
    ]

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

    return output_audio_path


def print_outputs(output_paths: dict[str, Path]) -> None:
    print()
    print(f"Burned subtitles video:   {output_paths['burned_video'].resolve()}")
    print(f"Optional subtitles video: {output_paths['optional_video'].resolve()}")
    print(f"Transcript:              {output_paths['transcript'].resolve()}")
    print(f"Audio:                   {output_paths['audio'].resolve()}")
    print(f"VTT subtitles:           {output_paths['subtitles'].resolve()}")


if __name__ == "__main__":
    main()