from data_processing import (
    explore_data,
    filtering_data,
    create_gdf,
    create_geometries,
    reproject_data,
)
from map_generator import generate_map_with_buffer, add_closest_building_to_map
from shapely.geometry import Point, Polygon
import geopandas as gpd


# CONSTANTS (Define your target and the buffer zone)
CRISTO_RENDOTOR_TARGET = (-43.21052677661779, -22.95183796600185)  # Longitude, Latitude
BUFFER_CLIP = 0.01  # Buffer zone in degrees (buffer size)

# Calculate the limits of the buffer zone
MIN_LONG = CRISTO_RENDOTOR_TARGET[0] - BUFFER_CLIP
MAX_LONG = CRISTO_RENDOTOR_TARGET[0] + BUFFER_CLIP
MIN_LAT = CRISTO_RENDOTOR_TARGET[1] - BUFFER_CLIP
MAX_LAT = CRISTO_RENDOTOR_TARGET[1] + BUFFER_CLIP

FILE = "009_buildings.csv"


def main():
    building_data_complete = explore_data(FILE)

    buffer_rect = Polygon(
        [
            (MIN_LONG, MIN_LAT),
            (MIN_LONG, MAX_LAT),
            (MAX_LONG, MAX_LAT),
            (MAX_LONG, MIN_LAT),
        ]
    )
    filtered_df = filtering_data(building_data_complete)
    filtered_df = create_geometries(filtered_df)

    # Create gdf
    target_point = Point(CRISTO_RENDOTOR_TARGET[0], CRISTO_RENDOTOR_TARGET[1])
    target_gdf = create_gdf(target_point)

    # Create gdf and reproject data
    filtered_gdf = gpd.GeoDataFrame(filtered_df, geometry="geometry").set_crs(
        "EPSG:4326"
    )
    filtered_gdf = reproject_data(filtered_gdf, 31983)
    target_gdf = reproject_data(target_gdf, 31983)

    filtered_gdf["distance_to_target_meters"] = filtered_gdf.geometry.distance(
        target_gdf.geometry[0]
    )

    # Find closest building
    closest_id = filtered_gdf["distance_to_target_meters"].idxmin()
    closest_building_metres = filtered_gdf.loc[closest_id]

    m = generate_map_with_buffer(filtered_gdf, target_point, buffer_rect)
    m = add_closest_building_to_map(
        m, closest_building_metres, target_point, CRISTO_RENDOTOR_TARGET
    )

    m.save("final_map.html")
    print("Map saved as 'final_map.html'")


if __name__ == "__main__":
    main()
