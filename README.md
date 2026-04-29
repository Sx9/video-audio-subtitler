# Video / Audio Subtitler

A local Windows-based Python application for generating transcripts and subtitles from audio or video files using faster-whisper and FFmpeg.

## Features

- Accept audio or video input
- Generate a plain text transcript
- Generate a WebVTT subtitle file
- Create a video from audio plus a background image
- Burn subtitles directly into the video
- Embed subtitles as a selectable subtitle track

## Video Input Workflow

1. User provides a video file.
2. FFmpeg extracts normalized audio from the video.
3. faster-whisper transcribes the audio.
4. The app writes a plain text transcript.
5. The app writes a VTT subtitle file.
6. The app creates a final video with burned or embedded subtitles.

## Audio Input Workflow

1. User provides an audio file.
2. FFmpeg normalizes the audio for transcription.
3. faster-whisper transcribes the audio.
4. The app writes a plain text transcript.
5. The app writes a VTT subtitle file.
6. User provides a background image.
7. FFmpeg creates a 16:9 video from the image and audio.
8. The app creates a final video with burned or embedded subtitles.

## Subtitle Modes

### Burned Subtitles

Burned subtitles are permanently rendered into the video image.

Best for:

- Social media
- Maximum compatibility
- Videos where subtitles should always be visible

### Embedded Subtitles

Embedded subtitles are added as a selectable subtitle track.

Best for:

- Local playback
- Archival videos
- Situations where subtitles should be optional

## Project Structure

Video - Audio Subtitler/
  Documentation/
    Video-Audio-Subtitler-Documentation.md
  libraries/
    __init__.py
    Sx9FFmpeg.py
    Sx9MediaInspector.py
    Sx9PathUtils.py
    Sx9SubtitleRenderer.py
    Sx9VTTGenerator.py
    Sx9Whisper.py
  models/
    __init__.py
    Sx9SubtitlingJob.py
    Sx9TranscriptionSegment.py
  output/
    audio/
    subtitles/
    transcripts/
    videos/
  temp/
  ffmpeger.ps1
  main.py
  README.md
  requirements.txt

## Requirements

- Windows
- Python
- Python virtual environment
- FFmpeg
- FFprobe
- faster-whisper
- Pillow

## FFmpeg Setup

FFmpeg must be installed and available on PATH.

Verify FFmpeg with:

ffmpeg -version

Verify FFprobe with:

ffprobe -version

If FFmpeg is installed but not recognized, run:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\ffmpeger.ps1

Then restart PowerShell or PyCharm.

## Virtual Environment Setup

Activate the virtual environment:

.\.venv\Scripts\Activate.ps1

Install dependencies:

python -m pip install -r requirements.txt

## Running the Application

From the project root, with the virtual environment activated:

python main.py

The application will ask for:

1. Audio or video file path
2. Whisper model size
3. Subtitle mode
4. Background image path if the input is audio-only

## Whisper Model Options

The app supports these model choices:

- tiny
- base
- small
- medium
- large-v3

Recommended first test:

tiny

Recommended normal use:

base

Better quality:

small

## Supported Input Formats

### Audio

- .mp3
- .wav
- .m4a
- .aac
- .flac
- .ogg
- .wma

### Video

- .mp4
- .mov
- .mkv
- .avi
- .webm
- .m4v

### Images

- .jpg
- .jpeg
- .png
- .webp
- .bmp

## Output Files

Generated files are written to the output folder.

Typical outputs:

- output/audio/sample_audio.wav
- output/transcripts/sample.txt
- output/subtitles/sample.vtt
- output/videos/sample_burn_subtitles.mp4
- output/videos/sample_embed_subtitles.mp4

## Main Components

### main.py

Command-line entry point.

Responsible for:

- Asking the user for input
- Running the full pipeline
- Calling the library classes
- Printing final output paths

### libraries/Sx9FFmpeg.py

Wrapper around FFmpeg and FFprobe.

Responsible for:

- Checking FFmpeg availability
- Extracting audio from video
- Normalizing audio
- Creating video from image and audio
- Burning subtitles
- Embedding subtitles

### libraries/Sx9Whisper.py

Wrapper around faster-whisper.

Responsible for:

- Loading the Whisper model
- Transcribing audio
- Creating transcription segments
- Writing plain text transcripts

### libraries/Sx9VTTGenerator.py

Generates WebVTT subtitle files.

Responsible for:

- Formatting timestamps
- Cleaning subtitle text
- Writing VTT files

### libraries/Sx9MediaInspector.py

Validates and classifies media files.

Responsible for:

- Detecting audio files
- Detecting video files
- Validating image files
- Checking whether images are roughly 16:9

### libraries/Sx9SubtitleRenderer.py

Chooses how subtitles are applied.

Responsible for:

- Burning subtitles
- Embedding subtitles
- Delegating to Sx9FFmpeg

### libraries/Sx9PathUtils.py

Centralizes output path generation.

Responsible for:

- Creating output folders
- Building consistent output file paths

### models/Sx9TranscriptionSegment.py

Data model for one timestamped transcription segment.

### models/Sx9SubtitlingJob.py

Data model for a complete subtitling job configuration.

## Basic Workflow

Input media
  -> Detect media type
  -> Prepare audio
  -> Transcribe with Whisper
  -> Generate transcript
  -> Generate VTT subtitles
  -> Create or reuse video
  -> Burn or embed subtitles
  -> Final video output

## Git Notes

Recommended ignored files and folders:

- .venv/
- __pycache__/
- output/
- temp/
- .idea/

Generated media files should generally not be committed.

Main source files to commit:

- main.py
- libraries/
- models/
- Documentation/
- requirements.txt
- ffmpeger.ps1
- README.md

## Common Commands

Activate venv:

.\.venv\Scripts\Activate.ps1

Run app:

python main.py

Verify FFmpeg:

ffmpeg -version

Verify FFprobe:

ffprobe -version

Install dependencies:

python -m pip install -r requirements.txt

Freeze dependencies:

python -m pip freeze > requirements.txt

Git status:

git status

Commit changes:

git add .
git commit -m "Update project"

Push changes:

git push

## Notes

- The first transcription may take time because the Whisper model may need to download.
- Burned subtitles are most compatible across players and platforms.
- Embedded subtitles may need to be manually enabled in some video players.
- Audio-only inputs require a background image to create a video.
- Non-16:9 images are scaled and padded to 1920x1080.

## License

No license has been specified yet.
