import pandas as pd
from playwright.sync_api import sync_playwright
from .base import BaseScraper

class SystemAScraper(BaseScraper):
    """3 boutiques partagent cette plateforme → un seul scraper paramétré."""

    def fetch(self) -> pd.DataFrame:
        rows = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.cfg["url"] + "/login", timeout=30_000)
            page.fill("input[name=username]", self.cfg["username"])
            page.fill("input[name=password]", self.cfg["password"])
            page.click("button[type=submit]")
            page.wait_for_load_state("networkidle")

            page.goto(f"{self.cfg['url']}/reports/sales?date={self.run_date}")
            page.wait_for_selector("table#sales tbody tr", timeout=20_000)
            for tr in page.query_selector_all("table#sales tbody tr"):
                cells = tr.query_selector_all("td")
                rows.append({
                    "product": cells[0].inner_text().strip(),
                    "qty": int(cells[1].inner_text().strip() or 0),
                    "price": float(cells[2].inner_text().replace(",", ".").strip()),
                })
            browser.close()
        self.log.info("[%s] %d lignes extraites", self.cfg["id"], len(rows))
        return pd.DataFrame(rows)