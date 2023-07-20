import sqlite3
import json
from models import Metal, Style, Size, Order

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
    # Open a connection to the database
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        if resource == "metals":
            db_cursor.execute("""
            SELECT
                m.id,
                m.metal,
                m.price
            FROM Metals m
            """)

        if resource == "styles":
            db_cursor.execute("""
            SELECT
                st.id,
                st.style,
                st.price
            FROM Styles st
            """)

        if resource == "sizes":
            db_cursor.execute("""
            SELECT
                s.id,
                s.carets,
                s.price
            FROM Sizes s
            """)

        if resource == "orders":
            db_cursor.execute("""
            SELECT
                o.id,
                o.time_stamp,
                o.size_id,
                o.style_id,
                o.metal_id,
                o.jewelry_id,
                m.metal,
                m.price,
                st.style,
                st.price,
                s.carets,
                s.price
            FROM `Orders` o
            JOIN Metals m
                ON m.id = o.metal_id
            JOIN Styles st
                ON st.id = o.style_id
            JOIN Sizes s
                ON s.id = o.size_id
            """)

        response = []
        metals = []
        styles = []
        sizes = []
        orders = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            if resource == "metals":

                metal = Metal(row['id'], row['metal'], row['price'])

                metals.append(metal.__dict__)

                response = metals

            if resource == "styles":

                style = Style(row['id'], row['style'], row['price'])

                styles.append(style.__dict__)

                response = styles

            if resource == "sizes":

                size = Size(row['id'], row['carets'], row['price'])

                sizes.append(size.__dict__)

                response = sizes

            if resource == "orders":

                order = Order(row['id'], row['metal_id'], row['style_id'], row['size_id'],
                              row['jewelry_id'], row['time_stamp'])
                metal = Metal(row['id'], row['metal'], row['price'])
                style = Style(row['id'], row['style'], row['price'])
                size = Size(row['id'], row['carets'], row['price'])

                order.metal = metal.__dict__
                order.style = style.__dict__
                order.size = size.__dict__

                orders.append(order.__dict__)

                response = orders

        return response

def retrieve(resource, id):
    """For GET requests to a single resource"""
    # Open a connection to the database
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        if resource == "metals":
            db_cursor.execute("""
            SELECT
                m.id,
                m.metal,
                m.price
            FROM Metals m
            WHERE m.id = ?
            """, (id, ))

            # Load the single result into memory
            data = db_cursor.fetchone()

            # Create an resource_list instance from the current row
            resource_list = Metal(data['id'], data['metal'], data['price'])

        if resource == "styles":
            db_cursor.execute("""
            SELECT
                st.id,
                st.style,
                st.price
            FROM Styles st
            WHERE st.id = ?
            """, (id, ))

            # Load the single result into memory
            data = db_cursor.fetchone()

            # Create an resource_list instance from the current row
            resource_list = Style(data['id'], data['Style'], data['price'])

        if resource == "sizes":
            db_cursor.execute("""
            SELECT
                s.id,
                s.carets,
                s.price
            FROM Sizes s
            WHERE s.id = ?
            """, (id, ))

            # Load the single result into memory
            data = db_cursor.fetchone()

            # Create an resource_list instance from the current row
            resource_list = Size(data['id'], data['carets'], data['price'])

        if resource == "orders":
            db_cursor.execute("""
            SELECT
                o.id,
                o.metal_id,
                o.style_id,
                o.size_id,
                o.jewelry_id,
                o.time_stamp
            FROM Orders o
            WHERE o.id = ?
            """, (id, ))

            # Load the single result into memory
            data = db_cursor.fetchone()

            # Create an resource_list instance from the current row
            resource_list = Order(data['id'], data['metal_id'], data['style_id'], data['size_id'],
                              data['jewelry_id'], data['time_stamp'])

        return resource_list.__dict__


def expand(response, resource):
    expand_list = DATABASE[f"{resource}s"]

    for single_resource in expand_list:
        if single_resource["id"] == response[f"{resource}_id"]:
            response[f"{resource}"] = single_resource
            response.pop(f"{resource}_id")
            break

    return response


def create(resource, post_body):
    """For POST requests to a collection"""
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        if resource == "metals":
            db_cursor.execute("""
            INSERT INTO Metals
                ( metal, price )
            VALUES
                ( ?, ?);
            """, (post_body['metal'], post_body['price']))

            # The `lastrowid` property on the cursor will return
            # the primary key of the last thing that got added to
            # the database.
            id = db_cursor.lastrowid

            # Add the `id` property to the animal dictionary that
            # was sent by the client so that the client sees the
            # primary key in the response.
            post_body['id'] = id
            response = post_body

        if resource == "styles":
            db_cursor.execute("""
            INSERT INTO Styles
                ( style, price )
            VALUES
                ( ?, ?);
            """, (post_body['style'], post_body['price']))

            # The `lastrowid` property on the cursor will return
            # the primary key of the last thing that got added to
            # the database.
            id = db_cursor.lastrowid

            # Add the `id` property to the animal dictionary that
            # was sent by the client so that the client sees the
            # primary key in the response.
            post_body['id'] = id
            response = post_body

        if resource == "sizes":
            db_cursor.execute("""
            INSERT INTO Sizes
                ( carets, price )
            VALUES
                ( ?, ?);
            """, (post_body['carets'], post_body['price']))

            # The `lastrowid` property on the cursor will return
            # the primary key of the last thing that got added to
            # the database.
            id = db_cursor.lastrowid

            # Add the `id` property to the animal dictionary that
            # was sent by the client so that the client sees the
            # primary key in the response.
            post_body['id'] = id
            response = post_body

        if resource == "orders":
            db_cursor.execute("""
            INSERT INTO Orders
                ( metal_id, style_id, size_id, jewelry_id, time_stamp )
            VALUES
                ( ?, ?, ?, ?, ?);
            """, (post_body['metal_id'], post_body['style_id'], post_body['size_id']
                  , post_body['jewelry_id'], post_body['time_stamp']))

            # The `lastrowid` property on the cursor will return
            # the primary key of the last thing that got added to
            # the database.
            id = db_cursor.lastrowid

            # Add the `id` property to the animal dictionary that
            # was sent by the client so that the client sees the
            # primary key in the response.
            post_body['id'] = id
            response = post_body

    return response


def update(id, post_body):
    """For PUT requests to a single resource"""
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Metals
            SET
                metal = ?,
                price = ?
        WHERE id = ?
        """, (post_body['metal'], post_body['price'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True


def delete(id, resource):
    """For DELETE requests to a single resource"""
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        if resource == "metals":
            db_cursor.execute("""
            DELETE FROM Metals
            WHERE id = ?
            """, (id, ))

        if resource == "styles":
            db_cursor.execute("""
            DELETE FROM Styles
            WHERE id = ?
            """, (id, ))

        if resource == "sizes":
            db_cursor.execute("""
            DELETE FROM Sizes
            WHERE id = ?
            """, (id, ))

        if resource == "orders":
            db_cursor.execute("""
            DELETE FROM Orders
            WHERE id = ?
            """, (id, ))
