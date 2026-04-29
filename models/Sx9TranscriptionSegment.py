from dataclasses import dataclass


@dataclass
class Sx9TranscriptionSegment:
    start: float
    end: float
    text: str

    def __repr__(self):
        return f"Sx9TranscriptionSegment(start={self.start}, end={self.end}, text='{self.text}')"
