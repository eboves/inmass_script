# Sheet metal material part numbers based on material and thickness
SHEET_METAL = {
    '316L': {
        0.075: '111-003000', # 14 GA SHEET METAL
        0.105: '111-004000', # 12 GA SHEET METAL
        0.120: '111-014000', # 11 GA SHEET METAL
    },
    'AL6XN': {
        0.075: '111-006000', # 14 GA SHEET METAL SMO
        0.105: '111-007000', # 12 GA SHEET METAL SMO
    },
    'CUNI': {
        0.075: '111-008900',  # 14 GA SHEET METAL CUNI
    }
}

SHEET_METAL_RAW_MATL = ['111-003000', '111-004000', '111-014000', '111-006000', '111-007000', '111-008900']

# Plate metal material part numbers based on material and thickness
PLATE_METAL = {
    '316L': {
        0.25: '110-005000',
        0.38: '110-006000',
        0.50: '110-007000',
        0.75: '110-028100',
        1.00: '110-034000',
    },
    '304L': {
        0.25: '110-001100',
        0.38: '110-001000',
        0.50: '110-002000',
        0.75: '110-028000',
    },
    'AL6XN': {
        0.25: '110-008000',
        0.38: '110-020000',
        0.50: '110-021000',
    }
}

# Thickness lookup list
THK_LIST = {
    '16': 0.060,
    '14': 0.075,
    '12': 0.105,  
    '11': 0.120,
    '1/8': 0.13,
    '1/4': 0.250,
    '3/8': 0.38,
    '1/2': 0.500,
    '3/4': 0.750,
    '1': 1.000,

}

# Insulation type
INSULATION_TYPE = {
    0: 'BLANKET',
    1: 'LAGGING',
}

# Insulation layer
INSULATION_LAYER = {
    0: 'SINGLE',
    1: 'DOUBLE',
}

# Insulation material part number
INSULATION_MAT_THK = {
    'temp_mat': {
        0.50: '010-001000',
        1.00: '010-002000',
    },
    'silcosoft':{
        0.50: '010-400000',
        1.00: '010-500000',
    },
    'ceramic_fiber':{
        1.00: '010-009000',
        2.00: '010-009100'
    }
}

INSULATION_OTHER = {
    'wire_mesh': '010-021000',
    'stevens_cloth': '010-006000',
    'silicone_cloth_grey': '010-008000',
    'silicone_cloth_black': '010-008100',
    'silicone_cloth_flat_black': '010-008300',
    'silicone_cloth_white': '010-014000',
    'silicone_cloth_mirror': '010-011000',
    'pre_preg': '010-900000' # This material goes on all insulations
}



# Function to get sheet metal part number based on material and thickness. the info is fetched from the material.py file
#@param material is either 316L, AL6XN, CUNI
#@param thickness is the thickness of the sheet metal in inches
def get_plate_part_no(material, thickness):
    """Get plate part number based on material and thickness."""
    part_number = PLATE_METAL.get(material, {}).get(thickness, None)
    return part_number

# function check if part number is in sheet metal raw material list
#@param part_number is the part number to check
def get_sheet_metal_part_no(part_number):
    """Check if part number is in sheet metal raw material list."""
    if part_number in SHEET_METAL_RAW_MATL:
        return True
    else:
        return False
