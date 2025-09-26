from io import BytesIO
from tkinter.font import names
import viktor as vkt
import plotly.graph_objects as go
from plotly.subplots import make_subplots 
from viktor.views import PlotlyView, PlotlyResult
import pandas as pd
import numpy as np
from src.Helper import create_df
from src.Defaults import create_default_mat_prop
from src.Dsettl import create_Dset_geometry, create_dsettlement_model
from src.Dsettl_results import extract_iteration_results_dset
from src.Visualizations import create_geo_profile_and_map, create_heatmap
from io import BytesIO, StringIO
import geolib as gl

model_types = {'NEN_BJERRUM': gl.models.dsettlement.internal.SoilModel.NEN_BJERRUM, 'NEN_KOPPEJAN': gl.models.dsettlement.internal.SoilModel.NEN_KOPPEJAN, 'ISOTACHE': gl.models.dsettlement.internal.SoilModel.ISOTACHE}
cons_model_types = {"DARCY": gl.models.dsettlement.internal.ConsolidationModel.DARCY, "TERZAGHI": gl.models.dsettlement.internal.ConsolidationModel.TERZAGHI}

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
    page_1 = vkt.Page("Inputs and checking", views=["show_locations_csv", "show_borehole_csv", "get_combined_geo_profile_and_map"], width=30)
    
    
    # Model Properties tab
    page_1.tab_1 = vkt.Tab("Model properties", description="What are the modelling properties for this project?")
    page_1.tab_1.section_1 = vkt.Section("Model types", description="Types for calculation and consolidation")
    page_1.tab_1.section_1.autocomplete_field_1 = vkt.AutocompleteField("Settlement calculation method", suffix="Settlement calculation method", options=list(model_types.keys()), default='NEN_BJERRUM')
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
    page_1.tab_3.option_field_1 = vkt.OptionField("Location ID for preview", options=get_location_filter_list, visible=_filter_list_vis)
    

    # Geometry tab
    page_1.tab_4 = vkt.Tab("Ground Water Table")
    page_1.tab_4.number_field_1 = vkt.NumberField("Ground Water Table - relative to NAP")
    
    # Loads tab
    page_1.tab_5 = vkt.Tab("Loads")
    page_1.tab_5.section_1 = vkt.Section("Uniform Load", description="Input for uniform loads on the area")
    page_1.tab_5.section_1.number_field_1 = vkt.NumberField("Unit Weight", flex=100, suffix="kN/m3", min=0)
    page_1.tab_5.section_1.number_field_2 = vkt.NumberField("Thickness", flex=100, suffix="m", min=0)
    

    page_2 = vkt.Page("Settlement Analysis Results", views=["plot_settl_results", "get_combined_geo_profile_and_map", "plot_heatmap"], width=20)
    page_2.number_field_1 = vkt.NumberField("Adjust the point size on the heatmap", default=50, min=0, max=200, step=10, variant="slider", flex=100)
    page_2.is_true = vkt.BooleanField("Show annotations on heatmap", default=True, flex=100)

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
    

    @vkt.TableView("Borehole Data", duration_guess=1)
    def show_borehole_csv(self, params, **kwargs):
        # Create dataframes for locations and boreholes
        df_loc, df_bh = self.input_csvs(params)

        if params.page_1.tab_3.option_field_1:
            filtered_df_bh = df_bh[df_bh['Location ID'] == params.page_1.tab_3.option_field_1]
            # Define desired columns and check which ones exist
            desired_columns = ["Location ID", "Depth Top", "Depth Base", "Description", "Geology Code Arup"]
            available_columns = [col for col in desired_columns if col in filtered_df_bh.columns]
            
            # Select only the available columns
            filtered_df_bh = filtered_df_bh[available_columns]
            filtered_df_bh = filtered_df_bh.sort_values(by=['Location ID', 'Depth Top'])
        else:
            filtered_df_bh = pd.DataFrame()

        return vkt.TableResult(filtered_df_bh)
    

    @vkt.ImageView("Heatmap")
    def plot_heatmap(self, params, **kwargs):
        # Create dataframes for locations and boreholes
        df_loc, df_bh = self.input_csvs(params)

        point_size = params.page_2.number_field_1
        toggle_annotations = params.page_2.is_true

        if not df_loc.empty:
            values = df_loc['Ground Level'].tolist()
            names = df_loc['Location ID'].tolist()
        
        # svg_data = create_heatmap(df_loc, '', '')
        svg_data = create_heatmap(df_loc, values, names, point_size, toggle_annotations)

        return vkt.ImageResult(svg_data)
    
    
    @vkt.PlotlyView('Geological Profile', duration_guess=1)
    def get_combined_geo_profile_and_map(self, params, **kwargs):
        # Create dataframes for locations and boreholes
        df_loc, df_bh = self.input_csvs(params)
        
        #select parameters from input
        Location_id = params.page_1.tab_3.option_field_1
        coord_system = params.page_1.tab_2.option_field_1
        material_table = params.page_1.tab_1.section_2.table_1

        fig = create_geo_profile_and_map(df_loc, df_bh, Location_id, coord_system, material_table)
            
        return vkt.PlotlyResult(fig)
    

    @vkt.TableView('Settlement results', duration_guess=1)
    def plot_settl_results(self, params, **kwargs):
        # d = self.create_Dfound_model(params)
        d = self.create_Dsettl_model(params)
        # result = extract_iteration_results_dset(d, time=10000)
        result_dict = extract_iteration_results_dset(d, time=10000)  # Example time in days
        
        # Create DataFrame with dictionary keys as column names
        result = pd.DataFrame([result_dict])  # Pass as list to create one row with keys as columns
    
        # TableView can handle DataFrames directly
        if isinstance(result, pd.DataFrame):
            return vkt.TableResult(result)
        else:
            # If not a DataFrame, create a simple DataFrame to display
            df = pd.DataFrame({'Result': [str(result)]})
            return vkt.TableResult(df)
        
        
    def create_Dsettl_model(self, params):
        # Create the model with misc. options.
        material_properties = params.page_1.tab_1.section_2.table_1
        const_model = model_types[params.page_1.tab_1.section_1.autocomplete_field_1]
        consol_model = cons_model_types[params.page_1.tab_1.section_1.option_field_1]

        result = create_dsettlement_model(material_properties, const_model, consol_model)

        return result
        


  
    

    
