CRITICAL_PARTS = [

    "Brake Pad",
    "Hydraulic Pump",
    "Main Landing Gear Tire",
    "Nose Wheel Tire",
    "Thrust Reverser Actuator",
    "Fuel Injector Nozzle",
    "Pitot Tube",
    "Flight Data Recorder Battery",
    "Engine Oil Pressure Switch"

]


IMPORTANT_PARTS = [

    "Temperature Sensor",
    "Engine Filter",
    "Cabin Air Filter",
    "Altimeter",
    "Oxygen Mask Pack",
    "APU Spark Plug",
    "Emergency Exit Light Battery",
    "Hydraulic Fluid Canister"

]


def calculate_risk_level(
    part_name,
    current_stock,
    reorder_threshold
):

    ratio = current_stock / reorder_threshold


    # ==================================
    # Critical Aviation Components
    # ==================================

    if part_name in CRITICAL_PARTS:

        if ratio <= 0.8:

            return "HIGH"

        else:

            return "MEDIUM"


    # ==================================
    # Important Components
    # ==================================

    if part_name in IMPORTANT_PARTS:

        if ratio <= 0.6:

            return "HIGH"

        elif ratio <= 0.9:

            return "MEDIUM"

        else:

            return "LOW"


    # ==================================
    # Regular Components
    # ==================================

    if ratio <= 0.5:

        return "HIGH"

    elif ratio <= 0.8:

        return "MEDIUM"

    else:

        return "LOW"