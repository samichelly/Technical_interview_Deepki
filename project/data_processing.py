import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
from shapely import wkt

# CONSTANTS
CRISTO_RENDOTOR_TARGET = (-43.21052677661779, -22.95183796600185)
BUFFER_CLIP = 0.01  # Buffer zone in degrees
MIN_LONG = CRISTO_RENDOTOR_TARGET[0] - BUFFER_CLIP
MAX_LONG = CRISTO_RENDOTOR_TARGET[0] + BUFFER_CLIP
MIN_LAT = CRISTO_RENDOTOR_TARGET[1] - BUFFER_CLIP
MAX_LAT = CRISTO_RENDOTOR_TARGET[1] + BUFFER_CLIP


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


def filtering_data(data):
    """
    Filters data to keep only records within the buffer zone.

    Parameters:
    data (pd.DataFrame): Original dataframe.

    Returns:
    pd.DataFrame: Filtered dataframe.
    """
    return data[
        (data["latitude"] >= MIN_LAT)
        & (data["latitude"] <= MAX_LAT)
        & (data["longitude"] >= MIN_LONG)
        & (data["longitude"] <= MAX_LONG)
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
