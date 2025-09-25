import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from io import StringIO
import plotly.graph_objects as go
from plotly.subplots import make_subplots 
from src.Dsettl import create_Dset_geometry
from src.Helper import rd_to_wgs84, calculate_zoom_level
from src.Helper import create_list_of_points

def create_geo_profile_and_map(df_loc, df_bh, Location_id, coord_system, material_table):
     # Create subplots: 1 row, 2 columns - CORRECTED ORDER
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Location Map', 'Geological Profile'),  # Map first, geo profile second
        specs=[[{"type": "mapbox"}, {"type": "scatter"}]],  # Mapbox first, scatter second
        column_widths=[0.8, 0.2]  # Adjust width ratio
    )

    # Add location map to FIRST subplot (col=1)
    if df_loc is not None:
        if coord_system == "Rijksdriehoek":
            df_loc['lat'] = df_loc.apply(lambda row: rd_to_wgs84(row['Easting'], row['Northing'])[0], axis=1)
            df_loc['lon'] = df_loc.apply(lambda row: rd_to_wgs84(row['Easting'], row['Northing'])[1], axis=1)
        elif coord_system == "wgs84":
            df_loc['lat'] = df_loc['Northing']
            df_loc['lon'] = df_loc['Easting']

        # Define selected_location ONCE at the beginning
        selected_location = None
        if df_loc is not None and Location_id is not None:
            selected_location = df_loc[df_loc['Location ID'] == Location_id]

        # Add all locations to map (FIRST subplot)
        fig.add_trace(go.Scattermapbox(
            lat=df_loc['lat'],
            lon=df_loc['lon'],
            mode='markers',
            marker=dict(
                size=8,
                color='blue',
                symbol='circle'
            ),
            text=df_loc['Location ID'],
            name='All Locations',
            showlegend=True
        ), row=1, col=1)  # FIRST subplot
        
        # Highlight selected location if available
        if selected_location is not None and not selected_location.empty:
            fig.add_trace(go.Scattermapbox(
                lat=selected_location['lat'],
                lon=selected_location['lon'],
                mode='markers',
                marker=dict(
                    size=12,
                    color='red',
                    symbol='circle'
                ),
                name=f'Selected: {Location_id}',
                showlegend=True
            ), row=1, col=1)  # FIRST subplot

    # Add geological profile to SECOND subplot (col=2)
    if (df_bh is not None and Location_id is not None and selected_location is not None and not selected_location.empty):
        filtered_df_bh = df_bh[df_bh['Location ID'] == Location_id]
        groundlevel = selected_location['Ground Level'].iloc[0]
        
        if not filtered_df_bh.empty:
            materials, depth_tops, depth_bases, colors, names, thicknesses = create_Dset_geometry(filtered_df_bh, groundlevel, material_table)

            # Add geological traces to SECOND subplot
            for i in range(len(materials)):
                fig.add_trace(go.Scatter(
                    x=[0.2, 0.4, 0.4, 0.2, 0.2],
                    y=[depth_tops[i], depth_tops[i], depth_bases[i], depth_bases[i], depth_tops[i]],
                    fill='toself',
                    fillcolor=colors[i],
                    line=dict(color='black', width=1),
                    name=f'{names[i]} ({thicknesses[i]}m)',
                    mode='lines',
                    showlegend=True
                ), row=1, col=2)  # SECOND subplot

        fig.update_yaxes(title_text="Depth (m)", row=1, col=2)
        fig.update_xaxes(visible=False, row=1, col=2)

    # Update layout with mapbox configuration
    if df_loc is not None:
        fig.update_layout(
            mapbox=dict(  # Since mapbox is now the FIRST subplot, use 'mapbox'
                style="open-street-map",
                center=dict(
                    lat=df_loc['lat'].mean(),
                    lon=df_loc['lon'].mean()
                ),
                zoom=calculate_zoom_level(df_loc['lat'], df_loc['lon']) + 1.6 # Slightly increased zoom
            )
        )

    return fig


def create_heatmap(df, values, names, point_size, toggle_annotations):

    # Use the existing function to convert coordinates
    points = create_list_of_points(df)
    
    # Extract X, Y coordinates and values from the dataframe
    X_array = np.array(df['Easting'].values)  # latitudes
    Y_array = np.array(df['Northing'].values)  # longitudes
    Value_array = np.array(values)
    names = np.array(names)

    # Add padding to extend the grid beyond the data points
    x_range = max(X_array) - min(X_array)
    y_range = max(Y_array) - min(Y_array)
    padding_x = x_range * 0.1
    padding_y = y_range * 0.1

    # Create coordinate grids with padding
    xcoords = np.linspace(min(X_array) - padding_x, max(X_array) + padding_x, 120)
    ycoords = np.linspace(min(Y_array) - padding_y, max(Y_array) + padding_y, 120)
    xi, yi = np.meshgrid(xcoords, ycoords)
    
    # Use griddata for interpolation
    points_array = np.column_stack((X_array, Y_array))
    interpolated = griddata(points_array, Value_array, (xi, yi), method='linear')

    fig, ax = plt.subplots(figsize=(12, 8))

    # Set consistent colormap and normalization
    vmin, vmax = Value_array.min(), Value_array.max()

    # Create the heatmap using imshow with proper extent
    extent = [xcoords[0], xcoords[-1], ycoords[0], ycoords[-1]]
    im = ax.imshow(interpolated, extent=extent, 
                    origin='lower', interpolation='bicubic', alpha=0.8,
                    cmap='viridis', vmin=vmin, vmax=vmax)
    
    # Plot the original data points as scatter
    scatter = ax.scatter(X_array, Y_array, c=Value_array, s=point_size, edgecolor='black', linewidth=2, 
                        cmap='viridis', vmin=vmin, vmax=vmax, zorder=10)
    
    if toggle_annotations:
        # Add value annotations for each point
        for i, (x, y, val, name) in enumerate(zip(X_array, Y_array, Value_array, names)):
            ax.annotate(f'{name}\n{val:.2f}', (x, y), xytext=(5, 5), textcoords='offset points',
                        fontsize=6, fontweight='bold', color='white', 
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7))
    
    plt.colorbar(im, ax=ax)
    ax.set_title('Heatmap')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')

    svg_data = StringIO()
    fig.savefig(svg_data, format='svg', bbox_inches='tight')
    plt.close()

    svg_data.seek(0)

    return svg_data