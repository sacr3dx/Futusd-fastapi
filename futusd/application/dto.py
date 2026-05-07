from dataclasses import dataclass

@dataclass(slots=True)
class SpendingDTO:
    base: int
    category: str
