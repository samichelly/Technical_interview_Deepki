import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
from shapely import wkt


def explore_data(file_path):
    """
    Loads and explores data from the CSV file.

    Parameters:
    file_path (str): Path to the CSV file.

    Returns:
    pd.DataFrame: Loaded dataframe.
    """
    data = pd.read_csv(file_path)
    print(f"Data shape: {data.shape}")
    print(data.head())
    return data


def create_buffer_clip(min_long, max_long, min_lat, max_lat):
    """
    Creates a rectangular buffer as a Polygon.

    Parameters:
    min_long (float): Minimum longitude.
    max_long (float): Maximum longitude.
    min_lat (float): Minimum latitude.
    max_lat (float): Maximum latitude.

    Returns:
    shapely.geometry.Polygon: A polygon representing the rectangular buffer zone.
    """
    buffer_rect = Polygon(
        [
            (min_long, min_lat),
            (min_long, max_lat),
            (max_long, max_lat),
            (max_long, min_lat),
        ]
    )
    return buffer_rect


def filtering_data(data, min_long, max_long, min_lat, max_lat):
    """
    Filters data to keep only records within the buffer zone.

    Parameters:
    data (pd.DataFrame): Original dataframe.

    Returns:
    pd.DataFrame: Filtered dataframe.
    """

    print("dans data filter ", min_long, max_long, min_lat, max_lat)
    return data[
        (data["latitude"] > min_lat)
        & (data["latitude"] < max_lat)
        & (data["longitude"] > min_long)
        & (data["longitude"] < max_long)
    ]


def create_gdf(input_layer):
    """
    Creates a GeoDataFrame from a geometry object.

    Parameters:
    input_layer (shapely.geometry): Geometry object.

    Returns:
    gpd.GeoDataFrame: GeoDataFrame.
    """
    return gpd.GeoDataFrame({"geometry": [input_layer]}, crs="EPSG:4326")


def create_geometries(filtered_df):
    """
    Converts WKT geometries to Shapely objects.

    Parameters:
    filtered_df (pd.DataFrame): Dataframe with WKT geometries.

    Returns:
    pd.DataFrame: Dataframe with converted geometries.
    """
    filtered_df["geometry"] = filtered_df["geometry"].apply(wkt.loads)
    return filtered_df


def reproject_data(data_gdf, target_crs):
    """
    Reprojects a GeoDataFrame to the specified CRS.

    Parameters:
    data_gdf (gpd.GeoDataFrame): The GeoDataFrame to reproject.
    target_crs (int or str): The target coordinate reference system (e.g., "EPSG:31983").

    Returns:
    gpd.GeoDataFrame: The reprojected GeoDataFrame.
    """
    return data_gdf.to_crs(epsg=target_crs)
