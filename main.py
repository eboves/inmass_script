"""
This is the inmass script for automating the process of calculating materials for each
project in DME. If you have any questions or need assistance, ASK ME!

this script will calculate also the insulation materials for each project.
"""
# Import
import math

from pydoc import text
import sys
import clr
from collections import defaultdict

import math
import re
import csv

import os
import datetime

# Import modules
from materials import *
import calc_func
from part_lookup import *




# GLOBAL VARIABLES
INVENTORY_URL = r"C:\Users\EBOVES\Desktop\Scripts_Automation ELVIS Copy\EB_SCRIPTS\DME\inmass_script\INVENTORY LIST.csv"
                  

BOM_URL = r"C:\Users\EBOVES\Desktop\Scripts_Automation ELVIS Copy\EB_SCRIPTS\DME\inmass_script\B25-10078.csv"
            

parts_list = []  # list to store part objects



###################################################### DUMMY CODE STARTS HERE ##########################################################
# TODO: ONLY MITTERS, TUBES, CONES, ELBOWS ARE THE PARTS THAT GET INSULATED.
        # MAKE A LIST OF THE PARTS THAT CONTAIN THOSE KEYWORDS. AND IF A TUBE CONTAINS HB OR LB REMOVE IT FROM LIST.


####################################################### DUMMY CODE ENDS HERE ###########################################################



input_file = "BOM.csv"
output_file = "MaterialSummary.csv"

totals = defaultdict(float)


