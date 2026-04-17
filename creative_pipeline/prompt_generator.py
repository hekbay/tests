import anthropic

from creative_pipeline.config import settings


client = anthropic.Anthropic(api_key=settings.anthropic_api_key)


def generate_image_prompt(brief: str, style_guide: str, product_info: str) -> str:
    """Generate a production-ready image prompt from briefing and expert style."""
    system_prompt = f"""Você é um especialista em criar prompts para IA de imagem.

Seu estilo de referência:
{style_guide}

Suas responsabilidades:
1. Entender o briefing do cliente
2. Traduzir para um prompt visual MUITO detalhado
3. Manter consistência com o estilo do expert
4. Incluir technical specs (resolution, aspect ratio, lighting, camera lens)
5. Adicionar palavras de qualidade (cinematic, premium, high-end)

Formato de saída:
- Responda APENAS com o prompt final
- Em uma única linha, pronto para API de image generation
"""

    user_content = f"""
BRIEFING: {brief}
PRODUTO/CONTEXTO: {product_info}

Gere um prompt detalhado e pronto para IA de imagem.
"""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}],
    )

    return response.content[0].text.strip()
