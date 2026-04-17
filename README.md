# Creative Generation Pipeline

Implementação base em **3 fases** para análise de criativos de referência, geração de prompts e geração de imagens, com orquestração assíncrona via Celery e API com FastAPI.

## Estrutura

- `creative_pipeline/image_analyzer.py`: análise de imagens com Claude Vision e consolidação de estilo.
- `creative_pipeline/prompt_generator.py`: geração de prompt final com base em briefing + style guide.
- `creative_pipeline/image_generator.py`: integração com Banana.dev + download da imagem.
- `creative_pipeline/pipeline.py`: fluxo completo + batch assíncrono em Celery.
- `creative_pipeline/api.py`: endpoints para iniciar geração e consultar status.

## Fases

1. **Análise de Referências**
   - Extrai padrão visual, CTA, público-alvo e composição.
   - Consolida conhecimento do expert em um `style_guide` reutilizável.

2. **Geração de Prompt**
   - Traduz briefing + contexto do produto em prompt técnico detalhado.
   - Mantém consistência de linguagem visual.

3. **Geração de Imagem**
   - Envia prompt para Banana.dev (modelo configurável).
   - Faz download e persistência local do ativo gerado.

## Como rodar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Variáveis de ambiente esperadas:

- `ANTHROPIC_API_KEY`
- `BANANA_API_KEY`
- `BANANA_MODEL_ID` (opcional, default: `stable-diffusion`)
- `OUTPUT_DIR` (opcional, default: `output`)

### API

```bash
uvicorn creative_pipeline.api:app --reload
```

### Celery (exemplo)

> Configure `celeryconfig.py` com broker/result backend antes de subir o worker.

```bash
celery -A creative_pipeline.pipeline worker --loglevel=info
```

## Próximos passos sugeridos

- Persistir análises e style guide em PostgreSQL.
- Adicionar feedback loop (bom/ruim) para otimizar prompts.
- Gerar 3-5 variações por brief automaticamente.
- A/B testing por canal/campanha.


## Setup rápido com NPM

Se você preferir rodar os comandos via `npm`, use este fluxo:

```bash
npm run setup
npm run check
npm run api
# em outro terminal
npm run worker
```

> Observação: o projeto continua sendo Python; o `package.json` aqui funciona como *task runner*.
