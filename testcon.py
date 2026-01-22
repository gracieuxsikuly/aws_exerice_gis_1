from db import get_connection
import geopandas as gpd
import psycopg2
from psycopg2.extras import execute_values
mon_fichier="data/routes.geojson"
table_name="roads"
try:
    con=get_connection()
    cur=con.cursor()
#    mon code pour insertion dans la base de donnee
    gdf=gpd.read_file(mon_fichier)
    print(gdf.crs)
    srid=gdf.crs
    # creation de ma table
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name}(
        id SERIAL PRIMARY KEY,
        geometry geometry({gdf.geom_type[0]},{srid})
        );
    """)
    # insertion de mes donnes depuis le fichier
    records=[
       (row.geometry.wkt,) 
       for _, row in gdf.iterrows()
    ]
    execute_values(
        cur,
        f"""
            INSERT INTO {table_name} (geometry)
            VALUES (ST_GeomFromText(%s,{srid}))
        """,
        records
    )
    cur.close()
    con.close()
except Exception as e:
    print("Erreur de connexion:",e)
