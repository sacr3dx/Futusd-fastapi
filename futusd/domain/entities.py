from dataclasses import dataclass

@dataclass(slots=True)
class CashOutDM:
    uuid: str
    base: int
    category: str
    date: int


