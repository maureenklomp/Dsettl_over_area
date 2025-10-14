import numpy as np
import viktor as vkt
from src.Dsettl_results import extract_iteration_results_dset
from src.Helper import materials_to_dict
import geolib as gl
from pathlib import Path
from datetime import timedelta

def create_dsettlement_model(material_properties, const_model, consol_model, GWT, levels, layer_names, bool_vert_drain):
    
    # Catching input errors
    violations = []
    if const_model == 2:
        violations.append(vkt.InputViolation("Constitutive model cannot be Isotache, only NEN-Bjerrum is currently available", fields=[const_model]))
    if const_model == 0:
        violations.append(vkt.InputViolation("Constitutive model cannot be Koppejan, only NEN-Bjerrum is currently available", fields=[const_model]))
    if GWT is None:
        violations.append(vkt.InputViolation("Groundwater level must be specified", fields=[GWT]))

    if violations:
        raise vkt.UserError("Invalid input for constitutive or consolidation model", input_violations=violations)

    model = gl.DSettlementModel()
    model.set_model(constitutive_model= const_model,
                    consolidation_model= consol_model,
                    is_two_dimensional=True,
                    strain_type= gl.models.dsettlement.internal.StrainType.LINEAR,
                    is_vertical_drain=bool_vert_drain,
                    is_fit_for_settlement_plate=False,
                    is_probabilistic=False,
                    is_horizontal_displacements=False,
                    is_secondary_swelling=False)
    
    # Create soil types
    # material_layers = ["SAND", "Peat", "Silty SAND", "Organic CLAY", "Peat", "Silty CLAY"]

    materials = materials_to_dict(material_properties)
    material_names = list(materials.keys())

    s = {}
    for material_name in material_names:
        if material_name in materials:
            props = materials[material_name]

            # Create soil type with specified properties
            s = gl.soils.Soil(name=material_name)
            s.soil_weight_parameters.saturated_weight.mean = props['sat_weight']  # kN/m³
            s.soil_weight_parameters.unsaturated_weight.mean = props['unsat_weight']  # kN/m³
            
            s.is_drained = props['is_drained']
            if not s.is_drained:
                s.storage_parameters.storage_type = 0
                s.storage_parameters.vertical_consolidation_coefficient.mean = props['cv'] # m²/s

            s.isotache_parameters.precon_isotache_type = gl.soils.StateType.POP
            s.soil_state.pop_layer.mean = props['pop_layer']  # kN/m2

            s.bjerrum_parameters.compression_ratio_CR.mean = props['cr']  # kN/m2
            s.bjerrum_parameters.reloading_swelling_RR.mean = props['rr']  # kN/m2
            s.bjerrum_parameters.coef_secondary_compression_Ca.mean = props['ca']  # kN/m2

            model.add_soil(s)
        else:
            raise ValueError(f"Material '{material_name}' not found in provided material properties table.")
    
    # Headline lines
    p1 = gl.geometry.Point(x=0, z=GWT)
    p2 = gl.geometry.Point(x=50, z=GWT)
    hl = model.add_head_line([p1, p2], is_phreatic=True)

    # Boundary lines
    # layers = [-20.0, -8.75, -8.0, -3.75, -3.0, -1.5, ground_level]

    p_left = []
    p_right = []

    boundary_lines = []

    for i in range(len(levels)):
        p_left.append(gl.geometry.Point(x=0, z=levels[i]))
        p_right.append(gl.geometry.Point(x=50, z=levels[i]))
        boundary_lines.append(model.add_boundary([p_left[i], p_right[i]]))
    
    for j in range(len(layer_names)):
        model.add_layer(boundary_top=boundary_lines[j], boundary_bottom=boundary_lines[j + 1], material_name= layer_names[j], head_line_top=hl, head_line_bottom=hl)

    # Create vertical
    p0 = gl.geometry.Point(x=25, z=0)
    model.set_verticals([p0])

    return model


