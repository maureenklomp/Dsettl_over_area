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


#* Default material properties for soil types
def create_default_mat_prop():
    """
    Create default material properties for geological layers
    """

    material = ['9', '8', '7', '6', '5', '4', '3', '2', '1']
    name = ['Stiff fine-grained SAND', 'Stiff SAND', 'Dense SAND', 'SAND', 'Silty SAND', 'Silty CLAY', 'CLAY', 'Organic CLAY', 'Peat']
    y_dry = [19.0, 19.0, 19.0, 19.0, 18.0, 18.0, 17.0, 13.0, 12.0]  # in kPa
    y_sat = [21.0, 21.0, 21.0, 21.0, 20.0, 18.0, 17.0, 13.0, 12.0]  # in kPa
    color = ['yellow', 'yellow', 'yellow', 'yellow', 'lightyellow', 'gray', 'darkgray', 'brown', 'maroon']
    RR = [0.0008, 0.0008, 0.0008, 0.0008, 0.0017, 0.038, 0.051, 0.102, 0.102]
    CR = [0.0023, 0.0023, 0.0023, 0.0023, 0.0051, 0.115, 0.153, 0.307, 0.307]  
    Ca = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0046, 0.0061, 0.015, 0.015]
    cv = [1.00e-7, 1.00e-7, 1.00e-7, 1.00e-7, 1.70e-8, 3.00e-7, 1.10e-7, 4.00e-8, 6.00e-8]  # in m²/s
    ch_cv = [1, 1, 1, 1, 1, 1, 1, 2, 3]  # dimensionless
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
            'col_9': ch_cv[i],
            'col_10': pop_layer[i],
        })

    return material_props


def create_default_loads():
    """
    Create default load properties for uniform loads on the area
    """

    name = ['Ophoging', 'Zettingscompensatie', 'Overhoogte', 'Ontgraven']
    time_start = [0, 0, 0, 271]
    load_value = [18, 18, 18, -18]
    load_thickness = [1, 0.5, 0.3, 0.3]
    
    loads = []
    for i in range(len(time_start)):
        loads.append({
            'col_1': name[i],
            'col_2': time_start[i],
            'col_3': load_value[i],
            'col_4': load_thickness[i],
        })

    return loads




