from .metal_requests import get_single_metal
from .size_requests import get_single_size
from .style_requests import get_single_style

ORDERS = [
    {
        "id": 1,
        "metalId": 1,
        "sizeId": 2,
        "styleId": 2,
        "jewelryId": 1,
        "timeStamp": 0
    },
    {
        "id": 2,
        "metalId": 1,
        "sizeId": 1,
        "styleId": 3,
        "jewelryId": 2,
        "timeStamp": 0
    },
    {
        "id": 3,
        "metalId": 5,
        "sizeId": 5,
        "styleId": 3,
        "jewelryId": 3,
        "timeStamp": 0
    },
    {
        "id": 4,
        "metalId": 5,
        "sizeId": 5,
        "styleId": 3,
        "jewelryId": 1,
        "timeStamp": 0
    },
    {
        "id": 5,
        "metalId": 2,
        "sizeId": 2,
        "styleId": 2,
        "jewelryId": 2,
        "timeStamp": 0
    },
    {
        "id": 6,
        "metalId": 1,
        "sizeId": 4,
        "styleId": 3,
        "jewelryId": 1,
        "timeStamp": 0
    }
]


def create_order(order):
    # Get the id value of the last order in the list
    max_id = ORDERS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the order dictionary
    order["id"] = new_id

    # Add the order dictionary to the list
    ORDERS.append(order)

    # Return the dictionary with `id` property added
    return order


def get_all_orders():
    return ORDERS

# Function with a single parameter


def get_single_order(id):
    # Variable to hold the found order, if it exists
    requested_order = None

    # Iterate the ORDERS list above. Very similar to the
    # for..of loops you used in JavaScript.
    for order in ORDERS:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if order["id"] == id:
            requested_order = order

            matching_metal = get_single_metal(requested_order["metalId"])
            requested_order["metal"] = matching_metal

            matching_style = get_single_style(requested_order["styleId"])
            requested_order["style"] = matching_style

            matching_size = get_single_size(requested_order["sizeId"])
            requested_order["size"] = matching_size

            requested_order.pop("metalId")
            requested_order.pop("styleId")
            requested_order.pop("sizeId")

    return requested_order


def delete_order(id):
    # Initial -1 value for order index, in case one isn't found
    order_index = -1

    # Iterate the ORDERS list, but use enumerate() so that you
    # can access the index value of each item
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            # Found the order. Store the current index.
            order_index = index

    # If the order was found, use pop(int) to remove it from list
    if order_index >= 0:
        ORDERS.pop(order_index)


def update_order(id, new_order):
    # Iterate the ORDERS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            # Found the order. Update the value.
            ORDERS[index] = new_order
            break