def add_table_loads(model, loads_table, ground_level):
    """
    Add loads from a table to the model
    """
    # Catching input errors
    violations = []
    if loads_table is None or len(loads_table) == 0:
        violations.append(vkt.InputViolation("Load table must be specified", fields=[loads_table]))

    if violations:
        raise vkt.UserError("Invalid input for load table", input_violations=violations)

    current_top_level = ground_level  # Track the current top level
    
    for row in loads_table:
        name = row['col_1']
        time_start = row['col_2']
        load_value = row['col_3']
        load_thickness = row['col_4']

        if load_value >= 0:
            # Positive load: add material on top
            current_base_level = current_top_level
            current_top_level = current_base_level + load_thickness
            
            # For positive loads: normal point order (base to top)
            point3 = gl.geometry.Point(label="1", x=10, y=0, z=current_base_level)
            point4 = gl.geometry.Point(label="2", x=10, y=0, z=current_top_level)
            point5 = gl.geometry.Point(label="3", x=40, y=0, z=current_top_level)
            point6 = gl.geometry.Point(label="4", x=40, y=0, z=current_base_level)
        else:
            # Negative load: excavate/remove material
            current_base_level = current_top_level - load_thickness
            
            # For negative loads: points 3,6 at top, points 4,5 at bottom
            point3 = gl.geometry.Point(label="1", x=10, y=0, z=current_top_level)
            point4 = gl.geometry.Point(label="2", x=10, y=0, z=current_base_level)
            point5 = gl.geometry.Point(label="3", x=40, y=0, z=current_base_level)
            point6 = gl.geometry.Point(label="4", x=40, y=0, z=current_top_level)
            
            # Update current top level to the new excavated level
            current_top_level = current_base_level
        
        pointlist = [point3, point4, point5, point6]
        
        # Add uniform load from table
        model.add_non_uniform_load(
            name=name,
            points=pointlist,
            time_start=timedelta(days=time_start),
            gamma_dry=load_value,
            gamma_wet=load_value,
        )

    # input_test_file = Path("Test.sli")
    # model.serialize(input_test_file)

    return model

def add_vertical_drains(model, drain_type, drain_spacing, drain_bottom, grid_type, start_time, end_time, underpressure, tube_pressure, water_head, phreatic_level, drain_diameter=None, drain_width=None, drain_thickness=None):
    """
    Add vertical drains to the model
    Parameters:
    - drain_type: String - "COLUMN", "STRIP", or "SANDWALL"
    - grid_type: String - "RECTANGULAR" or "TRIANGULAR"
    - drain_diameter: Required for COLUMN drain type
    - drain_width: Required for STRIP and SANDWALL drain types  
    - drain_thickness: Required for STRIP and SANDWALL drain types
    """
    # Convert string types to enums
    drain_type_enum = gl.models.dsettlement.drains.DrainType[drain_type]
    grid_type_enum = gl.models.dsettlement.drains.DrainGridType[grid_type]
    
    # Catching input errors
    # violations = []
    # if drain_type is None:
    #     violations.append(vkt.InputViolation("Drain type must be specified"))
    # if drain_spacing is None or drain_spacing <= 0:
    #     violations.append(vkt.InputViolation("Drain spacing must be a positive number"))
    # if drain_bottom is None:
    #     violations.append(vkt.InputViolation("Drain bottom level must be specified"))
    
    # # Validate drain-specific parameters
    # if drain_type == "COLUMN":
    #     if drain_diameter is None or drain_diameter <= 0:
    #         violations.append(vkt.InputViolation("Drain diameter must be a positive number for COLUMN drain type"))
    # elif drain_type in ["STRIP", "SANDWALL"]:
    #     if drain_width is None or drain_width <= 0:
    #         violations.append(vkt.InputViolation("Drain width must be a positive number for STRIP/SANDWALL drain type"))
    #     if drain_thickness is None or drain_thickness <= 0:
    #         violations.append(vkt.InputViolation("Drain thickness must be a positive number for STRIP/SANDWALL drain type"))
    
    # if grid_type is None:
    #     violations.append(vkt.InputViolation("Grid type must be specified"))
    # if start_time is None or start_time < 0:
    #     violations.append(vkt.InputViolation("Start time must be a non-negative number"))
    # if end_time is None or end_time <= start_time:
    #     violations.append(vkt.InputViolation("End time must be greater than start time"))
    # if underpressure is None or underpressure < 0:
    #     violations.append(vkt.InputViolation("Underpressure must be a non-negative number"))
    # if tube_pressure is None or tube_pressure < 0:
    #     violations.append(vkt.InputViolation("Tube pressure must be a non-negative number"))
    # if water_head is None or water_head < 0:
    #     violations.append(vkt.InputViolation("Water head must be a non-negative number"))
    # if phreatic_level is None:
    #     violations.append(vkt.InputViolation("Phreatic level must be specified"))

    # if violations:
    #     raise vkt.UserError("Invalid input for vertical drains", input_violations=violations)

    # Fixed range values
    range_from = 0
    range_to = 50

    # Create vertical drain with appropriate parameters based on drain type
    if drain_type == "COLUMN":
        vertical_drain = gl.models.dsettlement.drains.VerticalDrain(
            drain_type=drain_type_enum,
            range_from=range_from,
            range_to=range_to,
            bottom_position=drain_bottom,
            center_to_center=drain_spacing,
            diameter=drain_diameter,
            grid=grid_type_enum,
            schedule=gl.models.dsettlement.drains.ScheduleValuesSimpleInput(
                start_of_drainage=timedelta(days=start_time),
                phreatic_level_in_drain=phreatic_level,
                begin_time=1,
                end_time=end_time,
                underpressure=underpressure,
                tube_pressure_during_dewatering=tube_pressure,
                water_head_during_dewatering=water_head,
            ),
        )
    elif drain_type == "STRIP":
        vertical_drain = gl.models.dsettlement.drains.VerticalDrain(
            drain_type=drain_type_enum,
            range_from=range_from,
            range_to=range_to,
            bottom_position=drain_bottom,
            center_to_center=drain_spacing,
            width=drain_width,
            thickness=drain_thickness,
            grid=grid_type_enum,
            schedule=gl.models.dsettlement.drains.ScheduleValuesSimpleInput(
                start_of_drainage=timedelta(days=start_time),
                phreatic_level_in_drain=phreatic_level,
                begin_time=1,
                end_time=end_time,
                underpressure=underpressure,
                tube_pressure_during_dewatering=tube_pressure,
                water_head_during_dewatering=water_head,
            ),
        )
    elif drain_type == "SANDWALL":
        vertical_drain = gl.models.dsettlement.drains.VerticalDrain(
            drain_type=drain_type_enum,
            range_from=range_from,
            range_to=range_to,
            bottom_position=drain_bottom,
            center_to_center=drain_spacing,
            width=drain_width,
            grid=grid_type_enum,
            schedule=gl.models.dsettlement.drains.ScheduleValuesSimpleInput(
                start_of_drainage=timedelta(days=start_time),
                phreatic_level_in_drain=phreatic_level,
                begin_time=1,
                end_time=end_time,
                underpressure=underpressure,
                tube_pressure_during_dewatering=tube_pressure,
                water_head_during_dewatering=water_head,
            ),
        )

    model.set_vertical_drain(vertical_drain)
    return model
    

