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


def materials_to_dict(material_props):
    """
    Convert the material properties from Viktor input format into a dictionary of dictionaries
    suitable for geolib material creation
    """

    material_properties = {}
    for prop in material_props:
        material_name = prop['col_1']

        # Determine if material is drained (sand types are typically drained)
        is_drained = ('SAND' in material_name or 'Sand' in material_name)

        material_properties[material_name] = {
            "sat_weight": prop['col_3'],        # y_sat from col_3
            "unsat_weight": prop['col_2'],      # y_dry from col_2
            "cv": prop['col_8'],                # vertical consolidation coefficient
            "cr": prop['col_6'],                # compression ratio CR from col_6
            "rr": prop['col_5'],                # reloading ratio RR from col_5
            "ca": prop['col_7'],                # secondary compression Ca from col_7
            "is_drained": is_drained,           # determined based on material type
            "pop_layer": prop['col_9'],         # POP from col_9
        }

    return material_properties


def find_ground_level(df_loc, location_id):
    """
    Find the ground level for a specific location ID in the dataframe.
    Returns ground level for that location.
    """
    if (location_id is not None and df_loc is not None and not df_loc.empty):
        # Filter dataframe by location_id first, then get ground level
        filtered_df = df_loc[df_loc['Location ID'] == location_id]
        
        if not filtered_df.empty:
            ground_level = filtered_df['Ground Level'].iloc[0]
            return ground_level
        else:
            # Handle case where location_id is not found
            print(f"Warning: Location ID '{location_id}' not found in locations dataframe")
            return None
    
    return None


def find_filtered_df_bh(df_loc, df_bh, location_id):
    """
    Find the borehole data for a specific location name in the dataframe.
    Returns a dataframe with borehole data for that location.
    """
    if (df_bh is not None and location_id is not None and df_loc is not None and not df_loc.empty):
        filtered_df_bh = df_bh[df_bh['Location ID'] == location_id]
    
        return filtered_df_bh
