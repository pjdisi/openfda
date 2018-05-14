import http.server
import socketserver
import http.client
import json

# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 9007


# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)
        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()
            # Send message back to client
        if self.path == "/":
            with open("search.html") as f:
                index = f.read()
                message = index
            self.wfile.write(bytes(message, "utf8"))
        else:
            if "=" in self.path:
                drug = self.path[self.path.find("label")+6:self.path.find("&")]
                limit =self.path[self.path.find("limit")+6:]

                headers = {'User-Agent': 'http-client'}

                conn = http.client.HTTPSConnection("api.fda.gov")
                conn.request("GET", "/drug/label.json?search=generic_name:%s&limit=%s" %(drug,limit), None, headers)
                r1 = conn.getresponse()
                print(r1.status, r1.reason)
                repos_raw = r1.read().decode("utf-8")
                repos = json.loads(repos_raw)
                conn.close()

                with open("htlmlopenfda4.html","w"):
                    self.wfile.write(bytes("<ol>"+"\n","utf8"))
                    for element in repos["results"]:
                        elementli="<li>"+element["openfda"]["brand_name"][0]+"</li>"+"\n"
                        self.wfile.write(bytes(elementli, "utf8"))
                    self.wfile.write(bytes("</ol>","utf8"))
                    #include if brand name is noting the repostory--> print noot found in the html
            else:
                #Error, open the initial page and search for drug and limit
                print("")
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




# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)
        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        with open("htmlopenfda4.html", "r") as f:
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

