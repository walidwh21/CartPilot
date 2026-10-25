from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Product:
    name: str
    category: str
    store: str
    price: float
    brand: str
    tags: frozenset
    distance_km: float
    rating: float  # 0..5


@dataclass
class Profile:
    avoid_tags: set = field(default_factory=set)       # e.g. {"nuts", "gluten"}
    preferred_brands: set = field(default_factory=set)
    max_distance_km: float = 15.0
    budget: float | None = None                        # overrides budget parsed from text


@dataclass
class Request:
    text: str
    wanted: list = field(default_factory=list)          # category names
    budget: float | None = None


@dataclass
class Pick:
    category: str
    product: Product
    score: float
