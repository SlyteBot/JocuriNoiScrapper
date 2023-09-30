from dataclasses import dataclass

@dataclass
class Game:
    name: str
    date: str
    price: float
    publisher_name: str
    developer_name: str
    platform: str
    genres: list[str]
    age: str