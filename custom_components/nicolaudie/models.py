"""The stick3 integration models."""
from __future__ import annotations

from dataclasses import dataclass

from nicostick import Controller

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator


@dataclass
class NicolaudieData:
    """Data for the shade orb integration."""

    title: str
    device: Controller
    #coordinator: DataUpdateCoordinator[None]
