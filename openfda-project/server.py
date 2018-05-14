import socketserver
import http.server
import json
import http.client
socketserver.TCPServer.allow_reuse_address = True
# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 8000



class OpenFDAClient():
    limit=None
    repostory= None
    def two_params_request(self,variable,input,limit):
        #variable can be active_ingredient or openfda.manufacturer_name
        OpenFDAClient.limit=limit
        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json?search=%s:%s&limit=%s" % (variable,input,limit), None, headers)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        repos_raw = r1.read().decode("utf-8")
        repos = json.loads(repos_raw)
        OpenFDAClient.repostory = repos
        conn.close()
        print("A done")
        return

    def list(self, limit):
        OpenFDAClient.limit = limit
        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json?&limit=%s" % (limit), None, headers)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        repos_raw = r1.read().decode("utf-8")
        repos = json.loads(repos_raw)
        OpenFDAClient.repostory = repos
        conn.close()
        print("A done")
        return

A = OpenFDAClient()

class OpenFDAParser():
    info1=None
    info2=None
    def two_params_parser(self,param1,param2):
        results1=[]
        results2=[]
        #param1:spl_id,manufacturer_name param2:brand_name
        for element in OpenFDAClient.repostory["results"]:
            try:
                results1.append(element["openfda"][param1][0])
            except KeyError:
                results1.append("Unknown")
            try:
                results2.append(element["openfda"][param2][0])
            except KeyError:
                results2.append("Unknown")

        OpenFDAParser.info1=results1
        OpenFDAParser.info2=results2
        print("B done")
        return
    def brand_name_warnings(self):
        resultsbrand=[]
        resultswarn=[]
        for element in OpenFDAClient.repostory["results"]:
            try:
                resultsbrand.append(element["openfda"]["brand_name"][0])
            except KeyError:
                resultsbrand.append("Unknown")
            try:
                resultswarn.append(element["warnings"][0])
            except KeyError:
                resultswarn.append("Unknown")
        OpenFDAParser.info1 = resultsbrand
        OpenFDAParser.info2 = resultswarn
        print("B done")
        return

B =OpenFDAParser()

class OpenFDAHTML:
    message=None
    def html(self):
        with open("final html.html", "w") as f:
            f.write("<ul>" + "\n")
            for x in range(int(OpenFDAClient.limit)):
                elementli = "<li>" + OpenFDAParser.info1[x] +"   -->    " +OpenFDAParser.info2[x]+"</li>"
                f.write(elementli)
            f.write("</ul>")
        with open("final html.html", "r") as f:
            hello = str(f.read())
            OpenFDAHTML.message = hello
            print("C done")
        return
    def default(self):
        with open("final html default.html", "r") as f:
            index = f.read()
            OpenFDAHTML.message = index

C = OpenFDAHTML()


# HTTPRequestHandler class

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        if (("/searchDrug?active_ingredient=" in self.path) or ("/searchCompany?company=" in self.path) or ("/listCompanies?limit=" in self.path) or ("/listDrugs?limit=" in self.path) or ("/listWarnings" in self.path)) or ("/" == self.path):
            # Send headers
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
        if self.path == "/":
            # Send message back to client
            C.default()
            self.wfile.write(bytes(OpenFDAHTML.message, "utf8"))
        # Write content as utf-8 data
        elif "/searchDrug?active_ingredient=" in self.path:
            indexequal=self.path.find("active_ingredient=")

            if "&" in self.path:
                drug = self.path[indexequal + 18:self.path.index("&")]
            else:
                drug = self.path[indexequal + 18:]

            if "limit=" not in self.path:
                limit = "10"
            else:
                limit = self.path[self.path.find("limit=") + 6:]
            A.two_params_request("active_ingredient",drug,limit)
            B.two_params_parser("spl_id","brand_name")
            C.html()
            self.wfile.write(bytes(OpenFDAHTML.message, "utf8"))

        elif "/searchCompany?company=" in self.path:
            indexequal = self.path.find("company=")
            if "&" in self.path:
                company = self.path[indexequal + 8:self.path.index("&")]
            else:
                company = self.path[indexequal + 8:]
            if "limit=" not in self.path:
                limit = "10"
            else:
                limit = self.path[self.path.find("limit=") + 6:]
            A.two_params_request("openfda.manufacturer_name",company,limit)
            B.two_params_parser("spl_id","brand_name")
            C.html()
            self.wfile.write(bytes(OpenFDAHTML.message, "utf8"))


        elif "/listCompanies?limit="in self.path:
            indexequal = self.path.find("=")
            limit = self.path[indexequal+1:]
            A.list(limit)
            B.two_params_parser("manufacturer_name","brand_name")
            C.html()
            self.wfile.write(bytes(OpenFDAHTML.message, "utf8"))


        elif "/listDrugs?limit=" in self.path:
            indexequal = self.path.find("=")
            limit = self.path[indexequal + 1:]
            A.list(limit)
            B.two_params_parser("spl_id","brand_name")
            C.html()

            self.wfile.write(bytes(OpenFDAHTML.message, "utf8"))
        elif "/listWarnings" in self.path:
            indexequal=self.path.find("limit=")
            limit = self.path[indexequal+6:]
            A.list(limit)
            B.brand_name_warnings()
            C.html()
            self.wfile.write(bytes(OpenFDAHTML.message, "utf8"))
        elif self.path== "/secret":
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Reserved information"')
            self.end_headers()
        elif self.path == "/redirect":
            self.send_response(302)
            self.send_header('Location', 'http://localhost:8000/')
            self.end_headers()
        else:
            self.send_error(404,"NOT FOUND","INVALID URL")




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