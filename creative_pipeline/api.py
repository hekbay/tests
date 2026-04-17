from fastapi import FastAPI
from pydantic import BaseModel

from creative_pipeline.pipeline import generate_creative_batch


app = FastAPI(title="Creative Generator API")


class CreativeRequest(BaseModel):
    briefs: list[str]
    expert_id: str


def get_style_guide_from_db(expert_id: str) -> str:
    """Stub for DB integration in Phase 2/3."""
    return f"style-guide-placeholder-for-{expert_id}"


@app.post("/generate-creatives")
async def generate(request: CreativeRequest):
    style_guide = get_style_guide_from_db(request.expert_id)
    task = generate_creative_batch.delay(briefs=request.briefs, style_guide=style_guide)
    return {"task_id": task.id, "status": "processing"}


@app.get("/status/{task_id}")
async def get_status(task_id: str):
    task = generate_creative_batch.AsyncResult(task_id)
    return {"status": task.state, "progress": task.info}
