import smtplib
from email.message import EmailMessage
from pathlib import Path

def send_report(cfg: dict, excel_path: str, errors: list[dict]):
    msg = EmailMessage()
    status = "OK" if not errors else f"{len(errors)} erreur(s)"
    msg["Subject"] = f"[Ventes] Rapport quotidien — {status}"
    msg["From"] = cfg["from"]
    msg["To"] = ", ".join(cfg["to"])
    msg.set_content(
        "Rapport de ventes en pièce jointe.\n\n"
        + ("Erreurs :\n" + "\n".join(f"- {e['shop']}: {e['error']}" for e in errors) if errors else "")
    )
    with open(excel_path, "rb") as f:
        msg.add_attachment(f.read(),
                           maintype="application",
                           subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           filename=Path(excel_path).name)
    with smtplib.SMTP(cfg["smtp_host"], cfg["smtp_port"]) as s:
        s.starttls()
        s.login(cfg["smtp_user"], cfg["smtp_pass"])
        s.send_message(msg)