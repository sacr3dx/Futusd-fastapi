from dataclasses import dataclass

@dataclass(slots=True)
class CashOutDTO:
    base: int
    category: str
    date: int