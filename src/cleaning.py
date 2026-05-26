import pandas as pd
import numpy as np

def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Estandarditza els noms de les columnes.

    - elimina espais extres,
    - converteix a minúscules,
    - substitueix espais per underscores,
    - elimina parèntesis,
    - substitueix '/' per '_'.
    """
    
    df = df.copy()
    
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
        .str.replace("/", "_", regex=False)
    )

    return df


def replace_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reemplaça valors faltants habituals per NaN.
    """

    df = df.copy()

    return df.replace(["-", "..", "—", ""], np.nan)

def clean_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converteix automàticament columnes
    numèriques a tipus float.

    Gestiona:
    - comes decimals
    - separadors de milers
    - valors no numèrics
    """

    df = df.copy()

    for col in df.columns:

        if df[col].dtype == "object":

            try:

                df[col] = (
                    df[col]
                    .astype(str)
                    .str.replace(".", "", regex=False)
                    .str.replace(",", ".", regex=False)
                )

                df[col] = pd.to_numeric(
                    df[col],
                    errors="ignore"
                )

            except Exception:

                pass

    return df

def fix_tipus_territori(df):

    df = df.copy()

    mask_barri = (
        df["territori"]
        .str.contains(
            r"\(Barri\)",
            case=False,
            na=False,
        )
    ) & (
        df["tipus_de_territori"] == "-"
    )

    df.loc[
        mask_barri,
        "tipus_de_territori"
    ] = "Barri"

    mask_districte = (
        df["territori"]
        .str.contains(
            r"\(Districte\)",
            case=False,
            na=False,
        )
    ) & (
        df["tipus_de_territori"] == "-"
    )

    df.loc[
        mask_districte,
        "tipus_de_territori"
    ] = "Districte"

    return df