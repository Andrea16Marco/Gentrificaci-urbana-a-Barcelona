import pandas as pd
import re
import unicodedata

def normalize_text(text: str) -> str:
    """
    Normalitza text territorial.

    - minúscules
    - elimina accents
    - elimina símbols especials
    - harmonitza espais
    """

    if pd.isna(text):
        return text
    
    text = str(text).strip().lower()

    text = (
        unicodedata
        .normalize("NFKD", text)
        .encode("ascii", "ignore")
        .decode("utf-8")
    )

    text = re.sub(r"\s*\(barri\)", "", text)


    text = re.sub(r"[^a-z0-9\s\-]", "", text)
    text = text.replace("-", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def clean_year_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detecta anys dins noms de columnes i els simplifica.

    Exemple:
    'Població 2020' -> '2020'
    """

    df = df.copy()

    new_cols = {}
    
    for col in df.columns:
        match = re.search(r"(19|20)\d{2}", str(col))

        if match:
            new_cols[col] = match.group(0)

    return df.rename(columns=new_cols)


def remove_aei_suffix(text: str) -> str:
    """
    Elimina sufixos AEI de noms territorials.
    """

    if pd.isna(text):
        return text
    
    return re.sub(r"\s+aei.*$", "", text)


def detect_year_columns(df: pd.DataFrame) -> list:
    """
    Detecta columnes que són anys.
    """

    return [
        c for c in df.columns
        if re.fullmatch(r"(19|20)\d{2}", c)
    ]

def melt_years(
    df: pd.DataFrame,
    id_vars: list,
    value_name: str
) -> pd.DataFrame:
    """
    Converteix datasets wide a format long.
    """

    year_cols = detect_year_columns(df)

    if len(year_cols) == 0:
        raise ValueError(
            "No s'han detectat columnes d'any al dataframe"
        )

    df_long = df.melt(
        id_vars=id_vars,
        value_vars=year_cols,
        var_name="any",
        value_name=value_name
    )

    df_long["any"] = df_long["any"].astype(int)

    return df_long

def harmonize_territory(
    df: pd.DataFrame,
    col: str,
    territory_map: dict
) -> pd.DataFrame:
    """
    Harmonitza noms territorials.
    """

    df = df.copy()

    if col not in df.columns:
        raise ValueError(f"La columna '{col}' no existeix")
    
    df[col] = df[col].astype(str).apply(normalize_text)
    df[col] = df[col].replace(territory_map)

    return df