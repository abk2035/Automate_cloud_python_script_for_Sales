import pandas as pd
from playwright.sync_api import sync_playwright
from .base import BaseScraper

class CustomShopScraper(BaseScraper):
    """Générique pour les sites custom (config via 'selectors' dans YAML)."""

    def fetch(self) -> pd.DataFrame:
        sel = self.cfg["selectors"]
        rows = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.cfg["url"], timeout=30_000)
            page.fill(sel["user_field"], self.cfg["username"])
            page.fill(sel["pass_field"], self.cfg["password"])
            page.click(sel["submit"])
            page.wait_for_load_state("networkidle")
            page.click(sel["report_link"])
            page.wait_for_selector(sel["row"], timeout=20_000)

            for r in page.query_selector_all(sel["row"]):
                def txt(k):
                    e = r.query_selector(sel["cells"][k])
                    return e.inner_text().strip() if e else ""
                rows.append({
                    "product": txt("product"),
                    "qty": int(txt("qty") or 0),
                    "price": float(txt("price").replace(",", ".") or 0),
                })
            browser.close()
        return pd.DataFrame(rows)