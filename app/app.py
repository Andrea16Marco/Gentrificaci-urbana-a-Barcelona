# =====================================================
# app/app.py
# Aplicació Streamlit — Gentrificació a Barcelona
# =====================================================

# ==================================================
# Configuració projecte
# ==================================================

import sys
from pathlib import Path

# Ruta absoluta del projecte
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Afegir-la al PATH
sys.path.append(str(PROJECT_ROOT))

# =====================================================
# Imports
# =====================================================

import geopandas as gpd
import pandas as pd
import streamlit as st

import os
import sys

from streamlit_folium import st_folium

# ==================================================
# Configuració projecte
# ==================================================

from src.config import (
    DATA_PROCESSED,
)

from src.utils_io import (
    load_csv,
)

from src.config import DATA_PROCESSED
from src.visualization.maps import make_map


# =====================================================
# CONFIGURACIÓ STREAMLIT
# =====================================================

st.set_page_config(
    page_title="Mapa de Gentrificació a Barcelona",
    page_icon="📍",
    layout="wide",
)


# =====================================================
# ESTILS
# =====================================================

st.markdown(
    """
    <style>

        .main {
            padding-top: 1rem;
        }

        .stSidebar {
            background-color: #f8f9fa;
        }

        h1, h2, h3 {
            color: #1f2937;
        }

    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# CÀRREGA DE DADES
# =====================================================

@st.cache_data
def load_data() -> gpd.GeoDataFrame:
    """
    Carrega el GeoDataFrame principal.
    """

    path = DATA_PROCESSED / "df_geo_final.geojson"

    gdf = gpd.read_file(path)

    numeric_columns = [
        "indicador_gentrificacio",
        "indicador_socio",
        "indicador_housing",
        "indicador_demo",
        "indicador_turisme",
    ]

    for col in numeric_columns:

        if col in gdf.columns:

            gdf[col] = pd.to_numeric(
                gdf[col],
                errors="coerce",
            )

    return gdf


# =====================================================
# DADES PRINCIPALS
# =====================================================

df_geo = load_data()

VARIABLE_LABELS = {
    "indicador_gentrificacio": "Indicador de gentrificació",
    "indicador_socio": "Dimensió socioeconòmica",
    "indicador_housing": "Dimensió habitatge",
    "indicador_demo": "Dimensió demogràfica",
    "indicador_turisme": "Dimensió turística",
}

ANYS = sorted(
    df_geo["any"]
    .dropna()
    .unique()
)


# =====================================================
# HEADER
# =====================================================

st.title("📍 Gentrificació urbana a Barcelona")

st.markdown(
    """
    Aplicació interactiva per visualitzar l’evolució dels
    indicadors de gentrificació als barris de Barcelona.

    Aquesta eina forma part del TFM sobre anàlisi urbana,
    machine learning i visualització geoespacial.
    """
)


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("Configuració")

mode = st.sidebar.radio(
    "Mode de visualització",
    [
        "Mapa d'un any",
        "Comparar dos anys",
    ],
)

variable = st.sidebar.selectbox(
    "Variable",
    options=list(VARIABLE_LABELS.keys()),
    format_func=lambda x: VARIABLE_LABELS[x],
)

st.sidebar.markdown("---")

st.sidebar.info(
    """
    Dataset longitudinal dels barris de Barcelona.

    Indicadors construïts a partir de:
    - renda
    - habitatge
    - demografia
    - turisme

    Clustering realitzat amb K-Means.
    """
)


# =====================================================
# MODE 1 — MAPA D'UN ANY
# =====================================================

if mode == "Mapa d'un any":

    any_selected = st.sidebar.slider(
        "Selecciona un any",
        min_value=int(min(ANYS)),
        max_value=int(max(ANYS)),
        value=int(max(ANYS)),
    )

    st.subheader(
        f"{VARIABLE_LABELS[variable]} — Any {any_selected}"
    )

    df_year = df_geo[
        df_geo["any"] == any_selected
    ]

    # =================================================
    # MÈTRIQUES
    # =================================================

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Barris",
        df_year["territori"].nunique()
    )

    col2.metric(
        "Mitjana",
        round(df_year[variable].mean(), 2)
    )

    col3.metric(
        "Màxim",
        round(df_year[variable].max(), 2)
    )

    # =================================================
    # MAPA
    # =================================================

    mapa = make_map(
        df=df_geo,
        any_=any_selected,
        variable=variable,
        variable_label=VARIABLE_LABELS[variable],
    )

    st_folium(
        mapa,
        width=1200,
        height=700,
    )


# =====================================================
# MODE 2 — COMPARACIÓ TEMPORAL
# =====================================================

else:

    col1, col2 = st.columns(2)

    with col1:

        any1 = st.selectbox(
            "Any inicial",
            ANYS,
            index=0,
        )

    with col2:

        any2 = st.selectbox(
            "Any final",
            ANYS,
            index=len(ANYS) - 1,
        )

    st.subheader(
        f"Comparació temporal — {any1} vs {any2}"
    )

    colA, colB = st.columns(2)

    # =================================================
    # MAPA ANY 1
    # =================================================

    with colA:

        st.markdown(f"### Any {any1}")

        mapa1 = make_map(
            df=df_geo,
            any_=any1,
            variable=variable,
            variable_label=VARIABLE_LABELS[variable],
        )

        st_folium(
            mapa1,
            width=600,
            height=600,
        )

    # =================================================
    # MAPA ANY 2
    # =================================================

    with colB:

        st.markdown(f"### Any {any2}")

        mapa2 = make_map(
            df=df_geo,
            any_=any2,
            variable=variable,
            variable_label=VARIABLE_LABELS[variable],
        )

        st_folium(
            mapa2,
            width=600,
            height=600,
        )


# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    """
    TFM — Gentrificació urbana a Barcelona

    Visualització geoespacial interactiva basada en:
    renda, habitatge, demografia i turisme.
    """
)
