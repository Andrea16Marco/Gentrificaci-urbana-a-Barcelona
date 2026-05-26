import geopandas as gpd
import pandas as pd

def load_csv(path: str, **kwargs) -> pd.DataFrame:
    """
    Carrega un CSV.
    """

    return pd.read_csv(
        path, 
        encoding="utf-8", 
        sep=",", 
        **kwargs
    )

def save_csv(df: pd.DataFrame, path: str):
    """
    Guarda un CSV.
    """

    df.to_csv(path, index=False, encoding="utf-8")

def load_geojson(path: str) -> gpd.GeoDataFrame:
    """
    Carrega un GeoJSON.
    """

    return gpd.read_file(path)

def save_geojson(gdf: gpd.GeoDataFrame, path: str):
    """
    Guarda un GeoJSON.
    """

    gdf.to_file(path, driver="GeoJSON")

def save_parquet(df: pd.DataFrame, path: str):
    """
    Guarda un fitxer parquet.
    """

    df.to_parquet(path, index=False)

def load_parquet(path: str) -> pd.DataFrame:
    """
    Carrega un fitxer parquet.
    """

    return pd.read_parquet(path)