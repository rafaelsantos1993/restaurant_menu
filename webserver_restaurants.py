#libraries to set the server
from http import server
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import cgitb


#libraries to connect and modify the database 
from sqlalchemy import create_engine, engine
from sqlalchemy.orm import session, sessionmaker
from database_setup import Base, Restaurant, MenuItem 


cgitb.enable()

#connect to the DB
engine=create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBsession=sessionmaker(bind=engine)
session=DBsession()

class WebserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            #Home page with all restaurants listed
            if self.path.endswith('/restaurants'):
                self.send_response(200)
                self.send_header("Content-type","text/html")
                self.end_headers()

                #query all restauraunts 
                restaurants=session.query(Restaurant).all()

                #put them on the html 
                website=""
                website+="<html><body>"
                website+="<h1><a href='./restaurants/new'>Make a New Restaurant Here</a></h1>"
                website+="<h1>Restaurants</h1>"
                website+="<ul>"
                for restaurant in restaurants:
                    website+="<li>"+restaurant.name+"</li>"
                    website+="<a href='#'> Edit </a>"
                    website+="<br>"
                    website+="<a href='#'>Delete</a>"
                    website+="<br><br>"                    
                website+="</ul>"
                website+="</body></html>"
                self.wfile.write(website.encode())

                return
            
            #page for the new resurant 
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header("Content-type","text/html")
                print('aqui')
                self.end_headers()
                message=""
                message+="<html><body>"
                message+="<h1>Add the new restaurant to the list</h1>"
                message+="<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input name='restaurantName' type='text'> <input type='submit' value='Create'> </form>"
                message+="</body></html>"
                self.wfile.write(message.encode())
                return

        except IOError:
            self.send_error(404, "File Not Found: %s" %self.path)
    def do_POST(self):
        try:
            if self.path.endswith('/restaurants/new'):
                ctype, pdict= cgi.parse_header(self.headers['Content-type'])
                if ctype == 'multipart/form-data':
                    pdict['boundary']=bytes(pdict["boundary"],'utf-8')
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    restaurantName=fields.get('restaurantName')
                    newRestaurant=Restaurant(name=restaurantName[0])
                    session.add(newRestaurant)
                    session.commit()
                    print('new restaurant added')
                    self.send_response(301)
                    self.send_header('Content-type','text/html')
                    self.send_header('Location','/restaurants')
                    self.end_headers()

                    
        except:
            pass

def main():
        try:
            port=8080
            server=HTTPServer(("",port), WebserverHandler)
            print("Web Server is running on port %s", port)
            server.serve_forever()
        
        except KeyboardInterrupt:
            print("\n^C entered, stopping web server...")
            server.socket.close()

if __name__=='__main__':
    main()

            










