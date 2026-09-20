import imaplib, email, re
from email.header import decode_header
import pandas as pd
from .base import BaseScraper

class EmailScraper(BaseScraper):
    def fetch(self) -> pd.DataFrame:
        cfg = self.cfg
        M = imaplib.IMAP4_SSL(cfg["imap_host"])
        M.login(cfg["imap_user"], cfg["imap_pass"])
        M.select("INBOX")
        _, data = M.search(None, f'(SUBJECT "{cfg["subject_match"]}" SINCE {self.run_date})')
        ids = data[0].split()
        if not ids:
            raise RuntimeError("Aucun e-mail correspondant trouvé")

        _, msg_data = M.fetch(ids[-1], "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        body = self._get_body(msg)

        rows = []
        rx = re.compile(cfg["body_regex"])
        for m in rx.finditer(body):
            rows.append({
                "product": m.group("product").strip(),
                "qty": int(m.group("qty")),
                "price": float(m.group("price").replace(",", ".")),
            })
        M.logout()
        return pd.DataFrame(rows)

    @staticmethod
    def _get_body(msg) -> str:
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode(errors="ignore")
            return ""
        return msg.get_payload(decode=True).decode(errors="ignore")