import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString
from shapely.geometry.polygon import Polygon
from shapely import wkt
import folium

# CONSTANTS (Define your target and the buffer zone)
CRISTO_RENDOTOR_TARGET = (-43.21052677661779, -22.95183796600185)  # Longitude, Latitude
BUFFER_CLIP = 0.01  # Buffer zone in degrees (buffer size)

# Calculate the limits of the buffer zone
MIN_LONG = CRISTO_RENDOTOR_TARGET[0] - BUFFER_CLIP
MAX_LONG = CRISTO_RENDOTOR_TARGET[0] + BUFFER_CLIP
MIN_LAT = CRISTO_RENDOTOR_TARGET[1] - BUFFER_CLIP
MAX_LAT = CRISTO_RENDOTOR_TARGET[1] + BUFFER_CLIP

FILE = "009_buildings.csv"


def explore_data(data):
    """
    Loads and explores data from the CSV file.

    Parameters:
    data (str): The file path of the CSV file to load.

    Returns:
    pd.DataFrame: The loaded dataframe containing building data.
    """
    building_data_complete = pd.read_csv(data)
    print(
        building_data_complete.shape
    )  # Print the shape of the dataframe (rows, columns)
    building_data_complete.head()  # Show the first few rows
    return building_data_complete


def filtering_data(data):
    """
    Filters data to keep only the records within the buffer zone.

    Parameters:
    data (pd.DataFrame): The dataframe to filter.

    Returns:
    pd.DataFrame: A filtered dataframe with data inside the buffer zone.
    """
    filtered_df = data[
        (data["latitude"] >= MIN_LAT)
        & (data["latitude"] <= MAX_LAT)
        & (data["longitude"] >= MIN_LONG)
        & (data["longitude"] <= MAX_LONG)
    ]
    return filtered_df


def create_gdf(input_layer):
    """
    Creates a GeoDataFrame from a geometry object.

    Parameters:
    input_layer (shapely.geometry): The geometry object to convert into a GeoDataFrame.

    Returns:
    gpd.GeoDataFrame: The resulting GeoDataFrame.
    """
    return gpd.GeoDataFrame({"geometry": [input_layer]}, crs="EPSG:4326")  # WGS84


def create_geometries(filtered_df):
    """
    Converts WKT geometries into Shapely objects.

    Parameters:
    filtered_df (pd.DataFrame): The dataframe with WKT geometries to convert.

    Returns:
    pd.DataFrame: The dataframe with converted Shapely geometries.
    """
    filtered_df["geometry"] = filtered_df["geometry"].apply(wkt.loads)
    return filtered_df


def generate_map_with_buffer(filtered_df, target_point, buffer_rect):
    """
    Generates a Folium map with the filtered buildings and the buffer zone.

    Parameters:
    filtered_df (pd.DataFrame): The dataframe with filtered building data.
    target_point (shapely.geometry.Point): The target point (Cristo Redentor).
    buffer_rect (shapely.geometry.Polygon): The buffer zone polygon.

    Returns:
    folium.Map: The generated Folium map.
    """
    map_center = [target_point.y, target_point.x]  # Latitude, Longitude
    m = folium.Map(location=map_center, zoom_start=15)

    # Add the target location to the map
    folium.Marker(
        location=[target_point.y, target_point.x],
        popup="Cristo Redentor",
        icon=folium.Icon(color="red", icon="star"),
    ).add_to(m)

    # Add the buffer zone (rectangle) to the map
    folium.Polygon(
        locations=[(point[1], point[0]) for point in buffer_rect.exterior.coords],
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.3,
        popup="Buffer Zone",
    ).add_to(m)

    # Add the filtered buildings to the map
    for idx, row in filtered_df.iterrows():
        if isinstance(row["geometry"], Polygon):
            polygon_coords = [
                (point[1], point[0]) for point in row["geometry"].exterior.coords
            ]
            folium.Polygon(
                locations=polygon_coords,  # Polygon coordinates (Lat, Lon)
                color="blue",
                fill=True,
                fill_color="black",
                fill_opacity=0.3,
                popup=f"Building ID: {row.name}",  # Use index as the building ID
            ).add_to(m)

    return m


