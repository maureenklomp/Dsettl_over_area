from tkinter.font import names
import viktor as vkt
import plotly.graph_objects as go
from plotly.subplots import make_subplots 
from viktor.views import PlotlyView, PlotlyResult
import pandas as pd
import numpy as np

from src.Helper import create_df, find_ground_level, find_filtered_df_bh
from src.Defaults import create_default_mat_prop, create_default_loads
from src.Dsettl import create_Dset_geometry, create_dsettlement_model, get_layers, add_table_loads, run_model
from src.Dsettl_results import extract_iteration_results_dset
from src.Visualizations import create_geo_profile_and_map, create_heatmap, create_settl_graphs, create_restsettl_scatter
from src.ASCII import get_train

from io import BytesIO, StringIO
import geolib as gl
from datetime import timedelta
import zipfile
from pathlib import Path

model_types = {'NEN_BJERRUM': gl.models.dsettlement.internal.SoilModel.NEN_BJERRUM, 'NEN_KOPPEJAN': gl.models.dsettlement.internal.SoilModel.NEN_KOPPEJAN, 'ISOTACHE': gl.models.dsettlement.internal.SoilModel.ISOTACHE}
cons_model_types = {"DARCY": gl.models.dsettlement.internal.ConsolidationModel.DARCY, "TERZAGHI": gl.models.dsettlement.internal.ConsolidationModel.TERZAGHI}

times = {'1 month': 1, '6 months': 6, '9 months': 9, '1 year': 12, '60 years': 720, '100 years': 1200}

def get_location_filter_list(params, **kwargs):
        """
        This function returns a list of location IDs that can be used as option input for the borehole data tab
        """
        # Get location data
        Locations_file = params.page_1.tab_2.file_field_1
        if Locations_file:
            df_loc = create_df(Locations_file)
            df_loc = df_loc.sort_values(by='Location ID')
            loc_id_list = df_loc["Location ID"].tolist()

            return loc_id_list
        
        else:
            return []  

_filter_list_vis = vkt.And(vkt.IsNotNone(vkt.Lookup('page_1.tab_2.file_field_1')),
                              vkt.IsNotNone(vkt.Lookup('page_1.tab_3.file_field_1')))