with open(BOM_URL, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        part_no = row['PART #'].strip()
        desc = row['DESCRIPTION'].upper()
        material = row['MATL'].strip()
        thickness = row['Ga.'].strip()
        part_confi_section = row['Part-Configuration Name']
        qty = float(row['QTY']) if row['QTY'] else 0

        # Default multiplier
        multiplier = 1.0
# Determine if elbow is half or full based on description
        if "ELBOW" in desc and "PIPE" not in desc:
            angle = extract_angle(desc)
            if angle is not None:
                if angle < 45:
                    multiplier = 1  # one half
                else:
                    multiplier = 2  # two halves
            else:
                multiplier = 2  # assume full if unknown
# Determine elbow pipe
        elif "ELBOW PIPE" in desc:
            multiplier = 1  # always 1 per elbow pipe
# Determine tube or pipe and if sheet metal or actual tube/ pipe
        elif "TUBE" in desc or "PIPE" in desc and "PIPE PLUG" not in desc:
            length_in = extract_length_inch(desc)
            if get_sheet_metal_part_no(part_no):
                # print("Part {} is sheet metal tube/pipe.".format(part_no))
                sheetmetal_tube_od = extract_tube_od_sheet_metal(desc) 
                # print('This is sheet metal', sheetmetal_tube_od)
                sf_tube = calc_func.sheet_metal_tube_sf(sheetmetal_tube_od, length_in)
                multiplier = sf_tube
                # print("Square feet", multiplier)
            else:
                if not length_in:
                    print("Length not found in description for part {}.".format(part_no))
                    while True:
                        try:
                            length_in = float(input("Enter length in inches for part {}: ".format(part_no)))
                            tube_od = float(input("Enter outer diameter in inches for part {}: ".format(part_no)))
                            if length_in <= 0 or tube_od <= 0:
                                print("Length and outer diameter must be positive numbers. Please try again.\n")
                                continue
                            # tube_sf = calculations.sheet_metal_tube_sf(tube_od, length_in)
                            tube_sf = calc_func.sheet_metal_tube_sf(tube_od, length_in)
                            multiplier = tube_sf
                            break  # valid input
                        except ValueError:
                            print("Invalid input. Please enter a numeric value only.\n")
                if length_in:
                    multiplier = length_in / 12.0  # inches → feet
                else:
                    multiplier = 0
# Determine cone 
        elif "CONE" in desc:
            # Try to extract dimensions automatically from description
            cone_dims = extract_cone_dimensions(desc)

            if not cone_dims:
                print("Cone dimensions not found in description for part {}.".format(part_no))

                # Keep asking until the user enters valid numeric values
                while True:
                    try:
                        od1 = float(input("Enter big diameter (D10) for cone part {}: ".format(part_no)))
                        od2 = float(input("Enter small diameter (D12) for cone part {}: ".format(part_no)))
                        hgt = float(input("Enter height (D7) for cone part {}: ".format(part_no)))

                        # Validate that dimensions make sense (e.g., positive and od1 > od2)
                        if od1 <= 0 or od2 <= 0 or hgt <= 0:
                            print("All values must be positive numbers. Please try again.\n")
                            continue
                        if od1 <= od2:
                            print("Big diameter must be larger than small diameter. Please try again.\n")
                            continue

                        # Valid input → compute multiplier
                        multiplier = calc_func.cone_sf(od1, od2, hgt)
                        break  # exit input loop

                    except ValueError:
                        print("Invalid input. Please enter numeric values only.\n")
            else:
                # Extracted automatically from text
                big_dia = cone_dims["D10"]
                small_dia = cone_dims["D12"]
                height = cone_dims["D7"]
                multiplier = calc_func.cone_sf(big_dia, small_dia, height) 
# Determine flange and ring
        elif "FLANGE" in desc or "RING" in desc:
            
            flange_od = extract_flange_dimensions(desc)

            if not flange_od:
                print("Flange dimensions not found in description for part {}.".format(part_no))
                while True:
                    try:
                        flange_od = float(input("Enter flange OD for flange part {}: ".format(part_no)))
                        if flange_od <= 0:
                            print("Flange OD must be a positive number. Please try again.\n")
                            continue
                        break  # valid input
                    except ValueError:
                        print("Invalid input. Please enter a numeric value only.\n")
            
            matl = material
            thk = THK_LIST.get(thickness, None)  
            print("THICKNESS", thk)
            flange_sf = calc_func.calc_flange_sf(flange_od)
            part_no = get_plate_part_no(material=matl, thickness=thk)
            print("PART NUMBER", part_no)
            multiplier = flange_sf

# Determine FLEX sections
        elif "FLEX" in desc:
            length_in = extract_length_inch(desc)
            if length_in:
                multiplier = length_in / 12.0  # inches → feet
            else:
                multiplier = 0        
        
# Determine Diffuser
        elif "DIFFUSER" in desc:
            diffuser_od = extract_diffuser_info(part_confi_section)
            # print('DIFFUSER OD',diffuser_od)
            if diffuser_od:
                multiplier = calc_func.calc_flange_sf(diffuser_od)
                # print('SF of Diffuser', multiplier)
            else:
                multiplier = 0


# Determine regular miter set

        elif "MITER" in desc or "MITTER" in desc or "MITERS" in desc or "MITTERS" in desc:
            print("Please enter the information bellow to calculate miter SF.")
            
            diameter = float(input(f"Enter diameter for miter calculation (must be positive and greater than 0){part_no}:"))
            radious = float(input(f"Enter the radious for miter calculation (must be positive and greater than 0) {part_no}: "))
            angle = float(input(f"Enter elbow miter angle (must be positive) {part_no}: "))
            no_miter = float(input(f"Enter the number of miter sections  {part_no}: "))
                        
            multiplier = calc_func.regular_miter(diameter, radious, angle, no_miter)
                  
              



        total_amount = qty * multiplier
        totals[part_no] += total_amount

# Write results
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['PART #', 'TOTAL_MATERIAL'])
    for part_no, total in totals.items():
        writer.writerow([part_no, round(total, 2)])

print("Calculation complete. Results saved to:", output_file)

































"""

The code below is using classes to define different part types and their attributes.
Each class represents a specific part type (e.g., Tube, Pipe, Elbow_Half)


"""

# # class for each part

# class Part(object): # parent class derived from object
#     def __init__(self, part_number, qty, material_used):
#         self.part_number = part_number # part number 
#         self.qty = qty # how many parts
#         self.material_used = material_used # material used for the part
#         self.square_feet = 0.0 # square feet of the part, default to 0.0

#     def __str__(self):
#         return "Part Number: {}, Quantity: {}, Material Used: {}, Square Feet: {:.2f} ft²".format(
#             self.part_number, self.qty, self.material_used, self.square_feet)

