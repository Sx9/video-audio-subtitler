# Video / Audio Transcriber / Subtitler Documentation

## 1. Project Overview

**Video / Audio Subtitler** is a local Windows-based Python application that generates transcripts and subtitles from audio or video files using Whisper transcription, creates a WebVTT subtitle file, and produces a final video with subtitles either burned into the video or embedded as a selectable subtitle track.

The project is designed to run locally inside a Python virtual environment and uses FFmpeg for all media processing.

---

## 2. Main Features

This application supports the following workflows:

### Video Input Workflow

Given a video file, the application can:

1. Detect that the input is a video.
2. Extract audio from the video using FFmpeg.
3. Normalize the extracted audio for Whisper.
4. Transcribe the audio using `faster-whisper`.
5. Generate a plain text transcript.
6. Generate a `.vtt` subtitle file.
7. Create a final video with either:
   - burned-in subtitles, or
   - embedded selectable subtitles.

### Audio Input Workflow

Given an audio file, the application can:

1. Detect that the input is audio.
2. Normalize the audio for Whisper.
3. Transcribe the audio using `faster-whisper`.
4. Generate a plain text transcript.
5. Generate a `.vtt` subtitle file.
6. Ask the user for a background image.
7. Create a 16:9 video from the image and audio.
8. Create a final video with either:
   - burned-in subtitles, or
   - embedded selectable subtitles.

---

## 3. Technology Stack

### Language

- Python

### Local Environment

- Python virtual environment using `.venv`

### Core Tools

- FFmpeg
- FFprobe
- faster-whisper
- Pillow

### Python Libraries

The main installed Python packages include:

- `faster-whisper`
- `ctranslate2`
- `av`
- `huggingface_hub`
- `onnxruntime`
- `pillow`
- `tqdm`
- `numpy`

The full package list is stored in: text requirements.txt


---

## 4. External Dependency: FFmpeg

FFmpeg is required for:

- checking media capabilities
- extracting audio from video
- normalizing audio
- creating video from an image and audio file
- burning subtitles into a video
- embedding subtitles into a video

FFprobe is required for future media inspection features and is installed with FFmpeg.

### Verify FFmpeg

Run:
powershell ffmpeg -version


### Verify FFprobe

Run:
powershell ffprobe -version


If both commands return version information, FFmpeg is correctly configured.

---

## 5. Project Structure

Current project layout:
text Video - Audio Subtitler/ │ ├── .venv/ │ ├── Documentation/ │ ├── libraries/ │ ├── **init**.py │ ├── Sx9FFmpeg.py │ ├── Sx9MediaInspector.py │ ├── Sx9PathUtils.py │ ├── Sx9SubtitleRenderer.py │ ├── Sx9VTTGenerator.py │ └── Sx9Whisper.py │ ├── models/ │ ├── **init**.py │ ├── Sx9SubtitlingJob.py │ └── Sx9TranscriptionSegment.py │ ├── output/ │ ├── audio/ │ ├── subtitles/ │ ├── transcripts/ │ └── videos/ │ ├── temp/ │ ├── ffmpeger.ps1 ├── main.py └── requirements.txt


---

## 6. Folder Responsibilities

### `.venv/`

Contains the local Python virtual environment.

This folder should not be committed to Git.

### `Documentation/`

Contains project documentation files.

Recommended documentation files:
text Video-Audio-Subtitler-Documentation.md Setup.md Usage.md Troubleshooting.md


### `libraries/`

Contains handler/helper classes for external libraries and processing logic.

This is the main application logic layer.

### `models/`

Contains simple data classes used by the pipeline.

### `output/`

Contains generated files.

Subfolders:
text output/audio/ output/subtitles/ output/transcripts/ output/videos/


### `temp/`

Reserved for temporary working files.

### `main.py`

The CLI entry point for the application.

### `requirements.txt`

Contains pinned Python package dependencies.

### `ffmpeger.ps1`

PowerShell helper script used to add FFmpeg to the Windows User PATH.

---

## 7. Application Architecture

The application follows a simple pipeline architecture:

text User input │ ▼ Media type detection │ ▼ Audio preparation │ ▼ Whisper transcription │ ▼ Transcript generation │ ▼ VTT subtitle generation │ ▼ Video creation or video reuse │ ▼ Subtitle rendering │ ▼ Final video output


---

## 8. Main Pipeline

