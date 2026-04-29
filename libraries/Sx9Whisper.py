from faster_whisper import WhisperModel

from models.Sx9TranscriptionSegment import Sx9TranscriptionSegment


class Sx9Whisper:
    def __init__(self, model_size: str = "base", device: str = "cpu", compute_type: str = "int8"):
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.model = None

    def load_model(self) -> None:
        if self.model is None:
            print(f"Loading Whisper model: {self.model_size}")
            self.model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type,
            )

    def transcribe(self, audio_path: str) -> list[Sx9TranscriptionSegment]:
        self.load_model()

        print("Transcribing audio...")
        segments_iterator, info = self.model.transcribe(
            audio_path,
            beam_size=5,
            vad_filter=True,
        )

        print(f"Detected language: {info.language}")
        print(f"Language probability: {info.language_probability:.2f}")

        segments: list[Sx9TranscriptionSegment] = []

        for segment in segments_iterator:
            text = segment.text.strip()

            if not text:
                continue

            segments.append(
                Sx9TranscriptionSegment(
                    start=float(segment.start),
                    end=float(segment.end),
                    text=text,
                )
            )

            print(f"[{segment.start:.2f} -> {segment.end:.2f}] {text}")

        return segments

    def write_plain_text_transcript(
        self,
        segments: list[Sx9TranscriptionSegment],
        output_path: str,
    ) -> str:
        with open(output_path, "w", encoding="utf-8") as file:
            for segment in segments:
                file.write(segment.text)
                file.write("\n")

        return output_path

    def __repr__(self):
        return f"Sx9Whisper(model_size='{self.model_size}', device='{self.device}', compute_type='{self.compute_type}')"