# class Tube(Part): # child class derived from Part
#     def __init__(self, part_number, qty, material_used, length, outer_dia, square_feet):
#         super().__init__(part_number, qty, material_used) # call the parent constructor
#         self.length = length # length of the tube
#         self.outer_dia = outer_dia # outer diameter of the tube
#         self.square_feet = square_feet # square feet of the tube

#     def calculate_square_feet(self):
      
#         length = self.length/12  # Convert length from inches to feet
#         return length
    
#     def __str__(self):
#         return "Tube Part Number: {}, Quantity: {}, Material Used: {}, Length: {:.2f} ft, Outer Diameter: {:.2f} in, Square Feet: {:.2f} ft²".format(
#             self.part_number, self.qty, self.material_used, self.length, self.outer_dia, self.square_feet)  

# class Pipe(Tube): # child class derived from Tube
#     def __init__(self, part_number, qty, material_used, length, outer_dia, square_feet):
#         super().__init__(part_number, qty, material_used, length, outer_dia, square_feet) # call the parent constructor

# class Elbow_Half(Part): # child class devired from Part
#     def __init__(self, part_number, qty, material_used, angle):
#         super().__init__(part_number, qty, material_used) # call the parent constructor
#         self.angle = angle # angle of the elbow half
#         # if angle == 45: or less than 45, it counts as 1 full 90 deg half.
#         if angle <= 45:
#             self.qty = qty
#         else: # if angle is more than 45, it counts as 2 full 90 deg halfs.
#             self.qty = qty * 2

#         # return self.qty

#         def __str__(self):
#             return "Elbow Half Part Number: {}, Quantity (90 deg halves): {}, Material Used: {}, Angle: {} deg".format(
#                 self.part_number, self.qty, self.material_used, self.angle)

# class Elbow_Pipe(Elbow_Half): # child class derived from Elbow_Half
#     def __init__(self, part_number, qty, material_used, angle):
#         super().__init__(part_number, qty, material_used, angle) # call the parent constructor
#         # here angle does not matter since its a full elbow.

# class Cone(Part): # child class derived from Part
#     def __init__(self, part_number, qty, material_used, big_dia, small_dia, height, square_feet):
#         super().__init__(part_number, qty, material_used) # call the parent constructor
#         self.big_dia = big_dia # big diameter of the cone
#         self.small_dia = small_dia # small diameter of the cone
#         self.height = height # height of the cone
#         self.square_feet = square_feet # square feet of the cone

#     def __str__(self):
#         return "Cone Part Number: {}, Quantity: {}, Material Used: {}, Big Diameter: {:.2f} in, Small Diameter: {:.2f} in, Height: {:.2f} in, Square Feet: {:.2f} ft²".format(
#             self.part_number, self.qty, self.material_used, self.big_dia, self.small_dia, self.height, self.square_feet)

# class Flange(Part): # child class derived from Part
#     def __init__(self, part_number, qty, material_used, dia, thickness, square_feet):
#         super().__init__(part_number, qty, material_used) # call the parent constructor
#         self.dia = dia # diameter of the flange
#         self.thickness = thickness # thickness of the flange
#         self.square_feet = square_feet # square feet of the flange
    
#     def __str__(self):
#         return "Flange Part Number: {}, Quantity: {}, Material Used: {}, Diameter: {:.2f} in, Thickness: {:.2f} in, Square Feet: {:.2f} ft²".format(
#             self.part_number, self.qty, self.material_used, self.dia, self.thickness, self.square_feet)

# # TODO: open CSV files

# # function to extract numbers and hyphen value from the last column of the BOM
# # @param part_name: string, the part name from the BOM
# # @return: tuple, (list of numbers in the part name, hyphen value as float or None)
# def part_info(part_name):

#     number_part = [float(x) for x in re.findall(r'\d+\.?\d*', part_name)] # Extract all numbers from the part name

#     hyphen_match = re.search(r'-\s*([\d.]+)', part_name) # Extract the number after the hyphen
#     hyphen_value = float(hyphen_match.group(1)) if hyphen_match else None

#     return number_part, hyphen_value # return the list of numbers and the hyphen value