### Step 1: User Provides Media File

The application asks for a path to an audio or video file.

Supported audio formats include:
text .mp3 .wav .m4a .aac .flac .ogg .wma


Supported video formats include:
text .mp4 .mov .mkv .avi .webm .m4v


---

### Step 2: Media Type Detection

The application determines whether the file is audio or video based on its file extension.

This is handled by:




text libraries/Sx9MediaInspector.py


---

### Step 3: Audio Preparation

If the input is a video, audio is extracted using FFmpeg.

If the input is audio, it is normalized using FFmpeg.

The audio is converted to:
text WAV 16000 Hz mono pcm_s16le


This format is suitable for transcription.

The output audio is written to:
text output/audio/


Example output:
text output/audio/sample_audio.wav

---

### Step 4: Whisper Transcription

The normalized audio is transcribed using `faster-whisper`.

This is handled by:

text libraries/Sx9Whisper.py


The application supports these Whisper model choices:

text tiny base small medium large-v3


Recommended first-run model:
text tiny


Recommended general-use model:
text base


Better quality option:
text small


---

### Step 5: Plain Text Transcript Generation

A plain text transcript is generated from the transcription segments.

The transcript is written to:
text output/transcripts/


Example:
text output/transcripts/sample.txt


---

### Step 6: VTT Subtitle Generation

The application generates a WebVTT file from Whisper segments.

This is handled by:
text libraries/Sx9VTTGenerator.py


The VTT file is written to:
text output/subtitles/


Example:
text output/subtitles/sample.vtt


Example VTT format:
text WEBVTT
00:00:00.000 --> 00:00:03.200 Hello and welcome to the video.
00:00:03.200 --> 00:00:06.800 Today we are generating subtitles locally.


---

### Step 7: Video Preparation

If the original input is a video, the original video is used as the base video.

If the original input is audio, the user is prompted to provide a background image.

Supported image formats include:
text .jpg .jpeg .png .webp .bmp


The image is scaled and padded to 16:9, specifically:
text 1920x1080


The generated base video is written to:
text output/videos/


Example:
text output/videos/sample_base.mp4


---

### Step 8: Subtitle Rendering

The user chooses one of two subtitle modes:
text burn embed


---

## 9. Subtitle Modes

### Burned-In Subtitles

Burned-in subtitles are permanently rendered onto the video image.

#### Advantages

- Works almost everywhere
- Best compatibility
- Good for social media
- Subtitles are always visible

#### Disadvantages

- Cannot be turned off
- Requires video re-encoding
- Slower than embedding subtitles

#### Best For

- YouTube Shorts
- Instagram
- TikTok
- LinkedIn
- Video previews
- Any platform where subtitle compatibility is uncertain

---

### Embedded Subtitles

Embedded subtitles are added as a selectable subtitle track.

#### Advantages

- Can be turned on or off
- Usually faster
- Keeps the video image clean
- Useful for local playback and archives

#### Disadvantages

- Some players/platforms may not show subtitles automatically
- MP4 subtitle support is more limited than MKV
- Uses `mov_text` subtitles for MP4 output

#### Best For

- Local playback
- Archival files
- Uploads to platforms that process subtitle tracks
- Media library use

---

## 10. Output Files

A successful run produces files similar to the following:
text output/audio/sample_audio.wav output/transcripts/sample.txt output/subtitles/sample.vtt output/videos/sample_burn_subtitles.mp4


or:
text output/videos/sample_embed_subtitles.mp4


---

## 11. Class Documentation

Video / Audio Subtitler
File-by-File Purpose and Responsibilities
============================================================

This document explains the purpose and responsibility of every important file and folder in the Video / Audio Subtitler project.

The project is designed as a local Windows-based Python application that:

1. Accepts an audio or video file.
2. Generates a transcript using faster-whisper.
3. Creates a WebVTT subtitle file.
4. Produces a final video with subtitles either burned into the video or embedded as a selectable subtitle track.
5. Supports audio-only input by allowing the user to provide a background image for video generation.


============================================================
PROJECT ROOT
============================================================

Project Root:
Video - Audio Subtitler/

Purpose:
The root folder contains the main application entry point, dependency definitions, PowerShell setup helpers, documentation, source libraries, data models, output folders, temporary folders, and the Python virtual environment.

