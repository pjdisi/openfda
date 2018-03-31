IP = "localhost"  # Localhost means "I": your local machine
PORT = 9007
import http.server
import socketserver
import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?&limit=10", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)
names = []

for element in repos["results"]:
    if element["openfda"]=={}:
        names.append("")
    else:
        names.append(element["openfda"]["generic_name"][0])


intro="<ol>"+"\n"
end ="</ol>"+"\n"
with open("htmlopenfda3.html","w") as f:
    f.write(intro)
    for element in names:
        elementli = "<li>" + element + "</li>" + "\n"
        f.write(elementli)
    f.write(end)


# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)
        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        with open("htmlopenfda3.html", "r") as f:
             message= f.read()
        self.wfile.write(bytes(message, "utf8"))
        print("File served!")
        return


# Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
print("")
print("Server stopped!")

