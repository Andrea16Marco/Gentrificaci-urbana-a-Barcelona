import pandas as pd

def merge_master(
    df_income: pd.DataFrame,
    df_rent: pd.DataFrame,
    df_pop: pd.DataFrame,
    df_nat: pd.DataFrame,
) -> pd.DataFrame:
    """
    Construeix el dataset mestre del projecte.
    """

    df_income = df_income.copy()
    df_rent = df_rent.copy()
    df_pop = df_pop.copy()
    df_nat = df_nat.copy()

    df_income = df_income.rename(columns={"arealabel": "territori"})
    df_income["tipus_de_territori"] = "barri"

    nat_cols = [
        c for c in df_nat.columns 
        if "nacionalitat" in c.lower()
    ]

    if not nat_cols:
        raise ValueError(
            "No s'ha trobat cap columna de nacionalitat"
        )
    
    nat_col = nat_cols[0]

    df_nat = df_nat.rename(
        columns={nat_col: "categoria_nacionalitat"}
    )

    df_master = pd.merge(
        df_income, 
        df_rent, 
        on=["territori", "any"],
        how="outer"
    )

    df_master = pd.merge(
        df_master, 
        df_pop, 
        on=["territori", "any"], 
        how="left"
    )

    df_nat_wide = (
        df_nat
        .pivot_table(
            index=["territori", "any"],
            columns="categoria_nacionalitat",
            values="poblacio",
            aggfunc="sum"
        )
        .reset_index()
    )

    df_master = pd.merge(
        df_master, 
        df_nat_wide, 
        on=["territori", "any"], 
        how="left"
    )

    df_master["territori_id"] = (
        df_master["territori"]
        .astype("category")
        .cat.codes
    )

    return df_master