Main responsibilities:
- Hold the complete local project.
- Provide a predictable folder structure.
- Keep application code separate from generated output.
- Keep documentation separate from implementation.
- Support running the project locally from PowerShell or PyCharm.


============================================================
main.py
============================================================

Path:
main.py

Purpose:
main.py is the main command-line entry point for the application.

This is the file the user runs to start the program.

Run command:
python main.py

Primary responsibilities:
- Display the application title.
- Ensure output folders exist.
- Check that FFmpeg and FFprobe are available.
- Ask the user for the input audio or video file.
- Detect the input media type.
- Ask the user which Whisper model to use.
- Ask whether subtitles should be burned in or embedded.
- For video input:
  - extract audio from the video.
  - use the original video as the base video.
- For audio input:
  - normalize the audio for transcription.
  - ask the user for a background image.
  - validate the image.
  - generate a video from the image and audio.
- Start the Whisper transcription process.
- Generate a plain text transcript.
- Generate a VTT subtitle file.
- Apply subtitles to the video.
- Print final output file locations.

Main collaborators:
- Sx9PathUtils
- Sx9MediaInspector
- Sx9FFmpeg
- Sx9Whisper
- Sx9VTTGenerator
- Sx9SubtitleRenderer

What should stay in this file:
- CLI prompts.
- High-level orchestration.
- User interaction.
- Calling the library classes in the correct order.
- Final status messages.

What should not be added here long-term:
- Raw FFmpeg command construction.
- Whisper implementation details.
- Subtitle formatting logic.
- File type extension lists.
- Complex media processing internals.

Reason:
main.py should remain a coordinator, not a dumping ground for processing logic.


============================================================
requirements.txt
============================================================

Path:
requirements.txt

Purpose:
requirements.txt stores the Python package dependencies required by the project.

Primary responsibilities:
- Allow another environment to install the same packages.
- Record the installed versions of Python libraries.
- Support reproducible setup.

Typical usage:
python -m pip install -r requirements.txt

Main dependencies:
- faster-whisper
- ctranslate2
- av
- huggingface_hub
- pillow
- tqdm
- numpy
- onnxruntime

What should stay in this file:
- Python package dependencies.
- Version pins generated by pip freeze.

What should not be added here:
- FFmpeg, because FFmpeg is installed as a system executable, not as a Python package.
- Local output files.
- Comments about runtime usage unless intentionally curated.

Notes:
If dependencies are added or updated, regenerate this file with:
python -m pip freeze > requirements.txt


============================================================
ffmpeger.ps1
============================================================

Path:
ffmpeger.ps1

Purpose:
ffmpeger.ps1 is a PowerShell helper script used to add the FFmpeg binary folder to the Windows User PATH.

Primary responsibilities:
- Define the FFmpeg bin folder path.
- Read the current Windows User PATH.
- Add FFmpeg to User PATH if it is not already present.

Typical usage:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\ffmpeger.ps1

What should stay in this file:
- Windows PATH setup logic for FFmpeg.
- PowerShell-only environment setup commands.

What should not be added here:
- Python application logic.
- FFmpeg media conversion commands.
- Whisper transcription commands.
- Runtime app workflow.

Notes:
After running this script, PowerShell or PyCharm may need to be restarted before the updated PATH is recognized.


============================================================
.venv/
============================================================

Path:
.venv/

Purpose:
.venv contains the local Python virtual environment.

Primary responsibilities:
- Isolate project Python packages from the system Python installation.
- Store installed packages required by this project.
- Provide the python and pip executables used by this project.

Typical activation command:
.\.venv\Scripts\Activate.ps1

What should be inside:
- Python executable files.
- pip.
- installed packages.
- virtual environment metadata.

What should not be done:
- Do not manually edit package files inside .venv.
- Do not commit .venv to Git.
- Do not store application source files in .venv.

Git recommendation:
.venv/ should be ignored in .gitignore.


============================================================
Documentation/
============================================================

Path:
Documentation/

Purpose:
Documentation contains project notes, setup guides, design descriptions, troubleshooting notes, and file responsibility documents.

Primary responsibilities:
- Explain how the project works.
- Document setup steps.
- Document architecture.
- Document file responsibilities.
- Help future maintenance and onboarding.

Current documentation file:
Documentation/Video-Audio-Subtitler-Documentation.md

Recommended additional documentation:
Documentation/File-Responsibilities.txt
Documentation/Setup.md
Documentation/Usage.md
Documentation/Troubleshooting.md
Documentation/Roadmap.md

