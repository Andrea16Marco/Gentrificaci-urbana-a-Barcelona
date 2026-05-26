import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def cluster_barris(
    df: pd.DataFrame,
    features: list,
    n_clusters: int = 4,
    random_state: int = 42
):
    """
    Aplica clustering KMeans sobre barris.

    Returns
    -------
    df : pd.DataFrame
    kmeans : KMeans
    scaler : StandardScaler
    metrics : dict
    """

    df = df.copy()

    missing_features = [
        f for f in features
        if f not in df.columns
    ]

    if missing_features:
        raise ValueError(
            f"Variables inexistents: {missing_features}"
        )
    
    mask = df[features].notna().all(axis=1)
    
    X = df.loc[mask, features].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=random_state, 
        n_init="auto"
    )

    labels = kmeans.fit_predict(X_scaled)

    df.loc[mask, "cluster"] = labels
    df["cluster"] = df["cluster"].astype("Int64")

    metrics = {
        "inertia": kmeans.inertia_,
        "silhouette_score": silhouette_score(X_scaled, labels),
        "n_clusters": n_clusters
    }

    return df, kmeans, scaler, metrics
