import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import viktor as vkt
from io import StringIO
from src.Dfound_results import extract_iteration_results
from src.Dsettl_results import extract_iteration_results_dset
from src.Helper import convert_color_string_to_tuple
import geolib as gl
from pathlib import Path
from datetime import timedelta
import os

def create_dsettlement_model(material_properties):
    # # Set environment variable for geolib
    # os.environ['DSETTLEMENT_CONSOLE_PATH'] = r'C:\Program Files (x86)\Deltares\D-Settlement 23.2.1'
    
    # # Alternative approach - set the executable directly
    # dsettlement_path = r'C:\Program Files (x86)\Deltares\D-Settlement 23.2.1\DSettlement.exe'
    
    # # Check if executable exists
    # if not os.path.exists(dsettlement_path):
    #     print("Option 1")
    #     raise FileNotFoundError(f"D-Settlement executable not found at {dsettlement_path}")
    
    # # Configure geolib - try multiple approaches
    # try:
    #     gl.models.dsettlement.internal.DSETTLEMENT_EXECUTABLE = dsettlement_path
    #     print(gl.models.dsettlement.internal.DSETTLEMENT_EXECUTABLE)
    # except:
    #     pass
    
    # try:
    #     gl.env.DSETTLEMENT_CONSOLE_PATH = r'C:\Program Files (x86)\Deltares\D-Settlement 23.2.1'
    #     print("Option 3")
    # except:
    #     pass
    
    model = gl.DSettlementModel()

    model.set_model(constitutive_model= gl.models.dsettlement.internal.SoilModel.NEN_BJERRUM,
                    consolidation_model= gl.models.dsettlement.internal.ConsolidationModel.DARCY,
                    is_two_dimensional=True,
                    strain_type= gl.models.dsettlement.internal.StrainType.LINEAR,
                    is_vertical_drain=False,
                    is_fit_for_settlement_plate=False,
                    is_probabilistic=False,
                    is_horizontal_displacements=False,
                    is_secondary_swelling=False)
    
    # Create soil types
    material_layers = ["SAND", "Peat", "Silty SAND", "Organic CLAY", "Peat", "Silty CLAY"]

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
    p1 = gl.geometry.Point(x=0, z=-1)
    p2 = gl.geometry.Point(x=50, z=-1)
    hl = model.add_head_line([p1, p2], is_phreatic=True)

    # Boundary lines
    layers = [-20.0, -8.75, -8.0, -3.75, -3.0, -1.5, -0.45]

    p_left = []
    p_right = []

    boundary_lines = []

    for i in range(len(layers)):
        p_left.append(gl.geometry.Point(x=0, z=layers[i]))
        p_right.append(gl.geometry.Point(x=50, z=layers[i]))
        boundary_lines.append(model.add_boundary([p_left[i], p_right[i]]))
    
    for j in range(len(material_layers)):
        model.add_layer(boundary_top=boundary_lines[j], boundary_bottom=boundary_lines[j + 1], material_name= material_layers[j], head_line_top=hl, head_line_bottom=hl)

    # Create vertical
    p0 = gl.geometry.Point(x=25, z=0)
    model.set_verticals([p0])

    # Add uniform load
    # set up the point list
    point3 = gl.geometry.Point(label="1", x=10, y=0, z=-0.45)
    point4 = gl.geometry.Point(label="2", x=10, y=0, z=1.5)
    point5 = gl.geometry.Point(label="3", x=40, y=0, z=1.5)
    point6 = gl.geometry.Point(label="4", x=40, y=0, z=-0.45)
    pointlist = [point3, point4, point5, point6]
    # Add first uniform load
    model.add_non_uniform_load(
        name="My First Load",
        points=pointlist,
        time_start=timedelta(days=0),
        gamma_dry=18.0,
        gamma_wet=20.0,
    )

    input_test_file = Path("Trial_2.sli")
    model.serialize(input_test_file)

    model.filename = input_test_file
    # model.execute()

    return model