What should stay in this folder:
- Markdown documentation.
- Text documentation.
- Architecture notes.
- Setup instructions.
- Troubleshooting steps.

What should not be stored here:
- Generated videos.
- Generated audio files.
- Python virtual environment files.
- Large Whisper model caches.


============================================================
libraries/
============================================================

Path:
libraries/

Purpose:
The libraries folder contains the application’s processing and helper classes.

This folder is the main application logic layer.

Primary responsibilities:
- Encapsulate FFmpeg behavior.
- Encapsulate Whisper behavior.
- Encapsulate VTT generation.
- Encapsulate media type detection.
- Encapsulate subtitle rendering decisions.
- Encapsulate path generation.

Design principle:
Each file in libraries should have a focused responsibility.

This keeps main.py clean and makes the project easier to extend.


============================================================
libraries/__init__.py
============================================================

Path:
libraries/__init__.py

Purpose:
Marks the libraries folder as a Python package.

Primary responsibilities:
- Allow imports from the libraries package.
- Support statements such as:
  from libraries.Sx9FFmpeg import Sx9FFmpeg

What should stay in this file:
- Usually nothing.
- Optional package-level exports in the future.

What should not be added here:
- Application workflow.
- FFmpeg commands.
- Whisper logic.
- Large initialization side effects.


============================================================
libraries/Sx9FFmpeg.py
============================================================

Path:
libraries/Sx9FFmpeg.py

Primary class:
Sx9FFmpeg

Purpose:
Sx9FFmpeg is the project’s FFmpeg and FFprobe wrapper.

It centralizes all direct calls to FFmpeg so that the rest of the application does not need to know the exact FFmpeg command syntax.

Primary responsibilities:
- Check that FFmpeg is available.
- Check that FFprobe is available.
- Extract normalized WAV audio from a video.
- Normalize an audio file for Whisper transcription.
- Create a video from a still image and an audio file.
- Burn subtitles into a video.
- Embed subtitles into a video.
- Run external FFmpeg commands safely through subprocess.
- Raise clear errors when FFmpeg commands fail.
- Escape subtitle file paths for FFmpeg filter usage on Windows.

Main methods:
- check_available()
- extract_audio_from_video()
- normalize_audio_for_whisper()
- create_video_from_image_and_audio()
- burn_subtitles()
- embed_subtitles()
- _run_command()
- _escape_subtitle_path_for_ffmpeg()

Detailed responsibilities:

check_available():
- Runs ffmpeg -version.
- Runs ffprobe -version.
- Confirms both tools are available from the current environment.

extract_audio_from_video():
- Takes a video path.
- Extracts audio from the video.
- Converts audio to:
  - WAV format
  - pcm_s16le codec
  - 16000 Hz sample rate
  - mono channel
- Writes the output to output/audio/.

normalize_audio_for_whisper():
- Takes an audio file.
- Converts it to the same Whisper-friendly WAV format.
- Used for audio-only input files.

create_video_from_image_and_audio():
- Takes a background image and an audio file.
- Creates a 1920x1080 video.
- Scales and pads the image to fit 16:9 without cropping.
- Adds the audio track.
- Outputs an MP4 file.

burn_subtitles():
- Takes a video and a VTT file.
- Permanently renders subtitles into the video image.
- Produces a new MP4 file.
- Best for maximum compatibility.

embed_subtitles():
- Takes a video and a VTT file.
- Adds subtitles as a selectable subtitle track.
- Uses mov_text for MP4 subtitle compatibility.
- Produces a new MP4 file.

_run_command():
- Runs the actual subprocess command.
- Captures stdout and stderr.
- Prints the command being run.
- Raises RuntimeError if FFmpeg fails.

_escape_subtitle_path_for_ffmpeg():
- Converts Windows paths into FFmpeg-friendly paths.
- Replaces backslashes with forward slashes.
- Escapes drive letter colons.
- Used mainly for the subtitles video filter.

What should stay in this file:
- FFmpeg and FFprobe command building.
- subprocess execution logic.
- FFmpeg-specific path escaping.
- Media conversion operations.

What should not be added here:
- CLI input prompts.
- Whisper model loading.
- Transcript text formatting.
- VTT timestamp formatting.
- High-level application workflow.

