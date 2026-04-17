from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class Settings:
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    banana_api_key: str = os.getenv("BANANA_API_KEY", "")
    banana_model_id: str = os.getenv("BANANA_MODEL_ID", "stable-diffusion")
    output_dir: Path = Path(os.getenv("OUTPUT_DIR", "output"))


settings = Settings()
settings.output_dir.mkdir(parents=True, exist_ok=True)