#* Default material properties for soil types
def create_default_mat_prop():
    """
    Create default material properties for geological layers
    """

    material = ['9', '8', '7', '6', '5', '4', '3', '2', '1']
    name = ['Stiff fine SAND', 'Stiff SAND', 'Dense SAND', 'SAND', 'Silty SAND', 'Silty CLAY', 'CLAY', 'Organic CLAY', 'Peat']
    y_dry = [19.0, 19.0, 19.0, 19.0, 18.0, 18.0, 17.0, 13.0, 12.0]  # in kPa
    y_sat = [21.0, 21.0, 21.0, 21.0, 20.0, 18.0, 17.0, 13.0, 12.0]  # in kPa
    color = ['yellow', 'yellow', 'yellow', 'yellow', 'lightyellow', 'gray', 'darkgray', 'brown', 'red']
    RR = [0.0008, 0.0008, 0.0008, 0.0008, 0.0017, 0.038, 0.051, 0.102, 0.102]
    CR = [0.0023, 0.0023, 0.0023, 0.0023, 0.0051, 0.115, 0.153, 0.307, 0.307]  
    Ca = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0046, 0.0061, 0.015, 0.015]
    cv = [1.00e-7, 1.00e-7, 1.00e-7, 1.00e-7, 1.70e-8, 3.00e-7, 5.50e-8, 2.00e-8, 2.00e-8]  # in m²/s
    pop_layer = [5.0, 5.0, 5.0, 5.0, 5.0, 3.0, 3.0, 3.0, 2.0]  # in kPa

    material_props = []
    for i in range(len(material)):
        material_props.append({
            'col_1': name[i],
            'col_2': y_dry[i],
            'col_3': y_sat[i],
            'col_4': color[i],
            'col_5': RR[i],
            'col_6': CR[i],
            'col_7': Ca[i],
            'col_8': cv[i],
            'col_9': pop_layer[i],
        })

    return material_props


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



#* This function is an example made by Viktor
# Currently used for checking how D-software integrations work in Viktor
def create_Dfound_example_model(name:str, company_name:str):
    # Create the model with misc. options.
    options = vkt.dfoundations.BearingPilesCalculationOptions(vkt.dfoundations.CalculationType.BEARING_CAPACITY_AT_FIXED_PILE_TIP_LEVEL, False)
    model = vkt.dfoundations.BearingPilesModel(vkt.dfoundations.ConstructionSequence.CPT_INSTALL_EXCAVATION, options, -5.0)
    
    model.create_material("my_material", vkt.dfoundations.SoilType.SAND, 19.0, 19.0, 3.0)

    # Create profile(s).
    layers = [
        vkt.dfoundations.ProfileLayer(0.0, "my_material"),
        vkt.dfoundations.ProfileLayer(-20.0, "my_material")
    ]
    measurements = [(0.0, 10.0), (-20.0, 20.0)]
    model.create_profile('my_profile', layers, 0.0, 0.0, measurements, -5.0, -15.0, 1.0, -10.0, -12.0, -0.11)

    # Create pile type(s).
    model.create_pile_type(
        "my_pile_type",
        vkt.dfoundations.RectPile(1.0, 1.0),
        vkt.dfoundations.PileType.PREFAB_CONCRETE,
        vkt.dfoundations.PileSlipLayer.NONE
    )

    # Create pile(s).
    model.create_pile("my_pile", 0.0, 0.0, -1.0, 1.0, 0.0, 0.0)

    # Generate the input file for the model as if it was generated by D-Foundations.
    # Metadata can be used (not required) to update data such as titles, company, etc.
    metadata = vkt.dfoundations.Metadata(title_1=name, company=company_name)
    foi_file = model.generate_input_file(metadata)

    # Run the analysis with the generated input file (requires worker).
    analysis = vkt.dfoundations.DFoundationsAnalysis(foi_file)
    analysis.execute(300)

    # Obtain the result file.
    # Instead of using the parser, work with the raw file
    fod_file = analysis.get_output_file()
    # Save to a local file (if running locally)
    with open("dfoundations_example_results.fod", "wb") as f:
        f.write(fod_file.getvalue())

    # Read the raw content
    fod_bytes = fod_file.getvalue()
    fod_string = fod_bytes.decode('utf-8')

    result = extract_iteration_results(fod_string)

    # Process the raw string manually
    return result



#* This function is an example made by Viktor
# Currently not used, only for reference
def create_Dset_example_model(self, params):
    # Create model with model type and consolidation type
    model_dset = vkt.dsettlement.Model1D(vkt.dsettlement.CalculationModel.NEN_BJERRUM, vkt.dsettlement.ConsolidationModel.DARCY)

    # Create material(s) - Fixed color definitions
    model_dset.create_material("Sand", 19.0, 21.0, vkt.Color(255, 255, 0), r_ratio=0.0, c_ratio=0.0023, ca=0.0)  # yellow
    model_dset.create_material("Clay", 15.0, 15.0, vkt.Color(128, 128, 128), r_ratio=0.05, c_ratio=0.23, ca=0.02)  # gray

    # Create geometry - layers
    model_dset.update_geometry(-30.0, [(-15.0, "Sand"), (0.0, "Clay")], phreatic_level=-3)

    # Create load(s)
    model_dset.create_uniform_load("Uniform load", 0, 20.0, 1.0)

    # Generate the input file for the model as if it was generated by D-Settlement.
    # Metadata can be used (not required) to update data such as created_by, titles, etc.
    metadata = vkt.dsettlement.Metadata(title_1='Example Model', created_by='VIKTOR')
    input_file = model_dset.generate_input_file(metadata)

    # Run the analysis with the generated input file (requires worker).
    analysis = vkt.dsettlement.DSettlementAnalysis(input_file)
    analysis.execute(300)

    # Obtain the result file.
    sld_file = analysis.get_sld_file()

    # Save to a local file (if running locally)
    with open("dsettl_example_results.fod", "wb") as f:
        f.write(sld_file.getvalue())

    # Read the raw content
    sld_bytes = sld_file.getvalue()
    sld_string = sld_bytes.decode('utf-8')

    result = extract_iteration_results(sld_string)

    return result


