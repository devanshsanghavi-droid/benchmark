"""Registry of ride-generator implementations, so several can coexist and be compared.

    from robotaxi.rides.registry import create, available
    gen = create("commercial_to_commercial/tlc_overture_v1")
"""
from __future__ import annotations

from typing import Callable

from .interface import RideGenerator

_FACTORIES: dict[str, Callable[..., RideGenerator]] = {}


def register(name: str, factory: Callable[..., RideGenerator]) -> None:
    if name in _FACTORIES:
        raise ValueError(f"generator {name!r} already registered")
    _FACTORIES[name] = factory


def available() -> list[str]:
    return sorted(_FACTORIES)


def create(name: str, **kwargs) -> RideGenerator:
    try:
        return _FACTORIES[name](**kwargs)
    except KeyError:
        raise KeyError(f"unknown generator {name!r}; available: {available()}") from None


def _register_builtin() -> None:
    from .commercial.generator import CommercialToCommercialGenerator
    register(CommercialToCommercialGenerator.name, CommercialToCommercialGenerator)


_register_builtin()