Future improvement ideas:
- Add ffprobe metadata reading.
- Add duration detection.
- Add video resolution detection.
- Add output format selection.
- Add MKV output for embedded subtitles.
- Add subtitle styling for burned subtitles.
- Add hardware acceleration options.


============================================================
libraries/Sx9MediaInspector.py
============================================================

Path:
libraries/Sx9MediaInspector.py

Primary class:
Sx9MediaInspector

Purpose:
Sx9MediaInspector validates and classifies user-provided media files.

Primary responsibilities:
- Determine whether an input file is audio or video.
- Validate image files used as audio backgrounds.
- Check whether an image is roughly 16:9.
- Keep supported file extension lists centralized.

Supported audio extensions:
- .mp3
- .wav
- .m4a
- .aac
- .flac
- .ogg
- .wma

Supported video extensions:
- .mp4
- .mov
- .mkv
- .avi
- .webm
- .m4v

Supported image extensions:
- .jpg
- .jpeg
- .png
- .webp
- .bmp

Main methods:
- get_media_type()
- validate_image()
- is_roughly_16x9()

Detailed responsibilities:

get_media_type():
- Checks whether the file exists.
- Reads the file extension.
- Returns "audio" for supported audio files.
- Returns "video" for supported video files.
- Raises an error for unsupported file types.

validate_image():
- Checks whether the image exists.
- Checks whether the image extension is supported.
- Opens the image with Pillow.
- Confirms the image has valid dimensions.

is_roughly_16x9():
- Opens the image.
- Calculates width divided by height.
- Compares it to the 16:9 ratio.
- Allows a small tolerance.
- Returns True or False.

What should stay in this file:
- File type extension lists.
- Basic media classification.
- Image validation.
- Lightweight image aspect ratio checks.

What should not be added here:
- FFmpeg conversion commands.
- Whisper transcription code.
- CLI user prompts.
- Output path generation.
- Subtitle rendering logic.

Future improvement ideas:
- Use ffprobe to detect actual media streams instead of relying only on file extensions.
- Detect video resolution.
- Detect audio duration.
- Detect whether a video already contains subtitles.
- Detect whether a file has audio streams.


============================================================
libraries/Sx9PathUtils.py
============================================================

Path:
libraries/Sx9PathUtils.py

Primary class:
Sx9PathUtils

Purpose:
Sx9PathUtils centralizes output folder creation and output filename generation.

Primary responsibilities:
- Ensure required output folders exist.
- Generate consistent output paths for audio.
- Generate consistent output paths for transcripts.
- Generate consistent output paths for VTT subtitle files.
- Generate consistent output paths for base videos.
- Generate consistent output paths for final subtitled videos.

Main methods:
- ensure_output_folders()
- get_stem()
- audio_output_path()
- transcript_output_path()
- vtt_output_path()
- base_video_output_path()
- final_video_output_path()

Detailed responsibilities:

ensure_output_folders():
- Creates these folders if missing:
  - output/
  - output/audio/
  - output/transcripts/
  - output/subtitles/
  - output/videos/
  - temp/

get_stem():
- Extracts the filename without extension.
- Example:
  input: sample-video.mp4
  output: sample-video

audio_output_path():
- Builds the normalized audio output path.
- Example:
  output/audio/sample_audio.wav

transcript_output_path():
- Builds the transcript output path.
- Example:
  output/transcripts/sample.txt

vtt_output_path():
- Builds the VTT subtitle output path.
- Example:
  output/subtitles/sample.vtt

base_video_output_path():
- Builds the base video path for audio-only inputs.
- Example:
  output/videos/sample_base.mp4

final_video_output_path():
- Builds the final video path based on subtitle mode.
- Example:
  output/videos/sample_burn_subtitles.mp4
  output/videos/sample_embed_subtitles.mp4

What should stay in this file:
- Folder creation.
- Path generation.
- Filename conventions.
- Output location conventions.

What should not be added here:
- Media processing.
- FFmpeg commands.
- Whisper transcription.
- CLI prompts.
- File validation beyond simple path formatting.

Future improvement ideas:
- Add timestamped output folders.
- Add collision handling if output files already exist.
- Add configurable output directory.
- Add cleanup helpers.
- Add safe filename sanitization.


============================================================
libraries/Sx9SubtitleRenderer.py
============================================================

Path:
libraries/Sx9SubtitleRenderer.py

Primary class:
Sx9SubtitleRenderer