class Parametrization(vkt.Parametrization):
    page_1 = vkt.Page("Inputs and checking", views=["show_locations_csv"], width=50)
    
    # Model Properties tab
    page_1.tab_1 = vkt.Tab("Model properties", description="What are the modelling properties for this project?")
    page_1.tab_1.section_1 = vkt.Section("Model types", description="Types for calculation and consolidation")
    page_1.tab_1.section_1.autocomplete_field_1 = vkt.AutocompleteField("Settlement calculation method", options=list(model_types.keys()), default='NEN_BJERRUM')
    page_1.tab_1.section_1.option_field_1 = vkt.OptionField("Consoldiation Model", options=list(cons_model_types.keys()), default='DARCY', variant="radio")
    
    # Material Properties tab
    page_1.tab_1.section_2 = vkt.Section("Material properties")
    page_1.tab_1.section_2.table_1 = vkt.Table("Material properties and layers", default=create_default_mat_prop())

    page_1.tab_1.section_2.table_1.col_1 = vkt.TextField('Material Name')
    page_1.tab_1.section_2.table_1.col_2 = vkt.NumberField('Volum weight (unsat)')
    page_1.tab_1.section_2.table_1.col_3 = vkt.NumberField('Volum weight (sat)')
    page_1.tab_1.section_2.table_1.col_4 = vkt.TextField('Color')
    page_1.tab_1.section_2.table_1.col_5 = vkt.NumberField('RR')
    page_1.tab_1.section_2.table_1.col_6 = vkt.NumberField('CR')
    page_1.tab_1.section_2.table_1.col_7 = vkt.NumberField('Ca')
    page_1.tab_1.section_2.table_1.col_8 = vkt.NumberField('cv')
    page_1.tab_1.section_2.table_1.col_9 = vkt.NumberField('POP')
            

    
    # Locations tab
    page_1.tab_2 = vkt.Tab("Locations")
    page_1.tab_2.file_field_1 = vkt.FileField("Locations.csv", flex=100)
    page_1.tab_2.option_field_1 = vkt.OptionField("Coordinate system used", options=["wgs84", "Rijksdriehoek"], default="Rijksdriehoek", variant="radio-inline")
    
    # Borehole tab
    page_1.tab_3 = vkt.Tab("Borehole data")
    page_1.tab_3.file_field_1 = vkt.FileField("Field Geological Descriptions", flex=100, file_types=[".csv"])
    # page_1.tab_3.option_field_1 = vkt.OptionField("Location ID for preview", options=get_location_filter_list, visible=_filter_list_vis)
    

    # Geometry tab
    page_1.tab_4 = vkt.Tab("Ground Water Table")
    page_1.tab_4.number_field_1 = vkt.NumberField("Ground Water Table - relative to NAP")
    
    # Loads tab
    page_1.tab_5 = vkt.Tab("Loads")
    
    page_1.tab_5.section_1 = vkt.Section("Uniform Load", description="Input for uniform loads on the area")
    
    page_1.tab_5.section_1.table_1 = vkt.Table("Loads", default=create_default_loads())

    page_1.tab_5.section_1.table_1.col_1 = vkt.TextField('Name')
    page_1.tab_5.section_1.table_1.col_2 = vkt.NumberField('Time start [days]')
    page_1.tab_5.section_1.table_1.col_3 = vkt.NumberField('Load value [kPa]')
    page_1.tab_5.section_1.table_1.col_4 = vkt.NumberField('Load thickness [m]')


    page_2 = vkt.Page("Results per location", views=["show_borehole_csv", "get_combined_geo_profile_and_map", "plot_settl_graph"], width=20)
    page_2.section_1 = vkt.Section("Select location", description="Select a location to see the results for that specific location")
    page_2.section_1.option_field_1 = vkt.OptionField("Location ID for preview", options=get_location_filter_list, visible=_filter_list_vis, flex=100)
    page_2.section_1.boolean_field_1 = vkt.BooleanField("Logarithmic time axis", default=True, flex=100)
    page_2.section_2 = vkt.Section("Download model", description="Download the model files for this location")
    page_2.section_2.button = vkt.DownloadButton("Download model as zip", method = "download_zip", flex=100)




    page_3 = vkt.Page("Results for ALL locations", views=["plot_settl_results","plot_heatmap", "plot_scatter"], width=30)
    page_3.section_1 = vkt.Section("Selection of results", description="What results do you want to see?")
    page_3.section_1.option_field_1 = vkt.OptionField("Results to show on heatmap", options=["zetting na 9 maanden", "new ground level", "restzetting (60 years-9 months)", "eindzetting"], default="restzetting (60 years-9 months)", variant="radio-inline", flex=100)
    
    page_3.section_2 = vkt.Section("Visibility settings", description="Adjust the settings for the heatmap")
    page_3.section_2.number_field_1 = vkt.OptionField("Settlement at time:", options = list(times.keys()), flex=100)
    page_3.section_2.number_field_2 = vkt.NumberField("Adjust the point size on the heatmap", default=100, min=0, max=200, step=10, variant="slider", flex=100)
    page_3.section_2.is_true = vkt.BooleanField("Show annotations on heatmap", default=True, flex=100)
    
    page_3.section_3 = vkt.Section("Color intervals")
    page_3.section_3.interval_1_max = vkt.NumberField("Interval 1 Max Value", default=0.125, suffix="m", flex=100)
    page_3.section_3.interval_2_max = vkt.NumberField("Interval 2 Max Value", default=0.175, suffix="m", flex=100)
    page_3.section_3.interval_3_max = vkt.NumberField("Interval 3 Max Value", default=0.200, suffix="m", flex=100)

    page_3.section_4 = vkt.Section("Color Customization")
    page_3.section_4.color_1 = vkt.ColorField("Color Interval 1", default=vkt.Color(0,177,0), flex=100) #green
    page_3.section_4.color_2 = vkt.ColorField("Color Interval 2", default=vkt.Color(255,165,0), flex=100) #orange
    page_3.section_4.color_3 = vkt.ColorField("Color Interval 3", default=vkt.Color(255,0,0), flex=100) #red
    page_3.section_4.color_4 = vkt.ColorField("Color Interval 4", default=vkt.Color(205,0,18), flex=100) #darkred

    page_3.section_5 = vkt.Section("Upload previous settlement results", description="You can upload a previous settlement results .csv file ")
    page_3.section_5.file_field_1 = vkt.FileField("Upload previous settlement results (.csv)", flex=100, file_types=[".csv"])

