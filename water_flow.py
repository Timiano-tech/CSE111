# water_flow.py
# working on fixing the formulas for the water pressure project
# added a function at the bottom to convert to psi since that's what we use here

PVC_SCHED80_INNER_DIAMETER = 0.28687 # (meters)  11.294 inches
PVC_SCHED80_FRICTION_FACTOR = 0.013  # (unitless)
SUPPLY_VELOCITY = 1.65               # (meters / second)
HDPE_SDR11_INNER_DIAMETER = 0.048692 # (meters)  1.917 inches
HDPE_SDR11_FRICTION_FACTOR = 0.018   # (unitless)
HOUSEHOLD_VELOCITY = 1.75            # (meters / second)
WATER_DENSITY=998.2                  # density of water (998.2 kilogram / meter^3)

# added these constants after reading the assignment again
GRAVITY = 9.80665
VISCOSITY = 0.0010016

def main():
    tower_height = float(input("Height of water tower (meters): "))
    tank_height = float(input("Height of water tank walls (meters): "))
    length1 = float(input("Length of supply pipe from tank to lot (meters): "))
    quantity_angles = int(input("Number of 90° angles in supply pipe: "))
    length2 = float(input("Length of pipe from supply to house (meters): "))
    
    water_height = water_column_height(tower_height, tank_height)
    pressure = pressure_gain_from_water_height(water_height)
    diameter = PVC_SCHED80_INNER_DIAMETER
    friction = PVC_SCHED80_FRICTION_FACTOR
    velocity = SUPPLY_VELOCITY
    reynolds = reynolds_number(diameter, velocity)
    loss = pressure_loss_from_pipe(diameter, length1, friction, velocity)
    pressure += loss
    loss = pressure_loss_from_fittings(velocity, quantity_angles)
    pressure += loss
    loss = pressure_loss_from_pipe_reduction(diameter,
            velocity, reynolds, HDPE_SDR11_INNER_DIAMETER)
    pressure += loss
    diameter = HDPE_SDR11_INNER_DIAMETER
    friction = HDPE_SDR11_FRICTION_FACTOR
    velocity = HOUSEHOLD_VELOCITY
    loss = pressure_loss_from_pipe(diameter, length2, friction, velocity)
    pressure += loss
    
    # convert to psi and print both
    psi = kpa_to_psi(pressure)
    print(f"\nPressure at house: {pressure:.1f} kilopascals")
    print(f"Pressure at house: {psi:.1f} psi")

def water_column_height(tower_height, tank_height):
    # this one was actually correct already
    return tower_height + 3 * tank_height / 4

def pressure_gain_from_water_height(height):
    # fixed this - it was just returning 0 before
    # formula: P = density * gravity * height / 1000
    pressure = (WATER_DENSITY * GRAVITY * height) / 1000
    return pressure

def pressure_loss_from_pipe(pipe_diameter, pipe_length, friction_factor, fluid_velocity):
    # the denominator was 200 but should be 2000 according to the formula
    numerator = -friction_factor * pipe_length * WATER_DENSITY * fluid_velocity ** 2
    denominator = 2000 * pipe_diameter
    return numerator / denominator

def pressure_loss_from_fittings(fluid_velocity, quantity_fittings):
    # i messed this up - it's velocity squared not velocity times 2
    # formula: -0.04 * density * v^2 * n / 2000
    return -0.04 * WATER_DENSITY * fluid_velocity ** 2 * quantity_fittings / 2000

def reynolds_number(hydraulic_diameter, fluid_velocity):
    # had to look up the formula for this one
    # R = (density * diameter * velocity) / viscosity
    R = (WATER_DENSITY * hydraulic_diameter * fluid_velocity) / VISCOSITY
    return R

def pressure_loss_from_pipe_reduction(larger_diameter, fluid_velocity, reynolds_number, smaller_diameter):
    # this one had a +1 but the formula says it should be -1
    # took me forever to find that bug
    k = (0.1 + 50 / reynolds_number) * ((larger_diameter / smaller_diameter) ** 4 - 1)
    return -k * WATER_DENSITY * fluid_velocity ** 2 / 2000

def kpa_to_psi(kpa):
    # extra function to convert to psi
    # 1 kPa is about 0.145038 psi
    return kpa * 0.145038

if __name__ == "__main__":
    main()