Purpose:
Sx9SubtitleRenderer decides how subtitles should be applied to a video.

It is a small coordination class that delegates actual FFmpeg work to Sx9FFmpeg.

Primary responsibilities:
- Accept subtitle mode from the application.
- Normalize the subtitle mode value.
- If mode is burn, call Sx9FFmpeg.burn_subtitles().
- If mode is embed, call Sx9FFmpeg.embed_subtitles().
- Raise an error for unsupported subtitle modes.

Main methods:
- apply_subtitles()

Supported modes:
- burn
- embed

Detailed responsibilities:

apply_subtitles():
- Takes:
  - input video path
  - VTT subtitle path
  - output video path
  - subtitle mode
- Chooses the correct FFmpeg wrapper method.
- Returns the final output video path.

What should stay in this file:
- Subtitle mode routing.
- Subtitle application decision logic.
- Validation of supported subtitle modes.

What should not be added here:
- Raw FFmpeg commands.
- Whisper transcription.
- VTT generation.
- CLI prompts.
- File extension lists.

Future improvement ideas:
- Add subtitle mode aliases such as:
  - burned
  - hard
  - embedded
  - soft
- Add support for MKV embedded subtitles.
- Add subtitle styling presets.
- Add automatic fallback from embed to burn if embedding fails.


============================================================
libraries/Sx9VTTGenerator.py
============================================================

Path:
libraries/Sx9VTTGenerator.py

Primary class:
Sx9VTTGenerator

Purpose:
Sx9VTTGenerator converts transcription segments into a valid WebVTT subtitle file.

Primary responsibilities:
- Write the WEBVTT file header.
- Convert segment start and end times to VTT timestamps.
- Clean subtitle text.
- Write subtitle cue blocks.

Main methods:
- generate_vtt()
- format_timestamp()
- clean_text()

Detailed responsibilities:

generate_vtt():
- Accepts a list of Sx9TranscriptionSegment objects.
- Writes WEBVTT at the top of the file.
- Writes each subtitle cue:
  start timestamp --> end timestamp
  subtitle text
- Saves the file to output/subtitles/.

format_timestamp():
- Converts seconds as a float into WebVTT timestamp format.
- Example:
  input: 64.25
  output: 00:01:04.250

clean_text():
- Trims extra spaces.
- Normalizes repeated whitespace into single spaces.
- Keeps subtitle text clean and readable.

What should stay in this file:
- WebVTT formatting.
- Timestamp formatting.
- Subtitle text cleanup.
- VTT file writing.

What should not be added here:
- Whisper transcription.
- FFmpeg subtitle rendering.
- Audio extraction.
- User prompts.
- File type detection.

Future improvement ideas:
- Add SRT generation.
- Add subtitle line wrapping.
- Add max characters per line.
- Add max lines per cue.
- Add minimum and maximum cue duration.
- Add punctuation cleanup.
- Add speaker labels if diarization is added later.


============================================================
libraries/Sx9Whisper.py
============================================================

Path:
libraries/Sx9Whisper.py

Primary class:
Sx9Whisper

Purpose:
Sx9Whisper wraps the faster-whisper library and converts transcription output into project-specific transcription segment objects.

Primary responsibilities:
- Store Whisper model settings.
- Lazily load the Whisper model.
- Transcribe normalized audio.
- Print detected language and language probability.
- Convert faster-whisper segments into Sx9TranscriptionSegment objects.
- Write a plain text transcript.

Main methods:
- load_model()
- transcribe()
- write_plain_text_transcript()

Detailed responsibilities:

load_model():
- Loads the selected faster-whisper model.
- Uses CPU by default.
- Uses int8 compute by default.
- Loads only once per Sx9Whisper instance.

transcribe():
- Takes a normalized audio file path.
- Runs faster-whisper transcription.
- Uses VAD filtering to reduce silence/noise.
- Converts each returned segment into Sx9TranscriptionSegment.
- Skips empty text segments.
- Prints segment timestamps and text during processing.
- Returns a list of transcription segments.

write_plain_text_transcript():
- Takes transcription segments.
- Writes each segment’s text to a text file.
- Saves transcript in output/transcripts/.

Default settings:
- model_size: base
- device: cpu
- compute_type: int8

What should stay in this file:
- faster-whisper integration.
- Whisper model configuration.
- Transcription logic.
- Plain text transcript writing.

