from download_and_extract import download_and_extract
from data_processing import (
    explore_data,
    filtering_data,
    reproject_data,
    create_buffer_clip,
)
from map_generator import generate_map_with_filtered_data, add_closest_building_to_map
from shapely import wkt
from shapely.geometry import Point
import geopandas as gpd
import os
from pathlib import Path


# CONSTANTS
CRISTO_RENDOTOR_TARGET = (-43.21052677661779, -22.95183796600185)  # Longitude, Latitude
OFFSET_CLIP = 0.01  # approximately +/- 1km

# Calculate the limits of the buffer zone
MIN_LONG = CRISTO_RENDOTOR_TARGET[0] - OFFSET_CLIP
MAX_LONG = CRISTO_RENDOTOR_TARGET[0] + OFFSET_CLIP
MIN_LAT = CRISTO_RENDOTOR_TARGET[1] - OFFSET_CLIP
MAX_LAT = CRISTO_RENDOTOR_TARGET[1] + OFFSET_CLIP

URL = "https://storage.googleapis.com/open-buildings-data/v3/polygons_s2_level_4_gzip/009_buildings.csv.gz"

GZIPPED_FILE_NAME = "009_buildings.csv.gz"
FILE = "009_buildings.csv"


parent_directory = Path(__file__).resolve().parent.parent
file_path = parent_directory / "009_buildings.csv"


def main():
    # Download and extract the file
    download_and_extract(URL, GZIPPED_FILE_NAME)

    # Check if the file was successfully downloaded and extracted
    if os.path.exists(FILE):
        print(f"File successfully downloaded and extracted to {FILE}")
    else:
        print(f"Error: {FILE} not found.")
    # Try to load the building data from the specified CSV file
    try:
        building_data_complete = explore_data(file_path)
    except FileNotFoundError:
        # Handle case if the file is not found
        print(f"Error: {FILE} not found.")
        return

    # Create a rectangular buffer around the target point (Cristo Redentor)
    buffer_rect = create_buffer_clip(MIN_LONG, MAX_LONG, MIN_LAT, MAX_LAT)

    # Filter the building data to keep only the buildings within the buffer zone
    filtered_df = filtering_data(
        building_data_complete, MIN_LONG, MAX_LONG, MIN_LAT, MAX_LAT
    )

    # Convert WKT geometries to Shapely geometries to GeoDataFrame with the specified CRS
    filtered_gdf = gpd.GeoDataFrame(
        filtered_df,
        geometry=filtered_df["geometry"].apply(
            wkt.loads
        ),  # Convert WKT to Shapely geometries
        crs="EPSG:4326",  # Directement définir le CRS
    )

    # Create a GeoDataFrame for the target point (Cristo Redentor)
    target_point = Point(CRISTO_RENDOTOR_TARGET[0], CRISTO_RENDOTOR_TARGET[1])
    target_gdf = gpd.GeoDataFrame({"geometry": [target_point]}, crs="EPSG:4326")

    # Generate a map with the filtered buildings and the buffer zone, centered around the target point
    m = generate_map_with_filtered_data(filtered_gdf, target_point, buffer_rect)
    m.save("data_filtered_map.html")

    # Reproject both the filtered buildings and the target to use meters unit
    filtered_gdf = reproject_data(filtered_gdf, 31983)
    target_gdf = reproject_data(target_gdf, 31983)

    # Calculate the distance of each building to the target point
    filtered_gdf["distance_to_target_meters"] = filtered_gdf.geometry.distance(
        target_gdf.geometry[0]
    )

    # Find the ID of the closest building by selecting the minimum distance to the target
    closest_id = filtered_gdf["distance_to_target_meters"].idxmin()
    closest_building_metres = filtered_gdf.loc[closest_id]
    print(closest_building_metres)

    # Generate a new map with the closest building added to the map and a line showing the distance to the target
    m2 = add_closest_building_to_map(m, closest_building_metres, CRISTO_RENDOTOR_TARGET)
    m2.save("closest_building_map.html")


if __name__ == "__main__":
    main()
