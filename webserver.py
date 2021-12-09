from http.server import BaseHTTPRequestHandler, HTTPServer 
import cgi 
import cgitb
cgitb.enable()

class WebServerHandler(BaseHTTPRequestHandler):

    #handling requests to the server  

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header("Content-type","text/html")
                self.end_headers()
                message=""
                message+="<html><body>"
                message+="<h1>Hello!</h1>"
                message+= '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="output" type="text" ><input type="submit" value="Submit"> </form>'''
                message+="</html></body>"
                self.wfile.write(message.encode())

                print(message)

                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header("Content-type","text/html")
                self.end_headers()
                message=""
                message+="<html><body>"
                message+="&#161Hola <a href ='./hello'> Back to Hello</a>"
                message+= '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="output" type="text" ><input type="submit" value="Submit"> </form>'''
                message+="</body></html>"
                self.wfile.write(message.encode())

                print(message)
                
                return 
    
        except IOError:
            self.send_error(404, "File Not Found: %s" %self.path)
            
    #Getting information and posting it on the page

    def do_POST(self):
        try:
            self.send_response(301) 
            self.send_header('Content-type','text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
           
            if ctype == "multipart/form-data":
                pdict['boundary']=bytes(pdict["boundary"],'utf-8')
                fields=cgi.parse_multipart(self.rfile, pdict)
                print(fields)
                messagecontent = fields.get('output')[0]
            message=""
            message+="<html><body>"
            message+="<h2> Okay, how about this: </h2>"
            message+="<h1>%s</h1>" %messagecontent

            message+= '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="output" type="text" ><input type="submit" value="Submit"> </form>'''

            message+="</body></html>"

            self.wfile.write(message.encode())

            print (message)

        except:
            pass 
    
#creates the server until ctrl+c is pressed 
def main():
    try:
        port=8080
        server = HTTPServer(("",port), WebServerHandler)
        print("Web Server running on port %s", port)
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()

#starts the server as soon as the class is called   

if __name__=='__main__':
    main()
