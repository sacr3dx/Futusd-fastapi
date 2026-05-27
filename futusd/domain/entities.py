from dataclasses import dataclass
from datetime import date

@dataclass(slots=True)
class SpendingDM:
    uuid: str
    base: int
    category: str
    date: date

@dataclass(slots=True)
class UserDM:
    uuid: str
    username: str
    hashed_password: str

