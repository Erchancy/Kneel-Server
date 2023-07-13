import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_metals, get_single_metal,\
    get_all_sizes, get_single_size,\
    get_all_styles, get_single_style,\
    get_all_orders, get_single_order, create_order, delete_order, update_order


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def do_GET(self):
        """Handles GET requests to the server """

        response = {}  # Default response

        # Parse the URL and capture the tuple that is returned
        (resource, id) = self.parse_url(self.path)

        if resource == "metals":
            if id is not None:
                response = get_single_metal(id)

            else:
                response = get_all_metals()

        elif resource == "sizes":
            if id is not None:
                response = get_single_size(id)

            else:
                response = get_all_sizes()

        elif resource == "styles":
            if id is not None:
                response = get_single_style(id)

            else:
                response = get_all_styles()

        elif resource == "orders":
            if id is not None:
                response = get_single_order(id)

            else:
                response = get_all_orders()

        if response is None:
            self._set_headers(404)
            response = {"message": f'{"That metal is not currently in stock for jewelry." if resource == "metals" else ""}{"That order was never placed, or was cancelled." if resource == "orders" else ""}'}

        else:
            # Set the response code to 'Ok'
            self._set_headers(200)

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Handles POST requests to the server """
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new order
        new_order = None

        if resource == "orders":
            if post_body.get("metalId") is None:
                self._set_headers(400)
                response = {"message": " metalId is required "}
                self.wfile.write(json.dumps(response).encode())
                return
            if post_body.get("sizeId") is None:
                self._set_headers(400)
                response = {"message": " sizeId is required "}
                self.wfile.write(json.dumps(response).encode())
                return
            if post_body.get("styleId") is None:
                self._set_headers(400)
                response = {"message": " styleId is required "}
                self.wfile.write(json.dumps(response).encode())
                return
            if post_body.get("jewelryId") is None:
                self._set_headers(400)
                response = {"message": " jewelryId is required "}
                self.wfile.write(json.dumps(response).encode())
                return
            if post_body.get("timestamp") is None:
                self._set_headers(400)
                response = {"message": " timestamp is required "}
                self.wfile.write(json.dumps(response).encode())
                return
            
            new_order = create_order(post_body)
            response = new_order

        self._set_headers(201)
        self.wfile.write(json.dumps(response).encode())

    # A method that handles any PUT request.
    def do_PUT(self):
        self._set_headers(403)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Update a single order from the list
        if resource == "orders":
            response = {"message": " Modification of orders is forbidden "}

        # Encode the new order and send in response
        self.wfile.write(json.dumps(response).encode())

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single order from the list
        if resource == "orders":
            delete_order(id)

        self.wfile.write("".encode())

    def parse_url(self, path):
        # Just like splitting a string in JavaScript. If the
        # path is "/orders/1", the resulting list will
        # have "" at index 0, "orders" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        # Try to get the item at index 2
        try:
            # Convert the string "1" to the integer 1
            # This is the new parseInt()
            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /orders
        except ValueError:
            pass  # Request had trailing slash: /orders/

        return (resource, id)  # This is a tuple


# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
