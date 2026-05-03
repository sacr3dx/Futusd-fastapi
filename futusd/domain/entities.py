from dataclasses import dataclass
from datetime import date

@dataclass(slots=True)
class CashOutDM:
    uuid: str
    base: int
    category: str
    date: date


