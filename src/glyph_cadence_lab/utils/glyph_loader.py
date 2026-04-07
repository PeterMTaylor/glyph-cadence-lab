import yaml
import pathlib
import pandas as pd

BASE_DIR = pathlib.Path(__file__).resolve().parents[3]
GLYPH_DIR = BASE_DIR / "glyphs"
PARQUET_DIR = BASE_DIR / "parquet"


def load_yaml(path: pathlib.Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def flatten_glyph(g: dict) -> dict:
    """
    Flatten nested glyph structures into a row-friendly dict.
    This keeps nested structures JSON-encoded so Parquet can store them cleanly.
    """
    return {
        "glyph_id": g.get("glyph_id"),
        "name": g.get("name"),
        "family": g.get("family"),
        "category": g.get("category"),

        # lineage
        "lineage": g.get("lineage", {}),

        # origin glyphs
        "origin_glyphs": g.get("origin_glyphs", []),

        # function block
        "function": g.get("function", {}),

        # signature block
        "signature": g.get("signature", {}),

        # affect block (whisper / trauma / wildcard)
        "affect": g.get("affect", {}),

        # lists
        "drawer_affinity": g.get("drawer_affinity", []),
        "observational_fragments": g.get("observational_fragments", []),

        # rituals (list of structs)
        "rituals": g.get("rituals", []),

        # risk profile
        "risk_profile": g.get("risk_profile", {}),

        # vault behaviour
        "vault_behavior": g.get("vault_behavior", {}),
    }


def load_all_glyphs() -> pd.DataFrame:
    glyph_files = sorted(GLYPH_DIR.glob("*.glyph.yaml"))
    rows = []

    for gf in glyph_files:
        raw = load_yaml(gf)
        flat = flatten_glyph(raw)
        rows.append(flat)

    return pd.DataFrame(rows)


def write_parquet(df: pd.DataFrame):
    PARQUET_DIR.mkdir(exist_ok=True)
    out_path = PARQUET_DIR / "glyphs.parquet"
    df.to_parquet(out_path, index=False)
    print(f"✓ Wrote {len(df)} glyphs → {out_path}")


if __name__ == "__main__":
    df = load_all_glyphs()
    write_parquet(df)
