from pathlib import Path

import requests

from creative_pipeline.config import settings


def generate_with_banana(prompt: str, api_key: str | None = None) -> str:
    """Generate image with Banana.dev and return public image URL."""
    key = api_key or settings.banana_api_key
    if not key:
        raise ValueError("Banana API key is required")

    url = "https://api.banana.dev/start/v4/"
    payload = {
        "api_key": key,
        "model_id": settings.banana_model_id,
        "modelInputs": {
            "prompt": prompt,
            "negative_prompt": "blurry, low quality, watermark",
            "num_inference_steps": 50,
            "guidance_scale": 7.5,
            "height": 1024,
            "width": 1024,
        },
    }

    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()
    result = response.json()

    image_url = result.get("modelOutputs", {}).get("image_url")
    if not image_url:
        raise RuntimeError(f"Banana response did not contain image_url: {result}")
    return image_url


def download_image(image_url: str, output_path: str) -> str:
    """Download generated image into output path."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    img_response = requests.get(image_url, timeout=60)
    img_response.raise_for_status()
    path.write_bytes(img_response.content)

    return str(path)
