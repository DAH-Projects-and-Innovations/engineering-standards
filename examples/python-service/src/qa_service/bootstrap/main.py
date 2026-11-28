"""Entry point: `uvicorn --factory qa_service.bootstrap.main:create_app`."""

from __future__ import annotations

import logging

from fastapi import FastAPI

from qa_service.bootstrap.container import build_answer_question
from qa_service.bootstrap.settings import Settings
from qa_service.interfaces.http.app import build_app


def create_app() -> FastAPI:
    """Read the settings, build the dependencies and return the HTTP application."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    return build_app(build_answer_question(Settings()))
