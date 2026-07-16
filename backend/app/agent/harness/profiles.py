"""Register deepagents harness profiles for data_agent."""

from __future__ import annotations

import logging

from deepagents import HarnessProfile, register_harness_profile

logger = logging.getLogger(__name__)

_registered = False


def register_data_agent_harness_profiles() -> None:
    global _registered
    if _registered:
        return
    register_harness_profile(
        "openai",
        HarnessProfile(
            excluded_middleware=frozenset({"SummarizationMiddleware"}),
        ),
    )
    _registered = True
    logger.debug("Registered data_agent harness profile (openai)")
