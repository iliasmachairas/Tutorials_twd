from fastapi import FastAPI
from databases import Database
from geojson import Feature, FeatureCollection, dumps
from fastapi.middleware.cors import CORSMiddleware
import json  # Import json module

DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

database = Database(DATABASE_URL)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/polygons")
async def get_polygons():
    query = """
    SELECT 
        id,
        ST_AsGeoJSON(geom) AS geom_geojson,
        crop
    FROM 
        draft_ilias.parcels;
    """
    rows = await database.fetch_all(query)
    print("hello world")
    print(rows)

    # Create GeoJSON Features
    features = [
        Feature(
            id=row["id"],
            geometry=json.loads(row["geom_geojson"]),  # Parse the GeoJSON string into a dictionary
            properties={"crop": row["crop"]}  # Fix the key here for the 'crop' property
        )
        for row in rows
    ]

    # Return FeatureCollection
    return dumps(FeatureCollection(features))
