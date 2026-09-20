import pandas as pd
import yaml

def load_rules(path: str = "config/rules.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)

def enrich(df: pd.DataFrame, shop_id: str, rules: dict) -> pd.DataFrame:
    r = {**rules.get("default", {}), **rules.get("per_shop", {}).get(shop_id, {})}
    df = df.copy()
    df["shop_id"] = shop_id
    df["ca"] = df["qty"] * df["price"]
    df["commission"] = (df["ca"] * r.get("commission_rate", 0)).round(2)
    df["cout"] = (df["ca"] * r.get("cost_ratio", 0)).round(2)
    df["benefice_net"] = (df["ca"] - df["commission"] - df["cout"]).round(2)
    return df