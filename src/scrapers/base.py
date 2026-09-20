from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List
import pandas as pd

@dataclass
class ShopResult:
    shop_id: str
    shop_name: str
    df: pd.DataFrame = field(default_factory=pd.DataFrame)
    error: str | None = None
    ok: bool = True

class BaseScraper(ABC):
    def __init__(self, cfg: dict, run_date: str, logger):
        self.cfg = cfg
        self.run_date = run_date
        self.log = logger

    @abstractmethod
    def fetch(self) -> pd.DataFrame:
        """Retourne un DataFrame avec colonnes: product, qty, price."""