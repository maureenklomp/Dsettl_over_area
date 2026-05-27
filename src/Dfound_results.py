import re
import pandas as pd

def extract_iteration_results(fod_string):
    """
    Extract data table from [FIXED RESULTS] section between [DATA] and [END OF DATA]
    """
    try:
        # First, find the [FIXED RESULTS] section
        fixed_results_start = fod_string.find('[FIXED RESULTS]')
        if fixed_results_start == -1:
            print("No [FIXED RESULTS] section found")
            return None
        
        # Find the end of [FIXED RESULTS] section
        fixed_results_end = fod_string.find('[END OF FIXED RESULTS]', fixed_results_start)
        if fixed_results_end == -1:
            print("No [END OF FIXED RESULTS] section found")
            return None
        
        # Extract only the FIXED RESULTS section
        fixed_results_section = fod_string[fixed_results_start:fixed_results_end + len('[END OF FIXED RESULTS]')]
        
        # Find [COLUMN INDICATION] within the FIXED RESULTS section
        column_start = fixed_results_section.find('[COLUMN INDICATION]')
        if column_start == -1:
            print("No [COLUMN INDICATION] section found in FIXED RESULTS")
            return extract_basic_data(fixed_results_section)  # Fallback to basic version
        
        # Find [END OF COLUMN INDICATION]
        column_end = fixed_results_section.find('[END OF COLUMN INDICATION]', column_start)
        if column_end == -1:
            print("No [END OF COLUMN INDICATION] section found")
            return extract_basic_data(fixed_results_section)  # Fallback to basic version
        
        # Extract column headers
        column_section = fixed_results_section[column_start + len('[COLUMN INDICATION]'):column_end].strip()
        column_lines = [line.strip() for line in column_section.split('\n') if line.strip()]
        
        # Parse column names - they appear to be listed one per line
        column_names = []
        for line in column_lines:
            if line and not line.startswith('['):
                column_names.append(line)
        
        # Find [DATA] after [END OF COLUMN INDICATION] within FIXED RESULTS
        data_start = fixed_results_section.find('[DATA]', column_end)
        if data_start == -1:
            print("No [DATA] section found in FIXED RESULTS")
            return None
        
        # Find [END OF DATA] within FIXED RESULTS
        data_end = fixed_results_section.find('[END OF DATA]', data_start)
        if data_end == -1:
            print("No [END OF DATA] section found in FIXED RESULTS")
            return None
        
        # Extract the data section
        data_section = fixed_results_section[data_start + len('[DATA]'):data_end].strip()
        
        # Split into lines and filter out empty ones
        lines = [line.strip() for line in data_section.split('\n') if line.strip()]
        
        if not lines:
            print("No data lines found")
            return None
        
        # Split by whitespace (appears to be space-separated, not tab-separated)
        data_rows = []
        for line in lines:
            # Split by any whitespace and handle quoted strings
            parts = []
            in_quotes = False
            current_part = ""
            
            i = 0
            while i < len(line):
                char = line[i]
                if char == "'" and not in_quotes:
                    in_quotes = True
                    current_part += char
                elif char == "'" and in_quotes:
                    in_quotes = False
                    current_part += char
                    parts.append(current_part.strip())
                    current_part = ""
                elif char.isspace() and not in_quotes:
                    if current_part.strip():
                        parts.append(current_part.strip())
                        current_part = ""
                else:
                    current_part += char
                i += 1
            
            # Add the last part if exists
            if current_part.strip():
                parts.append(current_part.strip())
            
            if parts:  # Only add rows with data
                data_rows.append(parts)
        
        if data_rows:
            # Determine number of columns from data
            max_cols = max(len(row) for row in data_rows)
            
            # Use extracted column names or create generic ones
            if len(column_names) == max_cols:
                final_column_names = column_names
            elif len(column_names) > 0:
                # Use what we have and pad with generic names
                final_column_names = column_names[:max_cols]
                while len(final_column_names) < max_cols:
                    final_column_names.append(f'Column_{len(final_column_names) + 1}')
            else:
                # Create all generic names
                final_column_names = [f'Column_{i+1}' for i in range(max_cols)]
            
            print(f"Found {len(data_rows)} rows with {max_cols} columns")
            print(f"Column names: {final_column_names}")
            
            # Pad rows to same length
            for row in data_rows:
                while len(row) < max_cols:
                    row.append('')
            
            df = pd.DataFrame(data_rows, columns=final_column_names)
            
            # Try to convert numeric columns (skip quoted string columns)
            for col in df.columns:
                try:
                    # Don't convert columns that contain quoted strings
                    if not df[col].astype(str).str.contains("'").any():
                        df[col] = pd.to_numeric(df[col])
                except:
                    pass
            
            return df
        
        return None
        
    except Exception as e:
        print(f"Error parsing fixed results: {e}")
        return None
    
def extract_basic_data(fixed_results_section):
    """
    Basic fallback method to extract data without column headers
    """
    try:
        # Find [DATA] within the section
        data_start = fixed_results_section.find('[DATA]')
        if data_start == -1:
            return None
        
        # Find [END OF DATA]
        data_end = fixed_results_section.find('[END OF DATA]', data_start)
        if data_end == -1:
            return None
        
        # Extract the data section
        data_section = fixed_results_section[data_start + len('[DATA]'):data_end].strip()
        
        # Split into lines and filter out empty ones
        lines = [line.strip() for line in data_section.split('\n') if line.strip()]
        
        if not lines:
            return None
        
        # Split by whitespace
        data_rows = []
        for line in lines:
            row = line.split()
            if row:  # Only add rows with data
                data_rows.append(row)
        
        if data_rows:
            # Create generic column names
            max_cols = max(len(row) for row in data_rows)
            column_names = [f'Column_{i+1}' for i in range(max_cols)]
            
            # Pad rows to same length
            for row in data_rows:
                while len(row) < max_cols:
                    row.append('')
            
            df = pd.DataFrame(data_rows, columns=column_names)
            
            # Try to convert to numeric
            for col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col])
                except:
                    pass
            
            return df
        
        return None
        
    except Exception as e:
        print(f"Error in basic data extraction: {e}")
        return None