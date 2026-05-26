# =====================================================
# src/visualization/maps.py
# Funcions cartogràfiques Folium
# =====================================================

# =====================================================
# Imports
# =====================================================

import folium
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from folium.features import GeoJsonTooltip


# =====================================================
# FUNCIÓ PRINCIPAL
# =====================================================

def make_map(
    df,
    any_,
    variable="indicador_gentrificacio",
    variable_label="Indicador",
):
    """
    Genera un mapa Folium per un any concret.
    """

    # =================================================
    # Filtrar any
    # =================================================

    df_year = df[
        df["any"] == any_
    ].copy()

    # =================================================
    # Conversió numèrica
    # =================================================

    df_year[variable] = pd.to_numeric(
        df_year[variable],
        errors="coerce",
    )

    # =================================================
    # Escala de colors
    # =================================================

    vmin = df_year[variable].min()
    vmax = df_year[variable].max()

    # =================================================
    # Crear mapa
    # =================================================

    m = folium.Map(
        location=[41.385, 2.17],
        zoom_start=12,
        tiles="CartoDB positron",
    )

    # =================================================
    # Funció colors
    # =================================================

    def get_color(value):

        if pd.isna(value):
            return "#cccccc"

        if vmax == vmin:
            return "#999999"

        norm = (
            (value - vmin)
            / (vmax - vmin)
        )

        return mcolors.to_hex(
            plt.cm.RdYlBu_r(norm)
        )

    # =================================================
    # GeoJSON layer
    # =================================================

    folium.GeoJson(
        df_year,
        style_function=lambda x: {
            "fillColor": get_color(
                x["properties"][variable]
            ),
            "color": "black",
            "weight": 0.5,
            "fillOpacity": 0.75,
        },
        tooltip=GeoJsonTooltip(
            fields=[
                "NOM",
                variable,
                "cluster",
            ],
            aliases=[
                "Barri",
                variable_label,
                "Cluster",
            ],
            localize=True,
        )
    ).add_to(m)

    # =================================================
    # Llegenda
    # =================================================

    legend_html = f"""
    <div style="
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 220px;
        background-color: white;
        border:2px solid grey;
        z-index:9999;
        font-size:14px;
        padding: 10px;
    ">

        <b>{variable_label}</b><br>

        <div style="
            height: 20px;
            background: linear-gradient(
                to right,
                #4575b4,
                #91bfdb,
                #fc8d59,
                #d73027
            );
            margin-top: 8px;
            margin-bottom: 8px;
        "></div>

        <span style="float:left;">
            {vmin:.2f}
        </span>

        <span style="float:right;">
            {vmax:.2f}
        </span>

    </div>
    """

    m.get_root().html.add_child(
        folium.Element(legend_html)
    )

    return m