# # function to read the inventory CSV file and get the part numbers, descriptions, and unit measures
# def inventory_csv():  

#     with open(INVENTORY_URL, mode ='r', encoding='utf-8')as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             bom_part_number = row[0]
#             # print("BOM Part Number:", bom_part_number)
#             description = row[1]
#             # print("Description:", description)
#             unit_measure = row[3]
#             # print("Unit of Measure:", unit_measure)

# # when the BOM is added, it will get the raw number it needs to match with the inventory part number.            
# def bom_csv():

#     bom_list = {}

#     pattern = re.compile(r'-\s*([\d.]+)')  # Pattern to match '- <number>'

#     with open(BOM_URL, mode = "r", encoding="utf-8") as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             bom_part_number = row["PART #"]
#             # print("BOM Part Number:", bom_part_number)
#             bom_qty = row["QTY"]
#             # print("BOM Quantity:", bom_qty)

# # this section extracts the value after the hyphen in the "Part-Configuration Name" column
#             part_name = row["Part-Configuration Name"]
#             number_part = [float(x) for x in re.findall(r'\d+\.?\d*', part_name)] # Extract all numbers from the part name
          
#             bom_list[bom_part_number] = [part_name,bom_qty, number_part] # Store part name, quantity, and extracted numbers in the bom_list dictionary
#     # print(bom_list)

#     return bom_list


# def calculations():

#     bom_list = bom_csv()
#     part_obj = None


#     for part_number, details in bom_list.items():
#         part_name = details[0]
#         bom_qty = int(details[1])
#         value = details[2]
#         # print("Part Number: {}, Part Name: {}, BOM Quantity: {}, Extracted Value: {}".format(part_number, part_name, bom_qty, value))


#         if 'tube' in part_name.lower():
#             part_obj = Tube(part_number, bom_qty, '316L', length=value[-1], outer_dia=value[0], square_feet=0.0)
#             sq_ft = part_obj.calculate_square_feet()
#             print("Calculated square feet for tube part {}: {:.2f} ft²".format(part_number, sq_ft))
#             parts_list.append(part_obj)

#         elif re.search(r'\bpipe\b', part_name, re.IGNORECASE) and not re.search(r'\belbow\b', part_name, re.IGNORECASE):
#             part_obj = Pipe(part_number, bom_qty, '316L', length=value[-1], outer_dia=value[0], square_feet=0.0)
#             sq_ft = part_obj.calculate_square_feet()
#             print("Calculated square feet for pipe part {}: {:.2f} ft²".format(part_number, sq_ft))
#             parts_list.append(part_obj)

#         elif re.search(r'\belbow\b', part_name, re.IGNORECASE) and not re.search(r'\bpipe\b', part_name, re.IGNORECASE):
#             part_obj = Elbow_Half(part_number, bom_qty, "316L", angle=value[-1])
#             print("Elbow Half Part: {}, Quantity (90 deg halves): {}".format(part_number, part_obj.qty))
#             parts_list.append(part_obj)
#         elif 'elbow pipe' in part_name.lower():
#             part_obj = Elbow_Pipe(part_number, bom_qty, "316L", angle=value[-1])  # Full elbow assumed to be 90 degrees
#             print("Elbow Pipe Part: {}, Quantity: {}".format(part_number, part_obj.qty))
#             parts_list.append(part_obj)
#         elif 'cone' in part_name.lower():
#             # Here you would call the function to calculate square feet for cone parts
#             print("Calculating square feet for cone part:", part_name)
#         # Add more conditions for other part types as needed


# calculations()
# print("Total parts processed:")
# for part in parts_list:
#     print(part)
# # bom_csv()




































































# # TODO: function to calculate cones
# # function to calculate square feet for a cone part
# def calculate_SF_cone(part):

#     part_number = part.Number
#     print("part_number: ", part_number)
#     part_qty = part.Quantity
#     print("part_qty: ", part_qty)
#     square_feet = 0.0
#     # dimensions in Alibre are in mm need to convert to inches
#     big_dia = part.GetParameter('D10').Value/25.4  # Convert mm to inches
#     small_dia = part.GetParameter('D12').Value/25.4  # Convert mm to inches
#     height = part.GetParameter('D7').Value/25.4  # Convert mm to inches 

