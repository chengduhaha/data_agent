"""Chat-accessible model catalog + per-user model selection (all authenticated users)."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.agent.model_catalog import apply_profile_to_model_config, catalog_as_api, get_catalog_meta
from app.deps import get_user_id
from app.store.io import load_user_config, save_user_config
from app.store.schemas import ModelConfig

router = APIRouter(prefix="/api", tags=["model"])


class ModelSelectRequest(BaseModel):
    model: str = Field(..., min_length=1, description="Catalog model id")


def _mask_model(model_cfg: ModelConfig) -> dict:
    data = model_cfg.model_dump()
    key = data.get("api_key") or ""
    if key:
        data["api_key"] = key[:4] + "…" if len(key) > 4 else "****"
        data["api_key_set"] = True
    else:
        data["api_key_set"] = False
    return data


@router.get("/model-catalog")
async def model_catalog():
    """Synnex / Gateway preset profiles for chat model switcher."""
    return catalog_as_api()


@router.get("/model")
async def get_model(user_id: str = Depends(get_user_id)):
    cfg = await load_user_config(user_id)
    return {"model": _mask_model(cfg.model)}


@router.put("/model")
async def put_model(body: ModelSelectRequest, user_id: str = Depends(get_user_id)):
    existing = await load_user_config(user_id)
    meta = get_catalog_meta()
    existing.model.provider = meta.provider_id
    existing.model.model = body.model.strip()
    apply_profile_to_model_config(existing.model)
    saved = await save_user_config(user_id, existing)
    return {"model": _mask_model(saved.model)}