What should not be added here:
- FFmpeg command construction.
- VTT timestamp formatting.
- Subtitle rendering.
- CLI prompts.
- Output path naming rules.

Future improvement ideas:
- Add language selection.
- Add translation mode.
- Add GPU support.
- Add configurable beam size.
- Add configurable VAD settings.
- Add word-level timestamps.
- Add confidence scoring if available.
- Add progress reporting.


============================================================
models/
============================================================

Path:
models/

Purpose:
The models folder contains simple data classes used by the application.

Primary responsibilities:
- Define structured data objects.
- Avoid passing around unstructured dictionaries.
- Make future features easier to implement.

Design principle:
Models should be simple and should not contain heavy business logic.


============================================================
models/__init__.py
============================================================

Path:
models/__init__.py

Purpose:
Marks the models folder as a Python package.

Primary responsibilities:
- Allow imports from the models package.
- Support statements such as:
  from models.Sx9TranscriptionSegment import Sx9TranscriptionSegment

What should stay in this file:
- Usually nothing.
- Optional package-level exports in the future.

What should not be added here:
- Application runtime workflow.
- FFmpeg commands.
- Whisper model loading.
- Complex logic.


============================================================
models/Sx9TranscriptionSegment.py
============================================================

Path:
models/Sx9TranscriptionSegment.py

Primary class:
Sx9TranscriptionSegment

Purpose:
Sx9TranscriptionSegment represents one timestamped transcription segment.

Primary responsibilities:
- Store the start time of a segment.
- Store the end time of a segment.
- Store the text for that segment.

Fields:
- start: float
- end: float
- text: str

Example:
start = 0.00
end = 3.25
text = "Hello and welcome to this video."

Used by:
- Sx9Whisper
- Sx9VTTGenerator
- transcript writing logic

What should stay in this file:
- The dataclass definition.
- Possibly simple helper methods in the future.

What should not be added here:
- Whisper transcription logic.
- VTT file writing.
- FFmpeg commands.
- CLI prompts.

Future improvement ideas:
- Add duration property.
- Add confidence score.
- Add speaker label.
- Add word-level timestamps.
- Add original language metadata.


============================================================
models/Sx9SubtitlingJob.py
============================================================

Path:
models/Sx9SubtitlingJob.py

Primary class:
Sx9SubtitlingJob

Purpose:
Sx9SubtitlingJob represents the configuration for one complete subtitling job.

Primary responsibilities:
- Store the input media path.
- Store detected media type.
- Store subtitle mode.
- Store optional background image path.
- Store Whisper model size.

Fields:
- input_path: str
- media_type: str
- subtitle_mode: str
- background_image_path: Optional[str]
- whisper_model_size: str

Current usage:
This model is available for future expansion. The current CLI can operate without heavily using it, but it is useful for future batch processing, GUI workflows, and cleaner job orchestration.

Potential future uses:
- Store one job in a batch queue.
- Pass a complete job object through the pipeline.
- Save job history.
- Serialize job settings to JSON.
- Re-run previous jobs.

What should stay in this file:
- Job configuration data.
- Lightweight helper properties if needed.

What should not be added here:
- FFmpeg command execution.
- Whisper transcription.
- User prompts.
- File writing logic.

Future improvement ideas:
- Add output directory field.
- Add language field.
- Add subtitle format field.
- Add output video format field.
- Add status field.
- Add timestamps for job start and completion.
- Add error message field.


============================================================
output/
============================================================

Path:
output/

Purpose:
The output folder contains generated files produced by the application.

Primary responsibilities:
- Keep generated media separate from source code.
- Organize outputs by file type.
- Make results easy to find after a run.

Subfolders:
- output/audio/
- output/subtitles/
- output/transcripts/
- output/videos/

Git recommendation:
The output folder should usually be ignored by Git because it can contain large generated files.


============================================================
output/audio/
============================================================

Path:
output/audio/

Purpose:
Stores normalized audio files used for Whisper transcription.

Primary responsibilities:
- Store audio extracted from video files.
- Store normalized audio converted from audio-only inputs.
- Provide clean WAV files for transcription.

Typical generated files:
sample_audio.wav

Audio format:
- WAV
- pcm_s16le
- 16000 Hz
- mono

What should stay here:
- Generated intermediate audio files.

What should not be stored here:
- Source code.
- Documentation.
- Permanent manually curated audio assets unless intentionally added.


