"""Prometheus-text harness metrics."""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from app.agent.harness.metrics import render_prometheus

router = APIRouter(tags=["metrics"])


@router.get("/api/metrics", response_class=PlainTextResponse)
async def metrics() -> str:
    return render_prometheus()
