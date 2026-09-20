from pathlib import Path
import pandas as pd

def write_excel(df: pd.DataFrame, errors: list[dict], run_date: str, out_dir: str) -> str:
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    path = Path(out_dir) / f"ventes_{run_date}.xlsx"
    with pd.ExcelWriter(path, engine="openpyxl") as w:
        df.to_excel(w, sheet_name="Consolidé", index=False)
        if not df.empty:
            for sid, sub in df.groupby("shop_id"):
                sub.to_excel(w, sheet_name=sid[:31], index=False)
        pd.DataFrame(errors or [{"info": "Aucune erreur"}]).to_excel(
            w, sheet_name="Erreurs", index=False)
    return str(path)