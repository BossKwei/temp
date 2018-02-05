import time
import http.server


class Handler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        print('head')

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b'111111111111111111111111111111111')
        print(self.path)

    def do_POST(self):
        print(self.rfile)


server = http.server.HTTPServer(('127.0.0.1', 8000), Handler)
server.serve_forever()
