DATABASE = {
    "metals": [
        {
            "id": 1,
            "metal": "Sterling Silver",
            "price": 12.42
        },
        {
            "id": 2,
            "metal": "14K Gold",
            "price": 736.4
        },
        {
            "id": 3,
            "metal": "24K Gold",
            "price": 1258.9
        },
        {
            "id": 4,
            "metal": "Platinum",
            "price": 795.45
        },
        {
            "id": 5,
            "metal": "Palladium",
            "price": 1241
        }
    ],
    "orders": [
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
    ],
    "sizes": [
        {
            "id": 1,
            "carets": 0.5,
            "price": 405
        },
        {
            "id": 2,
            "carets": 0.75,
            "price": 782
        },
        {
            "id": 3,
            "carets": 1,
            "price": 1470
        },
        {
            "id": 4,
            "carets": 1.5,
            "price": 1997
        },
        {
            "id": 5,
            "carets": 2,
            "price": 3638
        }
    ],
    "styles": [
        {
            "id": 1,
            "style": "Classic",
            "price": 500
        },
        {
            "id": 2,
            "style": "Modern",
            "price": 710
        },
        {
            "id": 3,
            "style": "Vintage",
            "price": 965
        }
    ]
}


def get_price(resource, requested_resource):

    if requested_resource is not None:
        single_response = requested_resource

    response = DATABASE[resource]
    metal_list = DATABASE["metals"]
    style_list = DATABASE["styles"]
    size_list = DATABASE["sizes"]

    for single_response in response:
        for metal in metal_list:
            if single_response["metalId"] == metal["id"]:
                matching_metal = metal
                break

        for style in style_list:
            if single_response["styleId"] == style["id"]:
                matching_style = style
                break

        for size in size_list:
            if single_response["sizeId"] == size["id"]:
                matching_size = size
                break

        single_response["price"] = matching_metal["price"] + \
            matching_style["price"] + \
            matching_size["price"]

    return response


def all(resource):
    """For GET requests to collection"""
    if resource == "orders":
        get_price(resource, None)

    return DATABASE[resource]


def retrieve(resource, id):
    """For GET requests to a single resource"""
    # Variable to hold the found animal, if it exists
    requested_resource = None

    resource_list = DATABASE[resource]

    for single_resource in resource_list:
        if single_resource["id"] == id:
            requested_resource = single_resource
            break

    if resource == "orders":
        get_price(resource, requested_resource)

    return requested_resource


def expand(response, resource):
    expand_list = DATABASE[f"{resource}s"]

    for single_resource in expand_list:
        if single_resource["id"] == response[f"{resource}Id"]:
            response[f"{resource}"] = single_resource
            response.pop(f"{resource}Id")
            break

    return response


def create(resource, post_body):
    """For POST requests to a collection"""
    resource_list = DATABASE[resource]

    max_id = resource_list[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the dictionary
    post_body["id"] = new_id

    # Add the new resource dictionary to the list
    resource_list.append(post_body)

    # Return the dictionary with `id` property added
    return post_body


def update(id, resource, post_body):
    """For PUT requests to a single resource"""
    # Iterate the nested list, but use enumerate() so that
    # you can access the index value of each item.
    resource_list = DATABASE[resource]

    for index, single_resource in enumerate(resource_list):
        if single_resource["id"] == id:
            # Found the single_resource. Update the value.
            resource_list[index] = post_body
            break


def delete(id, resource):
    """For DELETE requests to a single resource"""
    resource_list = DATABASE[resource]

    resource_index = -1

    # Iterate the nested list, but use enumerate() so that you
    # can access the index value of each item
    for index, single_resource in enumerate(resource_list):
        if single_resource["id"] == id:
            # Found the single_resource. Store the current index.
            resource_index = index

    # If the resource was found, use pop(int) to remove it from list
    if resource_index >= 0:
        resource_list.pop(resource_index)