def add_closest_building_to_map(m, filtered_df, closest_id, closest_building_metres):
    """
    Adds the closest building to the map, including a marker, polygon, and a line to the target.

    Parameters:
    m (folium.Map): The folium map object to which the elements will be added.
    filtered_df (pd.DataFrame): The dataframe with filtered building data.
    closest_id (int): The index of the closest building in the dataframe.
    closest_building_metres (pd.Series): The row from the dataframe representing the closest building's data, including the distance to the target.

    Returns:
    folium.Map: The updated folium map with the closest building information added.
    """
    # Add Marker for the closest building
    folium.Marker(
        location=[closest_building_metres.latitude, closest_building_metres.longitude],
        popup="Closest Building",
        icon=folium.Icon(color="blue", icon="info-sign"),
    ).add_to(m)

    # Get the closest building geometry and create the polygon
    closest_building = filtered_df.loc[closest_id]  # WGS84
    polygon_coords = [
        (point[1], point[0]) for point in closest_building["geometry"].exterior.coords
    ]  # WGS84

    # Add closest building polygon to the map
    folium.Polygon(
        locations=polygon_coords,
        color="black",
        fill=True,
        fill_color="blue",
    ).add_to(m)

    # Create line between closest building and the target
    line = LineString(
        [
            (CRISTO_RENDOTOR_TARGET[1], CRISTO_RENDOTOR_TARGET[0]),
            (closest_building_metres.latitude, closest_building_metres.longitude),
        ]
    )

    # Add the line to the map
    folium.PolyLine(
        locations=[(point[0], point[1]) for point in line.coords],
        color="green",
        weight=2.5,
        opacity=0.8,
        popup=f"Distance: {closest_building_metres['distance_to_target_meters']:.2f} m",
    ).add_to(m)

    return m


def main():
    """
    The main function to load data, process it, and visualize it on a map.
    """
    # Load the dataset
    building_data_complete = explore_data(FILE)

    # Create a rectangular buffer around the target location
    buffer_rect = Polygon(
        [
            (MIN_LONG, MIN_LAT),
            (MIN_LONG, MAX_LAT),
            (MAX_LONG, MAX_LAT),
            (MAX_LONG, MIN_LAT),
        ]
    )
    buffer_gdf = create_gdf(buffer_rect)

    # Filter the data within the buffer zone
    filtered_df = filtering_data(building_data_complete)

    # Create geometries for the filtered data
    filtered_df = create_geometries(filtered_df)

    # Create a GeoDataFrame for the target (Cristo Redentor)
    target_point = Point(CRISTO_RENDOTOR_TARGET[0], CRISTO_RENDOTOR_TARGET[1])
    target_gdf = create_gdf(target_point)

    # Calculate the distances to the target in geographic coordinates
    filtered_df["distance_to_target_geo"] = filtered_df["geometry"].apply(
        lambda geom: geom.distance(target_point)
    )

    # Convert filtered_df to GeoDataFrame and reproject to EPSG:31983
    filtered_gdf = gpd.GeoDataFrame(filtered_df, geometry="geometry")
    filtered_gdf = filtered_gdf.set_crs("EPSG:4326").to_crs(epsg=31983)
    target_gdf = target_gdf.to_crs(epsg=31983)

    # Calculate the distance in meters
    filtered_gdf["distance_to_target_meters"] = filtered_gdf.geometry.distance(
        target_gdf.geometry[0]
    )

    # Determine the closest building
    closest_id = filtered_gdf["distance_to_target_meters"].idxmin()
    closest_building_metres = filtered_gdf.loc[closest_id]

    # Print the closest building information
    print(f"Closest building ID: {closest_id}")
    print(
        f"Distance to closest building: {closest_building_metres['distance_to_target_meters']} meters"
    )

    # Generate and save the map with the buffer zone
    m = generate_map_with_buffer(filtered_gdf, target_point, buffer_rect)
    m.save("filtered_map.html")  # Save the map as an HTML file

    # Add the closest building to the map
    m2 = add_closest_building_to_map(
        m, closest_building_metres, target_point, CRISTO_RENDOTOR_TARGET
    )
    m2.save("final_map.html")  # Save the map as an HTML file
    print("Map saved as 'filtered_map.html'")


# Run the script if this is the main module
if __name__ == "__main__":
    main()
