import os, sys, datetime as dt
import yaml
from dotenv import load_dotenv
from utils.logger import get_logger
from processors.calculator import load_rules
from processors.aggregator import run_all
from outputs.excel_writer import write_excel
from outputs.notifier import send_report

load_dotenv()

def resolve_date(mode: str) -> str:
    if mode == "today":
        return dt.date.today().isoformat()
    if mode == "yesterday":
        return (dt.date.today() - dt.timedelta(days=1)).isoformat()
    return mode  # YYYY-MM-DD

def expand_env(obj):
    """Remplace ${VAR} par la valeur d'env, récursivement."""
    if isinstance(obj, dict):
        return {k: expand_env(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [expand_env(v) for v in obj]
    if isinstance(obj, str) and obj.startswith("${") and obj.endswith("}"):
        return os.getenv(obj[2:-1], "")
    return obj

def main():
    log = get_logger()
    with open("config/config.yaml") as f:
        cfg = expand_env(yaml.safe_load(f))

    run_date = resolve_date(cfg["run"]["date"])
    log.info("=== Run pour %s ===", run_date)

    rules = load_rules()
    df, errors = run_all(cfg["shops"], run_date, rules, log)

    excel_path = write_excel(df, errors, run_date, cfg["run"]["output_dir"])
    log.info("Excel généré : %s", excel_path)

    try:
        send_report(cfg["email_report"], excel_path, errors)
        log.info("E-mail envoyé.")
    except Exception as e:
        log.exception("Échec envoi e-mail : %s", e)

    # Code de sortie non nul si erreurs, pour monitoring cloud
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()