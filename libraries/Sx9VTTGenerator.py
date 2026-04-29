from models.Sx9TranscriptionSegment import Sx9TranscriptionSegment


class Sx9VTTGenerator:
    def generate_vtt(
        self,
        segments: list[Sx9TranscriptionSegment],
        output_vtt_path: str,
    ) -> str:
        with open(output_vtt_path, "w", encoding="utf-8") as file:
            file.write("WEBVTT\n\n")

            for segment in segments:
                start = self.format_timestamp(segment.start)
                end = self.format_timestamp(segment.end)
                text = self.clean_text(segment.text)

                file.write(f"{start} --> {end}\n")
                file.write(f"{text}\n\n")

        return output_vtt_path

    def format_timestamp(self, seconds: float) -> str:
        total_milliseconds = int(round(seconds * 1000))

        hours = total_milliseconds // 3_600_000
        total_milliseconds %= 3_600_000

        minutes = total_milliseconds // 60_000
        total_milliseconds %= 60_000

        secs = total_milliseconds // 1000
        millis = total_milliseconds % 1000

        return f"{hours:02}:{minutes:02}:{secs:02}.{millis:03}"

    def clean_text(self, text: str) -> str:
        return " ".join(text.strip().split())

    def __repr__(self):
        return f"Sx9VTTGenerator()"