import geopandas as gpd
import matplotlib.pyplot as plt
import logging
from tabulate import tabulate
from matplotlib_scalebar.scalebar import ScaleBar

logging.basicConfig(level=logging.INFO)
PROVINCE_FILE="data1/provinces.geojson"
PARK_FILE="data1/protected_zones.geojson"

provinces=gpd.read_file(PROVINCE_FILE)
park=gpd.read_file(PARK_FILE)
park=park.to_crs(provinces.crs)
logging.info("Data loaded")
# Association of each park with its province using a spatial join
def spatialjoin(park,provinces):
    park_province=gpd.sjoin(
    park,
    provinces,
    how="left",
    predicate="intersects"
    )
    logging.info("Spatial join performed (intersects)")
    # Display the name of each park and its province (park_province.columns)
    logging.info(" each park and its province")
    logging.info(
        "\n%s",
        tabulate(
            park_province[["NOM_left", "NOM_right"]],
            headers=["PARK", "PROVINCE"],
            tablefmt="grid",
            showindex=False
        ))
    #Identify parks spanning multiple provinces|Parks spanning more than two provinces
    park_multi_provinces = (
    park_province
    .groupby("NOM_left")
    .agg(
        COUNT_PROVINCES=("NOM_right", "nunique"),
        PROVINCES=("NOM_right", lambda x: ", ".join(sorted(x.unique())))
    ).reset_index())
    park_multi_provinces = park_multi_provinces[
        park_multi_provinces["COUNT_PROVINCES"] > 1
    ]
    logging.info("\n--- Identify parks spanning multiple provinces ---")
    logging.info(
        "\n%s",
        tabulate(
            park_multi_provinces,
            headers=["PARK", "COUNT_PROVINCES", "PROVINCES"],
            tablefmt="grid",
            showindex=False
        ))
    # Visualization of parks spanning more than two provinces
    park_visu=park[
        park["NOM"].isin(
        park_multi_provinces["NOM_left"]
    )
    ]
    fig, ax = plt.subplots(figsize=(10, 10))
    provinces.plot(ax=ax, color="lightgrey", edgecolor="black")
    park_visu.plot(ax=ax, column="NOM", legend=True)
    leg = ax.get_legend()
    leg.set_bbox_to_anchor((1.02, 1))
    leg.set_loc("upper left")
    plt.title("Parks extending across more than two provinces")
    plt.tight_layout()
    plt.show()
    # Parks entirely contained within a province
    park_within_prov=gpd.sjoin(
        park,
        provinces,
        how="inner",
        predicate="within"
    )
    logging.info("Parks entirely contained within a province")
    logging.info(
        "\n%s",
        tabulate(
            park_within_prov[["NOM_left", "NOM_right"]],
            headers=["PARK", "PROVINCE"],
            tablefmt="grid",
            showindex=False
        ))
    fig, ax = plt.subplots(figsize=(10, 10))
    provinces.plot(ax=ax, color="white", edgecolor="black")
    park_within_prov.plot(ax=ax, color="green")
    for idx, row in park_within_prov.iterrows():
        # **Centroid to place the text at the center of the park**
        x, y = row.geometry.centroid.x, row.geometry.centroid.y
        ax.text(
            x, y, 
            row["NOM_left"],
            fontsize=9, 
            ha="center", 
            va="center", 
            color="black",
            bbox=dict(facecolor="white", alpha=0.5, edgecolor="none", pad=1)
        )
    plt.title("Parks entirely contained within a province")
    plt.show()
    # Number of parks per province

    nb_parcs_province = (
        park_province
        .groupby("NOM_right")
        .agg(
            COUNT_PARKS=("NOM_left", "nunique"),
           PARKS=("NOM_left", lambda x: "\n".join(sorted(x.unique())))
        ).reset_index())

    logging.info("Number of parks per province")
    logging.info(
        "\n%s",
        tabulate(
            nb_parcs_province,
            headers=["PROVINCE", "COUNT_PARK"],
            tablefmt="grid",
            showindex=False
        ))
    # Graphic
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(
        nb_parcs_province["NOM_right"],
        nb_parcs_province["COUNT_PARKS"]
    )

    ax.set_title("Number of parks per province")
    ax.set_xlabel("Province")
    ax.set_ylabel("Number of parks")

    # Rotation pour lisibilité
    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    plt.show()
    # Provinces without a national park ((~) not all provinces whith parc)
    provinces_without_park = provinces[
        ~provinces["NOM"].isin(
            nb_parcs_province["NOM_right"]
        )
    ]
    logging.info("--- Provinces without a national park---")
    logging.info(
        "\n%s",
        tabulate(
            provinces_without_park[["NOM"]],
            headers=["NOM"],
            tablefmt="grid",
            showindex=False
        ))
    # Area of each park by province

    # Area calculation (in km²)
    park_province["surface_km2"] = (
        park_province.geometry.area / 1_000_000
    )

    surface_parc_province = (
        park_province
        .groupby(["NOM_left", "NOM_right"])
        ["surface_km2"]
        .sum()
        .reset_index()
    )
    logging.info("Area of each park by province")
    logging.info(
        "\n%s",
        tabulate(
            surface_parc_province,
            headers=["DESIGNATION","PROVINCE","SUPERFICE"],
            tablefmt="grid",
            showindex=False
        ))
    fig, ax = plt.subplots(figsize=(12, 12))

    provinces.plot(ax=ax, color="lightgrey", edgecolor="black")
    park_within_prov.plot(ax=ax, color="green", label="Parcs contenus")
    parcs_multi_geom = park[
        park["NOM"].isin(
            park_multi_provinces["NOM_left"]
        )
    ]
    parcs_multi_geom.plot(ax=ax, color="red", label="Parcs multi-provinces")

    plt.legend()
    plt.title("Parcs nationaux et provinces de la RDC")
    plt.show()
spatialjoin(park,provinces)


