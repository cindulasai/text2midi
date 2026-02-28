# -*- coding: utf-8 -*-
"""
Configuration Package
Application configuration, LLM management, provider catalog, and genre registry.
"""

from src.config.llm import LLMConfig, call_llm
from src.config.log import setup_logging  # noqa: F401
from src.config.settings import AppSettings  # noqa: F401
from src.config.providers import LiteLLMProvider, validate_api_key  # noqa: F401
from src.config.constants import (  # noqa: F401
    TICKS_PER_BEAT,
    DEFAULT_BARS,
    DEFAULT_TEMPO,
    OUTPUT_DIR,
    MAX_REFINEMENT_ITERATIONS,
)
from src.config.genre_registry import (  # noqa: F401
    GENRE_TREE,
    SCALES_EXTENDED,
    SCALE_ALIASES,
    GM_INSTRUMENTS_EXTENDED,
    GenreNode,
    get_genre,
    get_root_genres,
    get_children,
    all_genre_ids,
    get_genre_ids_for_validation,
    get_tempo_ranges,
    find_by_alias,
    get_genre_instruments,
    resolve_scale,
    get_all_scale_names,
)

__all__ = [
    "LLMConfig",
    "call_llm",
    "setup_logging",
    "GENRE_TREE",
    "SCALES_EXTENDED",
    "SCALE_ALIASES",
    "GM_INSTRUMENTS_EXTENDED",
    "GenreNode",
    "get_genre",
    "get_root_genres",
    "get_children",
    "all_genre_ids",
    "get_genre_ids_for_validation",
    "get_tempo_ranges",
    "find_by_alias",
    "get_genre_instruments",
    "resolve_scale",
    "get_all_scale_names",
]
