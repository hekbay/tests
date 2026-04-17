import base64
import json
from pathlib import Path
from typing import Any

import anthropic

from creative_pipeline.config import settings


client = anthropic.Anthropic(api_key=settings.anthropic_api_key)


def analyze_creative_reference(image_path: str) -> dict[str, Any]:
    """Analyze a reference creative and extract style patterns as structured JSON."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    image_data = base64.standard_b64encode(path.read_bytes()).decode("utf-8")

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1500,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": (
                            "Analise este criativo e extraia: \n"
                            "1. Estilo visual (cores dominantes, tipografia, composição)\n"
                            "2. Elementos chave (ícones, mascotes, texto)\n"
                            "3. Call-to-Action (se houver)\n"
                            "4. Público-alvo aparente\n"
                            "5. Padrões de design (layout, hierarchy).\n"
                            "Responda em JSON estruturado."
                        ),
                    },
                ],
            }
        ],
    )

    return {"image_path": str(path), "analysis": message.content[0].text}


def build_knowledge_base(reference_folder: str) -> str:
    """Process multiple references and summarize signature visual style."""
    folder = Path(reference_folder)
    if not folder.exists():
        raise FileNotFoundError(f"Reference folder not found: {reference_folder}")

    analyses = [analyze_creative_reference(str(img)) for img in folder.glob("*.jpg")]
    if not analyses:
        raise ValueError("No .jpg images found in reference folder")

    consolidation_prompt = (
        f"Aqui estão análises de {len(analyses)} criativos do nosso expert:\n\n"
        f"{chr(10).join([json.dumps(a, ensure_ascii=False) for a in analyses])}\n\n"
        "Por favor, identifique e resuma:\n"
        "- Paleta de cores característica\n"
        "- Estilo tipográfico preferido\n"
        "- Elementos visuais recorrentes\n"
        "- Estrutura compositiva comum\n"
        "- Tom/vibe geral dos criativos\n\n"
        "Retorne em formato JSON para ser persistido em banco de dados."
    )

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        messages=[{"role": "user", "content": consolidation_prompt}],
    )

    return response.content[0].text
