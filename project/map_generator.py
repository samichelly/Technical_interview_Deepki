import folium
from shapely.geometry import Polygon, LineString


def generate_map_with_filtered_data(filtered_df, target_point, buffer_rect):
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
            ).add_to(m)

    return m


def add_closest_building_to_map(m, closest_building, target_coords):
    """
    Adds the closest building to the map, including a marker, polygon, and a line to the target.

    Parameters:
    m (folium.Map): The folium map object to which the elements will be added.
    closest_building (pd.Series): The row representing the closest building's data.
    target_point (shapely.geometry.Point): The target point (Cristo Redentor).
    target_coords (tuple): The coordinates of the target (lon, lat).

    Returns:
    folium.Map: The updated folium map with the closest building information added.
    """
    # Add Marker for the closest building
    folium.Marker(
        location=[closest_building.latitude, closest_building.longitude],
        popup="Closest Building",
        icon=folium.Icon(color="blue", icon="info-sign"),
    ).add_to(m)

    # Add the closest building polygon
    polygon_coords = [
        (point[1], point[0]) for point in closest_building["geometry"].exterior.coords
    ]
    folium.Polygon(
        locations=polygon_coords,
        color="black",
        fill=True,
        fill_color="blue",
    ).add_to(m)

    # Create a line between the closest building and the target
    line = LineString(
        [
            (target_coords[1], target_coords[0]),
            (closest_building.latitude, closest_building.longitude),
        ]
    )
    folium.PolyLine(
        locations=[(point[0], point[1]) for point in line.coords],
        color="green",
        weight=2.5,
        opacity=0.8,
        popup=f"Distance: {closest_building['distance_to_target_meters']:.2f} m",
    ).add_to(m)

    return m
