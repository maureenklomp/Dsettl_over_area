import numpy as np
import viktor as vkt
from src.Dsettl_results import extract_iteration_results_dset
from src.Helper import materials_to_dict
import geolib as gl
from pathlib import Path
from datetime import timedelta

def create_dsettlement_model(material_properties, const_model, consol_model, GWT, levels, layer_names):
    
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
                    is_vertical_drain=False,
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


def add_uniform_dsettlem_loads(model, load_value, load_thickness, ground_level):
    """
    Add uniform load to the model
    """
    # Catching input errors
    violations = []
    if load_value is None or load_thickness is None:
        violations.append(vkt.InputViolation("Load value and thickness must be specified", fields=[load_value, load_thickness]))

    if violations:
        raise vkt.UserError("Invalid input for constitutive or consolidation model", input_violations=violations)

    # set up the point list
    point3 = gl.geometry.Point(label="1", x=10, y=0, z=ground_level)
    point4 = gl.geometry.Point(label="2", x=10, y=0, z=ground_level + load_thickness)
    point5 = gl.geometry.Point(label="3", x=40, y=0, z=ground_level + load_thickness)
    point6 = gl.geometry.Point(label="4", x=40, y=0, z=ground_level)
    pointlist = [point3, point4, point5, point6]
    # Add first uniform load
    model.add_non_uniform_load(
        name="My First Load",
        points=pointlist,
        time_start=timedelta(days=0),
        gamma_dry=load_value,
        gamma_wet=load_value,
    )

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
    # sld_string = sld_bytes.decode('utf-8')

    # if download_bool:
    #     sli_filename = str(location_id) + ".sli"  
    #     input_test_file = Path(sli_filename)
    #     model.serialize(input_test_file)

    #     sld_filename = str(location_id) + ".sld"  
    #     # Save results to a local file (if running locally)
    #     with open(sld_filename, "w") as f:
    #         f.write(sld_file.getvalue())   

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

