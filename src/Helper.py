from io import BytesIO
from pyproj import Transformer
import pandas as pd
import numpy as np
import math


def rd_to_wgs84(x_rd, y_rd):
        """
        Convert Dutch RD coordinates (EPSG:28992) to WGS84 lat/lon (EPSG:4326)
        Using pyproj for accurate transformation
        """
        # Create transformer from RD New (EPSG:28992) to WGS84 (EPSG:4326)
        transformer = Transformer.from_crs("EPSG:28992", "EPSG:4326", always_xy=True)
        lon, lat = transformer.transform(x_rd, y_rd)
        return lat, lon

def create_df(file_field):
        binary = file_field.file.getvalue_binary()
        df = pd.read_csv(BytesIO(binary))
        return df

def create_list_of_points(df):
    points = []
    for _, row in df.iterrows():
        x, y = rd_to_wgs84(row['Easting'], row['Northing'])
        points.append((x, y))
    return points

def calculate_zoom_level(lats, lons, padding=0.1):
    """
    Calculate appropriate zoom level to fit all points with some padding
    """
    lat_range = max(lats) - min(lats)
    lon_range = max(lons) - min(lons)
    
    # Add padding (10% by default)
    lat_range *= (1 + padding)
    lon_range *= (1 + padding)
    
    # Use the larger range to determine zoom
    max_range = max(lat_range, lon_range)
    
    # Rough zoom level calculation (adjust these values based on your needs)
    if max_range > 10:
        return 6
    elif max_range > 5:
        return 7
    elif max_range > 2:
        return 8
    elif max_range > 1:
        return 9
    elif max_range > 0.5:
        return 10
    elif max_range > 0.2:
        return 11
    elif max_range > 0.1:
        return 12
    else:
        return 13
    
def convert_color_string_to_tuple(color_string):
    """Convert color string like "255, 255, 0" to tuple (255, 255, 0)"""
    # Split the string by comma and convert each part to integer
    color_parts = color_string.split(", ")
    color_tuple = tuple(int(part.strip()) for part in color_parts)
    return color_tuple




