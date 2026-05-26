import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.ensemble import RandomForestRegressor

def train_gentrification_model(
    df,
    target="indicador_gentrificacio",
    features=None,
    test_size=0.2,
    random_state=42,
):
    """
    Entrena un model Random Forest per predir
    l'indicador de gentrificació.
    """

    df = df.copy()

    if target not in df.columns:
        raise ValueError(
            f"La variable objectiu '{target}' no existeix"
        )
    
    if features is None:
        excluded_cols = [
            "territori", 
            "any", 
            "territori_id", 
            target, 
            "cluster"
        ]

        features = [
            c for c in df.columns
            if c not in excluded_cols
            and df[c].dtype != "object"
        ]

    missing_features = [
        f for f in features
        if f not in df.columns
    ]

    if missing_features:
        raise ValueError(
            f"Variables inexistents: {missing_features}"
        )

    mask = df[features + [target]].notna().all(axis=1)

    X = df.loc[mask, features]
    y = df.loc[mask, target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, 
        y, 
        test_size=test_size, 
        random_state=random_state
    )

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=random_state,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    metrics = {
        "r2": r2_score(y_test, y_pred),
        "rmse": mean_squared_error(
            y_test,
            y_pred, 
            squared=False
        ),
        "n_train": len(X_train),
        "n_test": len(X_test),
    }

    feature_importance = pd.DataFrame({
        "feature": features,
        "importance": model.feature_importances_
    }).sort_values("importance", ascending=False)

    return model, features, metrics, feature_importance
