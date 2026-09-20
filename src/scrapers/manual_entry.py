import pandas as pd
from .base import BaseScraper

class ManualEntryScraper(BaseScraper):
    """Lit un CSV où le client a saisi le total du jour (date,total)."""

    def fetch(self) -> pd.DataFrame:
        df = pd.read_csv(self.cfg["source"])
        row = df[df["date"] == self.run_date]
        if row.empty:
            raise RuntimeError(f"Pas de total manuel pour {self.run_date}")
        total = float(row.iloc[0]["total"])
        # On le représente comme une ligne unique non ventilée
        return pd.DataFrame([{
            "product": "TOTAL_JOURNEE",
            "qty": 1,
            "price": total,
        }])