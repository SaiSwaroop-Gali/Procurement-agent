def recommend_order_quantity(current_stock, reorder_threshold):
    """
    Maintain inventory of the threshold.
    Returns the quantity to order.
    """

    target_stock = reorder_threshold * 1.25

    order_quantity = target_stock - current_stock

    return max(int(order_quantity + 0.5), 0)