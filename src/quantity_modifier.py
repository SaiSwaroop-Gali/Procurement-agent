import re


def get_final_quantity(
    recommended_quantity,
    manager_instructions
):

    instructions = manager_instructions.lower()


    # ==================================
    # ADD X MORE
    # Examples:
    # Add 10 more
    # Add 5 units
    # ==================================

    match = re.search(
        r"add\s+(\d+)",
        instructions
    )

    if match:

        extra = int(match.group(1))

        return recommended_quantity + extra


    # ==================================
    # REDUCE BY X
    # Example:
    # Reduce by 3
    # ==================================

    match = re.search(
        r"reduce\s+by\s+(\d+)",
        instructions
    )

    if match:

        reduction = int(match.group(1))

        return max(
            1,
            recommended_quantity - reduction
        )


    # ==================================
    # DECREASE QUANTITY BY X
    # Example:
    # Decrease quantity by 4
    # ==================================

    match = re.search(
        r"decrease.*?(\d+)",
        instructions
    )

    if match:

        reduction = int(match.group(1))

        return max(
            1,
            recommended_quantity - reduction
        )


    # ==================================
    # REMOVE X UNITS
    # Example:
    # Remove 2 units
    # ==================================

    match = re.search(
        r"remove\s+(\d+)",
        instructions
    )

    if match:

        reduction = int(match.group(1))

        return max(
            1,
            recommended_quantity - reduction
        )


    # ==================================
    # ORDER X INSTEAD
    # Example:
    # Order 15 instead of 10
    # ==================================

    match = re.search(
        r"order\s+(\d+)",
        instructions
    )

    if match:

        return int(
            match.group(1)
        )


    # ==================================
    # NO CHANGES
    # ==================================

    return recommended_quantity