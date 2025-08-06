"""
This is the inmass script for automating the process of calculating materials for each
project in DME. If you have any questions or need assistance, ASK ME!

this script will calculate also the insulation materials for each project.
"""
# Import necessary modules
import math

class RawPart:
    def __init__ (self, name, pn, length, thickness, qty, description, big_dia, small_dia, height, angle):
        self.name = name
        self.pn = pn
        self.length = length
        self.thickness = thickness
        self.qty = qty
        self.description = description
        self.big_dia = big_dia
        self.small_dia = small_dia
        self.height = height
        self.angle = angle


# TODO: function to calculate cones
# function to calculate square feet for a cone part
def calculate_SF_cone(part):

    part_number = part.Number
    print("part_number: ", part_number)
    part_qty = part.Quantity
    print("part_qty: ", part_qty)
    square_feet = 0.0
    # dimensions in Alibre are in mm need to convert to inches
    big_dia = part.GetParameter('D10').Value/25.4  # Convert mm to inches
    small_dia = part.GetParameter('D12').Value/25.4  # Convert mm to inches
    height = part.GetParameter('D7').Value/25.4  # Convert mm to inches 

    tan_num = ((big_dia-small_dia)/2)/height
    alpha = math.atan(tan_num) * 180/ math.pi
    H_heigh = ((big_dia*height)/(big_dia-small_dia))
    R_dia = (H_heigh/math.cos((alpha * math.pi)/180))
    I_heigh = (height/math.cos((alpha * math.pi)/ 180))
    r_dia = R_dia - I_heigh
    theta = (180 * big_dia) / R_dia
    chord = 2 * r_dia * math.sin((theta * math.pi)/ (180 * 2))
    C_hord = 2 * R_dia * math.sin((theta * math.pi)/ (180 * 2))
    sagitta = r_dia * (1 - math.cos(theta * 0.5 * math.pi / 180))
    apothem = r_dia - sagitta
    S_agitta = R_dia * (1 - math.cos(theta * 0.5 * math.pi/ 180))
    blank = 2 * R_dia - S_agitta
    mini = min(S_agitta, blank)
    zero_out = 1 if (theta < 180) else 0
    total_area = round(C_hord * (R_dia - apothem) if (theta < 180) else math.pow((2 * R_dia),2) - 2 * R_dia * mini, 2)
    print("Area Total: ", total_area)
    print("big_dia: {}, small_dia: {}, height: {}".format(big_dia, small_dia, height))
    square_feet = (total_area * 1.05) / 144  # Convert square inches to square feet
    print("Calculated square feet for {}: {:.2f} ft²".format(part.Name, square_feet))
    return square_feet

def calculate_SF_tube(part):

    part_lenth = part.GetParameter('L').Value/25.4  # Convert mm to inches
    print("part_lenth: ", part_lenth)

# TODO: Print assy and subassy.
# Function to get the current assembly
def list_components(assembly, indent=0):
    space = "  " * indent
    # Print parts in this assembly
    for part in assembly.Parts:
        print("{}- {} (Part)".format(space, part.Name))
        if 'tube' in part.Name.lower() and "lag stop" not in part.Name.lower():
            calculate_SF_tube(part) # Calculate square feet for tube parts
        elif 'cone' in part.Name.lower():
            calculate_SF_cone(part) # Calculate square feet for cone parts
           
    for sub in assembly.SubAssemblies:
        print("{}- {} (Assembly)".format(space, sub.Name))
        list_components(sub, indent + 1)

# Main
print("🔍 Listing assembly components...")
assy = CurrentAssembly()

if assy is None:
    print("❌ No assembly is open.")
else:
    print("🧩 Assembly: {}".format(assy.Name))
    list_components(assy)
# calculate_SF_cone(assy)

# TODO: Add a function to calculate the insulation materials.
# TODO: Implement the main logic to iterate through projects and calculate materials.
# TODO: Add error handling.
# TODO: compare BOM with inventory parts.

# TODO: function to calculate mitters
# TODO: function to calculate tubing
# TODO: function to integrate EXCEL files for material data
# TODO: create new excel file with calculated materials
