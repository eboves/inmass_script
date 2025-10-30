import re

# Extract angle in degrees the "DESCRIPTION" column of the CSV file.
#@param text is the item description string from the DESCRIPTION column
def extract_angle(text):
    """Extract degree value from a text like '90 DEG.' or '63 DEG'."""
    match = re.search(r'(\d+)\s*DEG', text.upper())
    return int(match.group(1)) if match else None

# Extract the length of a part in inches from the "DESCRIPTION" column of the CSV file.
#@param text is the item description string from the DESCRIPTION column
def extract_length_inch(text):
    """Extract length in inches from text like '21.25 LG'."""
    match = re.search(r'(\d+(\.\d+)?)\s*LG', text.upper())
    return float(match.group(1)) if match else None



# Extract cone dimensions in inches from the "DESCRIPTION" column of the CSV file.
#@param text is the item description string from the DESCRIPTION column
def extract_cone_dimensions(text):
    """Extract cone dimensions from text like 'CONE 6.00 X 5.00 X 0.38LG'."""
    match = re.search(r'CONE\s+(\d+(\.\d+)?)\s+X\s+(\d+(\.\d+)?)\s+X\s+(\d+(\.\d+)?)LG', text.upper())
    if match:
        return {
            "D10": float(match.group(1)),  # Big Diameter
            "D12": float(match.group(3)),  # Small Diameter
            "D7": float(match.group(5))     # Height
        }
    return None

# Extract flange dimensions in inches from the "DESCRIPTION" column of the CSV file.
#@param text is the item description string from the DESCRIPTION column
def extract_flange_dimensions(text):
    """Extract flange dimensions from text like 'FLANGE 6OD'."""
   
    match = re.search(r'(\d+(?:\.\d+)?)\s*OD', text.upper())
    if match:
        number = float(match.group(1))  # get the numeric value as a float
        return number
    else:
        print("No match found")
    # Extract flange dimensions from text like 'FLANGE 6.00 DIA X 0.38THK'.
    # if after - only 5 numbers, add 1 0 at the end.
    # 14,316L,MATTE,1,,A94-020500,WHSE,"FLANGE TURBO ADAPTER",3/4,,A94-020500

# extract the OD of a tube/pipe from Tube, 8.00 x 12.00 LG
#@param text is the item description as shown above
def extract_tube_od_sheet_metal(text):
    """ Extract tube OD from text like Tube, 8.00"""
    match = re.search(r'(\d+(?:\.\d+)?)', text)
    return float(match.group(1)) if match else None
    
# extract the OD of the diffuser from R12-1028EVST
#@param text is the item description as shown above
def extract_diffuser_info(text):
    """ Extract the OD of the diffuser from R12-1028"""
    match = re.search(r'R(\d+)-', text)
    return float(match.group(1)) if match else None