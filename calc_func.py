import math


# Function calculates the SF of a cone based on big OD, small OD, & LG using M.F. excel formulas
#@param big_dia uses the big diameter of the cone
#@param small_dia, uses the small diameter of the cone
#@param height, uses the length of the cone
def cone_sf(big_dia, small_dia, height):
    """Calculate square feet for a cone given big diameter, small diameter, and height in inches."""
    tan_num = ((big_dia - small_dia) / 2) / height
    alpha = math.atan(tan_num) * 180 / math.pi
    H_heigh = ((big_dia * height) / (big_dia - small_dia))
    R_dia = (H_heigh / math.cos((alpha * math.pi) / 180))
    I_heigh = (height / math.cos((alpha * math.pi) / 180))
    r_dia = R_dia - I_heigh
    theta = (180 * big_dia) / R_dia
    chord = 2 * r_dia * math.sin((theta * math.pi) / (180 * 2))
    C_hord = 2 * R_dia * math.sin((theta * math.pi) / (180 * 2))
    sagitta = r_dia * (1 - math.cos(theta * 0.5 * math.pi / 180))
    apothem = r_dia - sagitta
    S_agitta = R_dia * (1 - math.cos(theta * 0.5 * math.pi / 180))
    blank = 2 * R_dia - S_agitta
    mini = min(S_agitta, blank)
    total_area = round(C_hord * (R_dia - apothem) if (theta < 180) else math.pow((2 * R_dia), 2) - 2 * R_dia * mini, 2)
    square_feet = (total_area * 1.05) / 144  # Convert square inches to square feet

    return square_feet


# Function calculate the SF of a flange based on the OD = Outer Diameter
#@param od is the flange Outer Diameter
def calc_flange_sf(od):
    flange_sf = round((od * od * 1.2) / 144, 2)  # Convert square inches to square feet
    # if material in 

    return flange_sf

# Function calculates the SF of a sheet metal tube based on the OD and length of the tube
#@param od is the tube/pipe outer diameter
#@param length is the overall length of the tube/pipe
def sheet_metal_tube_sf(od, length):
    """Calculate square feet for sheet metal tube given outer diameter and length in inches."""
    circumference = math.pi * od
    area = circumference * length
    square_feet = (area * 1.05) / 144  # Convert square inches to square feet
    return square_feet

# Function calculates the SF of REGULAR MITER SET (NO TRANSITIONING MITER)
#@param diameter is the outer diameter of the miters example: 10
#@param radious is the radious of the entire miter set example: 9
#@param angle is the complete angle of the elbow miter example: 110
#@param no_miter is how many sections are making that elbow miter example: 5
def regular_miter(diameter, radious, angle, no_miter):
    """Calculate the Square feet for regular miter set. """
    try:
        # Make sure all input values are positive and greater than 0
        if any(x is None for x in [diameter, radious, angle, no_miter]):
            raise ValueError("All inputs must have a value")
        if no_miter == 0:
            raise ZeroDivisionError("Number of miter can NOT be ZERO.")
        if radious <= 0 or diameter <= 0 or angle <= 0:
            raise ValueError("Diameter, Radious, and Angle must be positive")



        ro = radious + (diameter/2)
        ri = radious - (diameter/2)
        if ri <= 0:
            raise ValueError("Inner radious became negative. Check your inputs.")

        theta = angle/no_miter
        chord_big = 2*(ro*(math.sin(((theta*math.pi)/180)/2)))
        chord = 2*(ri*(math.sin(((theta*math.pi)/180)/2)))
        apothem_big = ro*(math.cos((theta*math.pi)/360))
        apothem = ri*(math.cos((theta*math.pi)/360))
        dc = apothem_big - apothem
        perimeter = math.pi * dc
        area = round(((perimeter * chord_big * no_miter * 1.05)/144), 2)

        if not math.isfinite(area) or area <= 0:
            raise ValueError("Calculated area is not a valid real number.")

        return area

    except Exception as e:
        print(f"Error calculating regular miter area: {e}")
        return None
