import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from repository import retrieve, all, create, update, delete, expand
# Import this stdlib package first
from urllib.parse import urlparse

method_mapper = {
    "metals": {"single": retrieve, "all": all, "create": create, "update": update, "delete": delete},
    "sizes": {"single": retrieve, "all": all, "create": create, "update": update, "delete": delete},
    "styles": {"single": retrieve, "all": all, "create": create, "update": update, "delete": delete},
    "orders": {"single": retrieve, "all": all, "create": create, "update": update, "delete": delete}
}


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server"""

    def get_all_or_single(self, resource, id):
        if id is not None:
            response = method_mapper[resource]["single"](resource, id)

            if response is not None:
                self._set_headers(200)
            else:
                self._set_headers(404)
                response = ''
        else:
            self._set_headers(200)
            response = method_mapper[resource]["all"](resource)

        return response

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        response = None
        (resource, id, query_params) = self.parse_url(self.path)
        response = self.get_all_or_single(resource, id)

        if "_expand=metalId" in query_params:
            expand(response, "metal")
        if "_expand=styleId" in query_params:
            expand(response, "style")
        if "_expand=sizeId" in query_params:
            expand(response, "size")

        self.wfile.write(json.dumps(response).encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id, query_params) = self.parse_url(self.path)

        if resource == "orders":
            response = method_mapper[resource]["create"](resource, post_body)
            self._set_headers(201)
            # Encode the new animal and send in response
            self.wfile.write(json.dumps(response).encode())
            return

        self._set_headers(403)
        self.wfile.write("Creation Forbidden".encode())

    # A method that handles any PUT request.
    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id, query_params) = self.parse_url(self.path)

        if resource == "metals":
            self._set_headers(204)
            method_mapper[resource]["update"](id, resource, post_body)
            self.wfile.write("".encode())
            return

        self._set_headers(403)
        self.wfile.write("Alteration Forbidden".encode())

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
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

    def parse_url(self, path):
        url_components = urlparse(path)
        path_params = url_components.path.strip("/").split("/")
        query_params = url_components.query.split("&")
        resource = path_params[0]
        id = None

        try:
            id = int(path_params[1])
        except IndexError:
            pass
        except ValueError:
            pass

        return (resource, id, query_params)

    def do_DELETE(self):

        # Parse the URL
        (resource, id, query_params) = self.parse_url(self.path)

        method_mapper[resource]["delete"](id, resource)

        # Set a 204 response code
        self._set_headers(204)
        self.wfile.write("".encode())


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
