from pathlib import Path

import yaml


class Sx9SubtitleStyleConfig:
    DEFAULT_CONFIG_PATH = "subtitle-style.yaml"

    def __init__(self, config_path: str = DEFAULT_CONFIG_PATH):
        self.config_path = config_path

    def load_force_style(self) -> str | None:
        path = Path(self.config_path)

        if not path.exists():
            print()
            print(f"Subtitle style config not found: {path.resolve()}")
            print("Using FFmpeg default subtitle styling.")
            return None

        with open(path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file) or {}

        active_preset_name = config.get("active_preset", "clean")
        presets = config.get("presets", {})
        preset = presets.get(active_preset_name)

        if not preset:
            raise ValueError(f"Subtitle style preset not found: {active_preset_name}")

        return self._build_force_style(preset)

    def _build_force_style(self, preset: dict) -> str:
        style_parts = {
            "FontName": preset.get("font_name", "Arial"),
            "FontSize": preset.get("font_size", 28),
            "PrimaryColour": preset.get("primary_colour", "&H00FFFFFF"),
            "OutlineColour": preset.get("outline_colour", "&H00000000"),
            "BackColour": preset.get("back_colour", "&H80000000"),
            "Bold": -1 if preset.get("bold", False) else 0,
            "Italic": -1 if preset.get("italic", False) else 0,
            "BorderStyle": preset.get("border_style", 1),
            "Outline": preset.get("outline", 2),
            "Shadow": preset.get("shadow", 1),
            "Alignment": preset.get("alignment", 2),
            "MarginV": preset.get("margin_v", 48),
        }

        return ",".join(f"{key}={value}" for key, value in style_parts.items())

    def __repr__(self):
        return f"Sx9SubtitleStyleConfig(config_path='{self.config_path}')"