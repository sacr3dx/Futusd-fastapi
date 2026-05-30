from dataclasses import dataclass

@dataclass(slots=True)
class SpendingDTO:
    base: int
    category: str

@dataclass(slots=True)
class UserDTO:
    username: str
    password: str