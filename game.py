from dataclasses import dataclass


@dataclass
class Game:
    name: str
    date: str
    price: float
    publisher: str
    developer: str
    platform: str
    genres: list[str]
