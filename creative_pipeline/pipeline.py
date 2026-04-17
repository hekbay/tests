from datetime import datetime, timezone
from pathlib import Path

from celery import Celery

from creative_pipeline.image_generator import download_image, generate_with_banana
from creative_pipeline.prompt_generator import generate_image_prompt


app = Celery("creative_generator")
app.config_from_object("celeryconfig")


def create_creative(brief: str, style_guide: str, output_path: str) -> dict:
    prompt = generate_image_prompt(brief, style_guide, "seu-produto")
    image_url = generate_with_banana(prompt)
    image_path = download_image(image_url, output_path)

    return {
        "brief": brief,
        "prompt_generated": prompt,
        "image_url": image_url,
        "image_path": image_path,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "success",
    }


@app.task(bind=True)
def generate_creative_batch(self, briefs: list[str], style_guide: str, output_dir: str = "output"):
    """Async task for generating multiple creatives with progress updates."""
    results: list[dict] = []
    base = Path(output_dir)
    base.mkdir(parents=True, exist_ok=True)

    for i, brief in enumerate(briefs):
        self.update_state(state="PROGRESS", meta={"current": i, "total": len(briefs)})

        try:
            result = create_creative(brief, style_guide, str(base / f"creative_{i}.png"))
            results.append(result)
        except Exception as exc:  # noqa: BLE001
            results.append(
                {
                    "brief": brief,
                    "error": str(exc),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "status": "failed",
                }
            )

    return results