============================================================
output/subtitles/
============================================================

Path:
output/subtitles/

Purpose:
Stores generated subtitle files.

Primary responsibilities:
- Store WebVTT subtitle output.
- Provide subtitle files used for burning or embedding.

Typical generated files:
sample.vtt

What should stay here:
- Generated .vtt subtitle files.

Future possible files:
- .srt subtitle files
- .ass subtitle files
- styled subtitle files

What should not be stored here:
- Videos.
- Normalized audio.
- Source code.


============================================================
output/transcripts/
============================================================

Path:
output/transcripts/

Purpose:
Stores plain text transcript files.

Primary responsibilities:
- Store readable text transcription output.
- Provide a quick review file separate from subtitles.

Typical generated files:
sample.txt

What should stay here:
- Generated .txt transcript files.

What should not be stored here:
- Videos.
- Audio files.
- Subtitle files unless intentionally copied.


============================================================
output/videos/
============================================================

Path:
output/videos/

Purpose:
Stores generated video files.

Primary responsibilities:
- Store base videos created from audio plus image.
- Store final videos with burned subtitles.
- Store final videos with embedded subtitles.

Typical generated files:
sample_base.mp4
sample_burn_subtitles.mp4
sample_embed_subtitles.mp4

What should stay here:
- Generated videos.

What should not be stored here:
- Source code.
- Virtual environment files.
- Documentation.


============================================================
temp/
============================================================

Path:
temp/

Purpose:
Reserved for temporary working files.

Current status:
The current first version does not heavily depend on temp, but the folder is available for future intermediate processing.

Potential future uses:
- Temporary converted subtitle files.
- Temporary audio chunks.
- Temporary extracted media streams.
- Temporary batch processing files.
- Intermediate subtitle styling files.

Git recommendation:
temp/ should usually be ignored by Git.


============================================================
Recommended .gitignore Responsibilities
============================================================

A .gitignore file should be added at the project root if not already present.

Purpose:
Prevent unnecessary or large generated files from being committed.

Recommended ignored paths:
.venv/
__pycache__/
*.pyc
*.pyo
*.pyd
output/
temp/
.idea/
.DS_Store
Thumbs.db

Recommended committed paths:
main.py
libraries/
models/
Documentation/
requirements.txt
ffmpeger.ps1

Reason:
The source code and documentation should be versioned.
The virtual environment and generated media should not be versioned.


============================================================
High-Level Responsibility Flow
============================================================

The application flow can be summarized as:

main.py
- Controls the app flow.
- Asks the user questions.
- Calls helper classes.

Sx9MediaInspector
- Figures out what kind of input file was provided.
- Validates images.

Sx9PathUtils
- Creates folders.
- Determines where output files should go.

Sx9FFmpeg
- Performs all FFmpeg and FFprobe operations.

Sx9Whisper
- Performs transcription using faster-whisper.

Sx9VTTGenerator
- Creates the VTT subtitle file.

Sx9SubtitleRenderer
- Decides whether to burn or embed subtitles.

Sx9TranscriptionSegment
- Represents one timestamped transcription result.

Sx9SubtitlingJob
- Represents the configuration for a full subtitling job.


============================================================
Dependency Direction
============================================================

The intended dependency direction is:

main.py
  depends on libraries and models

libraries/
  may depend on models

models/
  should not depend on libraries

This keeps the architecture clean.

Good:
main.py imports Sx9FFmpeg.
Sx9Whisper imports Sx9TranscriptionSegment.
Sx9VTTGenerator imports Sx9TranscriptionSegment.

Avoid:
models importing Sx9FFmpeg.
models importing Sx9Whisper.
Sx9VTTGenerator directly running FFmpeg.
Sx9MediaInspector asking the user for input.


============================================================
Design Rules for Future Development
============================================================

1. Keep main.py focused on orchestration.
2. Keep FFmpeg commands inside Sx9FFmpeg.
3. Keep Whisper logic inside Sx9Whisper.
4. Keep subtitle file formatting inside Sx9VTTGenerator.
5. Keep subtitle application decisions inside Sx9SubtitleRenderer.
6. Keep path naming inside Sx9PathUtils.
7. Keep file type validation inside Sx9MediaInspector.
8. Keep data-only objects in models/.
9. Do not put generated output into source folders.
10. Do not commit .venv or generated videos to Git.


============================================================
End of File
============================================================