def run_model(model):
    """
    Run the model and return the SLD file content as a string
    """
    # Try execution approaches
    file = vkt.File()
    path = Path(file.source)
    model.serialize(path)
    
    dsettlementanalysis = vkt.dsettlement.DSettlementAnalysis(input_file=file)
    dsettlementanalysis.execute(timeout=600)

    # Obtain the result file.
    sld_file = dsettlementanalysis.get_sld_file()
    sli_file = file

    # Read the raw content
    sld_string = sld_file.getvalue()

    return sld_string, sld_file, sli_file


def create_Dset_geometry(df_bh, ground_level, material_table):
        """
        Create geometry lists for geological layers including colors and names
        """
        material = []
        depth_top = []
        depth_base = []
        color = []
        name = []
        thickness = []
        
        # Define material colors and names inside the function
        material_colors = {}
        for row in material_table:
             material_name = row['col_1']
             material_color = row['col_4']
             material_colors[material_name] = material_color
        
        df_bh_sorted = df_bh.sort_values(by='Depth Top')

        # Creating lists
        for index, row in df_bh_sorted.iterrows():
            mat = row['Description']
            d_top = round(-row['Depth Top'] + ground_level, 2)
            d_base = round(-row['Depth Base'] + ground_level, 2)
            thick = round(d_top - d_base, 2)  # Fixed parenthesis
            
            material.append(mat)
            depth_top.append(d_top)
            depth_base.append(d_base)
            thickness.append(thick)
            color.append(material_colors.get(mat, 'white'))
            name.append(mat)
        
        return material, depth_top, depth_base, color, name, thickness


def get_layers(filtered_df_bh, ground_level, material_table):
    if not filtered_df_bh.empty:
        materials, depth_tops, depth_bases, colors, names, thicknesses = create_Dset_geometry(filtered_df_bh, ground_level, material_table)
    
    depth_base_array = np.array(depth_bases)
    reversed_array = depth_base_array[::-1].tolist()

    names_array = np.array(names)
    layer_names = names_array[::-1].tolist()
    
    # Ensure ground_level is added to each element
    levels = reversed_array + [float(ground_level)]

    return levels, layer_names