#     tan_num = ((big_dia-small_dia)/2)/height
#     alpha = math.atan(tan_num) * 180/ math.pi
#     H_heigh = ((big_dia*height)/(big_dia-small_dia))
#     R_dia = (H_heigh/math.cos((alpha * math.pi)/180))
#     I_heigh = (height/math.cos((alpha * math.pi)/ 180))
#     r_dia = R_dia - I_heigh
#     theta = (180 * big_dia) / R_dia
#     chord = 2 * r_dia * math.sin((theta * math.pi)/ (180 * 2))
#     C_hord = 2 * R_dia * math.sin((theta * math.pi)/ (180 * 2))
#     sagitta = r_dia * (1 - math.cos(theta * 0.5 * math.pi / 180))
#     apothem = r_dia - sagitta
#     S_agitta = R_dia * (1 - math.cos(theta * 0.5 * math.pi/ 180))
#     blank = 2 * R_dia - S_agitta
#     mini = min(S_agitta, blank)
#     zero_out = 1 if (theta < 180) else 0
#     total_area = round(C_hord * (R_dia - apothem) if (theta < 180) else math.pow((2 * R_dia),2) - 2 * R_dia * mini, 2)
#     print("Area Total: ", total_area)
#     print("big_dia: {}, small_dia: {}, height: {}".format(big_dia, small_dia, height))
#     square_feet = (total_area * 1.05) / 144  # Convert square inches to square feet
#     print("Calculated square feet for {}: {:.2f} ft²".format(part.Name, square_feet))
#     return square_feet

# def calculate_SF_tube(part):


#     faces = part.Bodies.Item(0).Faces
#     edges = part.Bodies.Item(0).Edges
#     print("edges: ", edges.Count)
#     print("faces: ", faces.Count)  
    
#     # for i, f in enumerate(faces):
#     #     print("\nFace", i+1)
#     #     surf = f.GetAdjoiningFaces()
#     #     print("Surface Type:", surf.Type)
#     #     print(" Area:", f.Area)
#         # print("Face {}: Area = {:.2f}".format(i+1, f.Area))
#     # # part_lenth = part.GetParameter('L').Value/25.4  # Convert mm to inches
#     # # print("part_lenth: ", part_lenth)
#     # part_face = part.GetFaces()
#     # print("part_face: ", part_face)
#     # print(dir(part.GetFaces()))
#     # # print("part_face: ", part_face)
#     # # faces_list = part.GetHashCode()
#     # # print("HASH CODE: ", faces_list)
#     # # for face in faces_list:
#     # #     print("faces: ", face.Area)
   



# # TODO: Print assy and subassy.
# # Function to get the current assembly
# def list_components(assembly, indent=0):
#     space = "  " * indent
#     # Print parts in this assembly
#     for part in assembly.Parts:
#         print("{}- {} (Part)".format(space, part.Name))
#         if 'tube' in part.Name.lower() and "lag stop" not in part.Name.lower():
#             calculate_SF_tube(part) # Calculate square feet for tube parts
#         elif 'cone' in part.Name.lower():
#             calculate_SF_cone(part) # Calculate square feet for cone parts
           
#     for sub in assembly.SubAssemblies:
#         print("{}- {} (Assembly)".format(space, sub.Name))
#         list_components(sub, indent + 1)

# # Main
# print("🔍 Listing assembly components...")
# assy = CurrentAssembly()

# if assy is None:
#     print("❌ No assembly is open.")
# else:
#     print("🧩 Assembly: {}".format(assy.Name))
#     list_components(assy)
# # calculate_SF_cone(assy)

# # TODO: Add a function to calculate the insulation materials.
# # TODO: Implement the main logic to iterate through projects and calculate materials.
# # TODO: Add error handling.
# # TODO: compare BOM with inventory parts.

# # TODO: function to calculate mitters
# # TODO: function to calculate tubing
# # TODO: function to integrate EXCEL files for material data
# # TODO: create new excel file with calculated materials
