import pandas as pd
from bs4 import BeautifulSoup
import requests
from .base import BaseScraper

class SystemBScraper(BaseScraper):
    """Système B : API interne simple → requests + BS4."""

    def fetch(self) -> pd.DataFrame:
        s = requests.Session()
        s.post(f"{self.cfg['url']}/api/login",
               json={"u": self.cfg["username"], "p": self.cfg["password"]},
               timeout=20)
        r = s.get(f"{self.cfg['url']}/api/sales/{self.run_date}", timeout=20)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        rows = []
        for el in soup.select("div.sale-item"):
            rows.append({
                "product": el.get("data-name"),
                "qty": int(el.get("data-qty", 0)),
                "price": float(el.get("data-price", 0)),
            })
        return pd.DataFrame(rows)