class Controller(vkt.Controller):
    label = "My Entity Type"
    parametrization = Parametrization

    def input_csvs(self, params):
        # Get location data
        Locations_file = params.page_1.tab_2.file_field_1
        if Locations_file:
            df_locations = create_df(Locations_file)
            df_locations = df_locations.sort_values(by='Location ID')

        # Get borehole data
        Boreholes_file = params.page_1.tab_3.file_field_1
        if Boreholes_file:
            df_boreholes = create_df(Boreholes_file)

        return df_locations, df_boreholes
    

    def get_color_for_value(self, value, params):
        """Determine which color interval a value belongs to and return the corresponding color."""
        if value <= params.page_3.section_3.interval_1_max:
            return params.page_3.section_4.color_1.hex
        elif value <= params.page_3.section_3.interval_2_max:
            return params.page_3.section_4.color_2.hex
        elif value <= params.page_3.section_3.interval_3_max:
            return params.page_3.section_4.color_3.hex
        else:
            return params.page_3.section_4.color_4.hex

    def get_interval_label(self, value, params):
        """Get the interval label for a given value."""
        if value <= params.page_3.section_3.interval_1_max:
            return f"≤ {params.page_3.section_3.interval_1_max}"
        elif value <= params.page_3.section_3.interval_2_max:
            return f"{params.page_3.section_3.interval_1_max} - {params.page_3.section_3.interval_2_max}"
        elif value <= params.page_3.section_3.interval_3_max:
            return f"{params.page_3.section_3.interval_2_max} - {params.page_3.section_3.interval_3_max}"
        else:
            return f"> {params.page_3.section_3.interval_3_max}"

    

    @vkt.TableView("Locations.csv", duration_guess=1)
    def show_locations_csv(self, params, **kwargs):
        if params.page_1.tab_2.option_field_1 and params.page_1.tab_3.file_field_1:
            # Create dataframes for locations and boreholes
            df_loc = self.input_csvs(params)[0]
            
            # Define desired columns and check which ones exist
            desired_columns = ["Location ID", "Northing", "Easting", "Ground Level", "Final Depth"]
            available_columns = [col for col in desired_columns if col in df_loc.columns]

            df_loc = df_loc[available_columns]
        else:
            df_loc = pd.DataFrame()

        return vkt.TableResult(df_loc)
    


    # RESULTS PER INDIVIDUAL LOCATION
    # This shows the location and location-specific borehole data
    @vkt.TableView("Borehole Data", duration_guess=1)
    def show_borehole_csv(self, params, **kwargs):
        # Create dataframes for locations and boreholes
        df_loc, df_bh = self.input_csvs(params)

        if params.page_2.section_1.option_field_1:
            filtered_df_bh = df_bh[df_bh['Location ID'] == params.page_2.section_1.option_field_1]
            # Define desired columns and check which ones exist
            desired_columns = ["Location ID", "Depth Top", "Depth Base", "Description", "Geology Code Arup"]
            available_columns = [col for col in desired_columns if col in filtered_df_bh.columns]
            
            # Select only the available columns
            filtered_df_bh = filtered_df_bh[available_columns]
            filtered_df_bh = filtered_df_bh.sort_values(by=['Location ID', 'Depth Top'])
        else:
            filtered_df_bh = pd.DataFrame()

        return vkt.TableResult(filtered_df_bh)
    

    # This shows the settlement graph for a selected location
    @vkt.PlotlyView('Settlement over time', duration_guess=1)
    def plot_settl_graph(self, params, **kwargs):
        # Create dataframes for locations and boreholes
        df_loc, df_bh = self.input_csvs(params)

        material_table = params.page_1.tab_1.section_2.table_1
        
        location_id = params.page_2.section_1.option_field_1
        log = params.page_2.section_1.boolean_field_1

        ground_level = find_ground_level(df_loc, location_id)
        filtered_df_bh = find_filtered_df_bh(df_loc, df_bh, location_id)

        if not filtered_df_bh.empty:
            levels, layer_names = get_layers(filtered_df_bh, ground_level, material_table)

        time_in_days = np.logspace(0.1, 4, 20)
        d, sld_file, sli_file = self.create_Dsettl_model(params, ground_level, levels, layer_names, location_id)

        settlements = []
        for t in time_in_days:
            result_dict = extract_iteration_results_dset(d, time=t, ground_level=ground_level, loads_table=params.page_1.tab_5.section_1.table_1)
            settlements.append(result_dict.get('settlement', 0))
        
        fig = create_settl_graphs(d, log, ground_level, loads_table=params.page_1.tab_5.section_1.table_1)

        return vkt.PlotlyResult(fig)  # Changed from: return fig
        

    def create_Dsettl_model(self, params, ground_level, levels, layer_names, location_id):
        # Create the model with misc. options.
        material_properties = params.page_1.tab_1.section_2.table_1
        const_model = model_types[params.page_1.tab_1.section_1.autocomplete_field_1]
        consol_model = cons_model_types[params.page_1.tab_1.section_1.option_field_1]

        # groundlevel = -0.45
        GWT = params.page_1.tab_4.number_field_1

        # Create loads table
        loads_table = params.page_1.tab_5.section_1.table_1

        model = create_dsettlement_model(material_properties, const_model, consol_model, GWT, levels, layer_names)
        
        # if iterative_load_bool:
        model = add_table_loads(model, loads_table, ground_level)

        result, sld_file, sli_file = run_model(model)

        return result, sld_file, sli_file

    
    @vkt.PlotlyView('Geological Profile', duration_guess=1)
    def get_combined_geo_profile_and_map(self, params, **kwargs):
        # Create dataframes for locations and boreholes
        df_loc, df_bh = self.input_csvs(params)
        
        #select parameters from input
        Location_id = params.page_2.section_1.option_field_1
        coord_system = params.page_1.tab_2.option_field_1
        material_table = params.page_1.tab_1.section_2.table_1

        fig = create_geo_profile_and_map(df_loc, df_bh, Location_id, coord_system, material_table)
            
        return vkt.PlotlyResult(fig)
    

    # ALL LOCATIONS
    # This shows a table of the settlement results at a certain time for all locations
    @vkt.memoize
    def settl_results(self, params, **kwargs):
        # Create dataframes for locations and boreholes
        df_loc, df_bh = self.input_csvs(params)
        # Material table
        material_table = params.page_1.tab_1.section_2.table_1

        # loads table
        loads_table = params.page_1.tab_5.section_1.table_1
        
        # Define time in days:
        time_in_days = times[params.page_3.section_2.number_field_1] * 30 # Approximate conversion from months to days

        # Get all location IDs (including those without borehole data)
        valid_location_ids = [loc_id for loc_id in df_loc['Location ID'].unique() if loc_id != '' and pd.notna(loc_id)]
        total_calculations = len(valid_location_ids)

        print(f"Total locations to process: {total_calculations}")
        print(f"Location IDs: {valid_location_ids}")

        # Initialize list to collect all results
        all_results = []

        # Calculate settlements for all locations
        for i, location_id in enumerate(valid_location_ids):
            # Progress message
            moving_train = get_train(i)
            percentage = int((i / total_calculations) * 100)

            message = f"Processing location {i + 1}/{total_calculations}: {location_id}"
            message = message + "  \n  \n" + moving_train

            vkt.progress_message(
                message=message,
                percentage=percentage
            )

            print(f"Processing location {i + 1}: {location_id}")

            try:
                # For every location, get the required data
                ground_level = find_ground_level(df_loc, location_id)
                filtered_df_bh = find_filtered_df_bh(df_loc, df_bh, location_id)
                
                print(f"Ground level for {location_id}: {ground_level}")
                print(f"Borehole data empty: {filtered_df_bh.empty}")
                
                if not filtered_df_bh.empty:
                    levels, layer_names = get_layers(filtered_df_bh, ground_level, material_table)

                    # Create and run model
                    d, sld_file, sli_file = self.create_Dsettl_model(params, ground_level, levels, layer_names, location_id)
                    
                    result_dict = extract_iteration_results_dset(d, time=time_in_days, ground_level=ground_level, loads_table=loads_table)
                    
                    # Add location ID to the result dictionary
                    result_dict['Location_ID'] = location_id
                    
                    print(f"Result for {location_id}: {result_dict}")
                    
                    # Collect the result
                    all_results.append(result_dict)
                else:
                    # Handle case where no borehole data exists - ALWAYS add result
                    print(f"No borehole data for {location_id}")
                    result_dict = {
                        'Location_ID': location_id,
                        'settlement': 'No borehole data',
                        'effective_vertical_stress': 'No borehole data',
                        'time_found': 'No borehole data'
                    }
                    all_results.append(result_dict)
                    
            except Exception as e:
                # Handle any errors during processing - ALWAYS add result
                print(f"ERROR processing {location_id}: {str(e)}")
                print(f"ERROR type: {type(e)}")
                import traceback
                traceback.print_exc()
                
                result_dict = {
                    'Location_ID': location_id,
                    'settlement': f'Error: {str(e)[:50]}',  # Truncate long error messages
                    'effective_vertical_stress': 'Error',
                    'time_found': 'Error'
                }
                all_results.append(result_dict)

        
        # Create final DataFrame with all results
        if all_results:
            result = pd.DataFrame(all_results)
            # Set Location_ID as index if desired
            result = result.set_index('Location_ID')
            print(f"Final DataFrame shape: {result.shape}")
            print(f"Final DataFrame:\n{result}")
        else:
            result = pd.DataFrame({'Message': ['No valid locations found']})

        return result
    
    def cached_results(self, params, **kwargs):
        return self.settl_results(params, **kwargs)

    @vkt.TableView('ALL Settlement results', duration_guess=10)
    def plot_settl_results(self, params, **kwargs):
        df_settl_results = self.cached_results(params)

        return vkt.TableResult(df_settl_results)

    @vkt.ImageView("Heatmap")
    def plot_heatmap(self, params, **kwargs):
        # Create dataframes for locations and boreholes
        df_loc, df_bh = self.input_csvs(params)
        input_csv_settl = params.page_3.section_5.file_field_1
        if input_csv_settl:
            df_settl_results = create_df(input_csv_settl)
            df_settl_results['location id'] = df_settl_results['0']

        # This will now use the cached result if available
        # df_settl_results = self.cached_results(params)

         # Define point size and annotation toggle
        point_size = params.page_3.section_2.number_field_2
        toggle_annotations = params.page_3.section_2.is_true

        # Option field for showing results on heatmap
        option_field_result = params.page_3.section_1.option_field_1

        if option_field_result == 'zetting na 9 maanden':
            if not df_settl_results.empty and 'zetting na 9 maanden' in df_settl_results.columns:
                values = df_settl_results['zetting na 9 maanden'].tolist()
                names = df_settl_results['location id'].tolist()
            else:
                print("Error: Settlement results DataFrame is empty or missing 'zetting na 9 maanden' column.")
        elif option_field_result == 'new ground level':
            if not df_settl_results.empty and 'new_level' in df_settl_results.columns:
                values = df_settl_results['new_level'].tolist()
                names = df_settl_results['location id'].tolist()
            else:
                print("Error: Settlement results DataFrame is empty or missing 'new_level' column.")
        elif option_field_result == 'restzetting (60 years-9 months)':
            if not df_settl_results.empty and 'restzetting (60 years-9 months)' in df_settl_results.columns:
                values = df_settl_results['restzetting (60 years-9 months)'].tolist()
                names = df_settl_results['location id'].tolist()
            else:
                print("Error: Settlement results DataFrame is empty or missing 'restzetting (60 years-9 months)' column.")
        elif option_field_result == 'eindzetting':
            if not df_settl_results.empty and 'eindzetting' in df_settl_results.columns:
                values = df_settl_results['eindzetting'].tolist()
                names = df_settl_results['location id'].tolist()
            else:
                print("Error: Settlement results DataFrame is empty or missing 'eindzetting' column.")
        
        # svg_data = create_heatmap(df_loc, '', '')
        svg_data = create_heatmap(df_loc, values, names, point_size, toggle_annotations)

        return vkt.ImageResult(svg_data)


    def download_zip(self, params, **kwargs):
        # Create dataframes for locations and boreholes
        df_loc, df_bh = self.input_csvs(params)
        location_id = params.page_2.section_1.option_field_1
        material_table = params.page_1.tab_1.section_2.table_1
        
        file = vkt.File()

        ground_level = find_ground_level(df_loc, location_id)
        filtered_df_bh = find_filtered_df_bh(df_loc, df_bh, location_id)

        levels, layer_names = get_layers(filtered_df_bh, ground_level, material_table)

        result, sld_file, sli_file = self.create_Dsettl_model(params, ground_level, levels, layer_names, location_id)

        return vkt.DownloadResult(zipped_files={f"{location_id}.sli": sli_file, f"{location_id}.sld": sld_file}, file_name=f"{location_id}_model.zip")

    @vkt.ImageView("Scattermap")
    def plot_scatter(self, params, **kwargs):
        # Create dataframes for locations and boreholes
        df_loc, df_bh = self.input_csvs(params)
        input_csv_settl = params.page_3.section_5.file_field_1
        if input_csv_settl:
            df_settl_results = create_df(input_csv_settl)
            df_settl_results['location id'] = df_settl_results['0']

        option = params.page_3.section_1.option_field_1

         # Define point size and annotation toggle
        point_size = params.page_3.section_2.number_field_2
        toggle_annotations = params.page_3.section_2.is_true


        if not df_settl_results.empty and 'zetting na 9 maanden' in df_settl_results.columns:
            values = df_settl_results['restzetting (60 years-9 months)'].tolist()
            names = df_settl_results['location id'].tolist()

        # Create scatter plot
        svg_data = create_restsettl_scatter(df_loc, values, names, point_size, toggle_annotations, option_field=option)

        return vkt.ImageResult(svg_data)
    

    @vkt.MapView("Points Map")
    def show_points_map(self, params, **kwargs):
        """Display points on a map with color-coded values."""
        features = []

        # Create dataframes for locations and boreholes
        df_loc, df_bh = self.input_csvs(params)
        input_csv_settl = params.page_3.section_5.file_field_1


        
        # Create map features for each point
        for point_data in params.data_section.points_data:
            lat = point_data['latitude']
            lon = point_data['longitude']
            value = point_data['value']
            
            # Get color based on value and intervals
            color_hex = self.get_color_for_value(value, params)
            color_rgb = vkt.Color.hex_to_rgb(color_hex)
            color = vkt.Color(color_rgb[0], color_rgb[1], color_rgb[2])
            
            # Get interval label
            interval_label = self.get_interval_label(value, params)
            
            # Create map point
            map_point = vkt.MapPoint(
                lat=lat,
                lon=lon,
                title=f"Point (Value: {value})",
                description=f"Location: ({lat:.4f}, {lon:.4f})\nValue: {value}\nInterval: {interval_label}",
                color=color,
                size='medium'
            )
            features.append(map_point)
        
        # Create legend entries
        legend_entries = [
            (params.color_custom_section.color_1, f"≤ {params.color_section.interval_1_max}"),
            (params.color_custom_section.color_2, f"{params.color_section.interval_1_max} - {params.color_section.interval_2_max}"),
            (params.color_custom_section.color_3, f"{params.color_section.interval_2_max} - {params.color_section.interval_3_max}"),
            (params.color_custom_section.color_4, f"> {params.color_section.interval_3_max}")
        ]
        legend = vkt.MapLegend(legend_entries)
        
        return vkt.MapResult(features, legend=legend)    

