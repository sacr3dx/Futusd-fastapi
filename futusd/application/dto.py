from dataclasses import dataclass

@dataclass(slots=True)
class SpendingDTO:
    base: int
    category: str

@dataclass(slots=True)
class RegisterDTO:
    username: str
    password: str

@dataclass(slots=True)
class LoginDTO:
    username: str
    password: str