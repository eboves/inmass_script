"""
This is the inmass script for automating the process of calculating materials for each
project in DME. If you have any questions or need assistance, ASK ME!

this script will calculate also the insulation materials for each project.
"""

# TODO: Print assy and subassy.

def calculate_SF_cone(part):
    square_feet = 0.0
    # for part in assembly.Parts:
    #     if "cone" in part.Name.lower():
    big_dia = part.GetParameter('D10').Value
    small_dia = part.GetParameter('D12').Value
    height = part.GetParameter('D7').Value
            # # Assuming the part has a method to calculate its surface area
            # surface_area = part.calculate_surface_area()
            # print("Surface area of {}: {:.2f} m²".format(part.Name, surface_area))
    square_feet = big_dia * small_dia * height * 3.1416
    print("Calculated square feet for {}: {:.2f} ft²".format(part.Name, square_feet))
    return square_feet

def list_components(assembly, indent=0):
    space = "  " * indent

    # Print parts in this assembly
    for part in assembly.Parts:
        print("{}- {} (Part)".format(space, part.Name))
        if 'cone' in part.Name.lower():
            calculate_SF_cone(part)

    # Print subassemblies and go deeper recursively
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
    calculate_SF_cone(assy)

# TODO: Add a function to calculate the insulation materials.
# TODO: Implement the main logic to iterate through projects and calculate materials.
# TODO: Add error handling.
# TODO: compare BOM with inventory parts.
# TODO: function to calculate cones
# TODO: function to calculate mitters
# TODO: function to calculate tubing
# TODO: function to integrate EXCEL files for material data
# TODO: create new excel file with calculated materials