# Created Dsettlement model for MDR as one single example
def create_Dset_example_model_MDR(name:str, company_name:str):
    # Create model with model type and consolidation type
    model_dset = vkt.dsettlement.Model1D(vkt.dsettlement.CalculationModel.NEN_BJERRUM, vkt.dsettlement.ConsolidationModel.DARCY, create_default_materials=False)

    # Create material(s) - Fixed with RGB values instead of color names
    model_dset.create_material("Sand_1", 19.0, 21.0, vkt.Color(255, 255, 0), r_ratio=0.0008, c_ratio=0.0023, ca=0.0)  # yellow
    model_dset.create_material("Silty SAND", 19.0, 21.0, vkt.Color(255, 255, 224), r_ratio=0.0017, c_ratio=0.0051, ca=0.0)  # lightyellow
    model_dset.create_material("Silty CLAY", 18.0, 18.0, vkt.Color(128, 128, 128), r_ratio=0.038, c_ratio=0.115, ca=0.0046)  # gray
    model_dset.create_material("CLAY", 17.0, 17.0, vkt.Color(64, 64, 64), r_ratio=0.051, c_ratio=0.153, ca=0.0061)  # darkgray
    model_dset.create_material("Organic CLAY", 15.0, 15.0, vkt.Color(165, 42, 42), r_ratio=0.102, c_ratio=0.307, ca=0.0153)  # brown

    

    # model_dset.update_material("Sand", 19.0, 21.0, vkt.Color(255, 255, 0), r_ratio=0.0008, c_ratio=0.0023, ca=0.0)
    

    # Create geometry - layers
    model_dset.update_geometry(-35.36, [(-4.60, "Sand_1"),
                                        (-5.16, "Organic CLAY"), 
                                        (-5.98, "Sand_1"), 
                                        (-6.94, "Silty SAND"), 
                                        (-9.78, "Sand_1"), 
                                        (-12.00, "Silty CLAY"), 
                                        (-12.76, "Silty SAND"), 
                                        (-13.16, "Sand_1"), 
                                        (-13.64, "Silty SAND"), 
                                        (-14.63, "Sand_1"), 
                                        (-25.15, "Silty CLAY"), 
                                        (-25.55, "CLAY"), 
                                        (-26.38, "Silty CLAY"), 
                                        (-27.83, "CLAY"), 
                                        (-28.16, "Silty CLAY"), 
                                        (-32.06, "Silty SAND"), 
                                        (-33.36, "Sand_1")], 
                                        phreatic_level=-5.6)

    # Create load(s)
    model_dset.create_uniform_load("Uniform load", 0, 20.0, 1.0, -4.60)

    # Generate the input file for the model as if it was generated by D-Settlement.
    # Metadata can be used (not required) to update data such as created_by, titles, etc.
    metadata = vkt.dsettlement.Metadata(title_1='Example Model MDR', created_by='Maureen Danique Klomp')
    
    input_file = model_dset.generate_input_file(metadata)
    # input_file = 

    # Save model to a local file (if running locally)
    with open("dsettl_example_results_MDR.sli", "w") as f:
        f.write(input_file.getvalue().decode('utf-8'))

    # Run the analysis with the generated input file (requires worker).
    analysis = vkt.dsettlement.DSettlementAnalysis(input_file)
    analysis.execute(300)


    # Obtain the result file.
    sld_file = analysis.get_sld_file()

    # Save results to a local file (if running locally)
    with open("dsettl_example_results_MDR.sld", "w") as f:
        f.write(sld_file.getvalue())

    # Read the raw content
    sld_bytes = sld_file.getvalue()
    # sld_string = sld_bytes.decode('utf-8')

    result = extract_iteration_results(sld_bytes)

    return result
