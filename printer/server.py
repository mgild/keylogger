import SimpleHTTPServer
import SocketServer

PORT = 8000

def do_GET(self):
    self.send_response(200)
    self.send_header('Access-Control-Allow-Origin', '*')
    self.send_header('Content-Type', 'text/plain');
    self.end_headers()
    return self.path

handler = SimpleHTTPServer.SimpleHTTPRequestHandler
handler.do_GET = do_GET

httpd = SocketServer.TCPServer(("", PORT), handler)

print "serving at port", PORT
httpd.serve_forever()
