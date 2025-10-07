import re
import pandas as pd
from src.Helper import find_new_level

def extract_iteration_results_dset(sld_string, time, ground_level, loads_table):
    """
    Extract settlement results from SLD file content at a specific time.
    
    Args:
        sld_string (str): Content of the SLD file as a string
        time (float): Time in days to extract results for
        
    Returns:
        dict: Dictionary with settlement and effective vertical stress values
        
    Example:
        For time=100000 days, returns {'settlement': -0.45, 'effective_vertical_stress': 0.696}
    """
    results = {}
    
    # Split the content into lines
    lines = sld_string.strip().split('\n')
    
    # Find all tables that start with [Vertical Data at Time]
    tables = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for table headers
        if line.startswith('[Vertical Data at Time'):
            # Next line should contain the time
            if i + 1 < len(lines):
                time_line = lines[i + 1].strip()
                
                # Extract time value (format: <Number> = Time in days)
                time_match = re.match(r'^(\d+\.?\d*)\s*=.*', time_line)
                if time_match:
                    table_time = float(time_match.group(1))
                    
                    # Find the start of data (skip header lines)
                    data_start = i + 2
                    while data_start < len(lines) and not re.match(r'^\s*-?\d+\.?\d*', lines[data_start].strip()):
                        data_start += 1
                    
                    # Find the end of this table (next [Vertical Data at Time] or end of file)
                    data_end = data_start
                    while data_end < len(lines):
                        if lines[data_end].strip().startswith('[Vertical Data at Time'):
                            break
                        data_end += 1
                    
                    # Extract the first data line (first settlement and effective vertical stress values)
                    first_effective_vertical_stress = None
                    first_settlement = None
                    
                    for j in range(data_start, data_end):
                        data_line = lines[j].strip()
                        if data_line and re.match(r'^\s*-?\d+\.?\d*', data_line):
                            parts = data_line.split()
                            if len(parts) >= 2:
                                try:
                                    first_settlement = round(float(parts[0]), 3)  # Settlement value, rounded to 3 decimals
                                    first_effective_vertical_stress = round(float(parts[1]), 3)  # Effective vertical stress, rounded to 3 decimals
                                    break
                                except ValueError:
                                    continue
                    
                    if first_effective_vertical_stress is not None and first_settlement is not None:
                        tables.append({
                            'time': round(table_time, 3),
                            'settlement': first_settlement,
                            'effective_vertical_stress': first_effective_vertical_stress
                        })
                    
                    i = data_end - 1  # Skip to end of current table
        
        i += 1
    
    # Find the table with time closest to the requested time
    if tables:
        closest_table = min(tables, key=lambda x: abs(x['time'] - time))
        closest_table_9m = min(tables, key=lambda x: abs(x['time'] - 270))  # 9 months in days
        closest_table_60y = min(tables, key=lambda x: abs(x['time'] - 21900))  # 60 years in days
        closest_table_end = min(tables, key=lambda x: abs(x['time'] - 21900))  # End of simulation
        results = {
            'ground_level': ground_level,
            'zetting na 9 maanden': closest_table_9m['settlement'],
            'new_level': round(find_new_level(ground_level, loads_table, settlement=closest_table['settlement']),2),
            'effective_vertical_stress': closest_table['effective_vertical_stress'],
            'time_found': closest_table['time'],
            'restzetting (60 years-9 months)': round(closest_table_60y['settlement'] - closest_table_9m['settlement'], 2),
            'eindzetting': round(closest_table_end['settlement'], 2)
        }
    
    return results

def debug_sld_parsing(sld_string, num_lines=50):
    """
    Debug function to help understand the SLD file structure.
    Returns the first few lines of the file for inspection and table info.
    """
    lines = sld_string.strip().split('\n')
    
    # Find table headers for debugging
    table_info = []
    for i, line in enumerate(lines):
        if line.strip().startswith('[Vertical Data at Time'):
            if i + 1 < len(lines):
                time_line = lines[i + 1].strip()
                table_info.append(f"Line {i}: {line.strip()}")
                table_info.append(f"Line {i+1}: {time_line}")
    
    return {
        'first_lines': lines[:num_lines],
        'table_headers': table_info
    }