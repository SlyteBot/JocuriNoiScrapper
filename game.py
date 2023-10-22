from dataclasses import dataclass


@dataclass
class Game:
    id: int
    name: str
    date: str
    price: float
    publisher: str
    developer: str
    platform: str
    genres: [str]
