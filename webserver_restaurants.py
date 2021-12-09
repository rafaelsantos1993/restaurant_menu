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
                #query all restauraunts 
                restaurants=session.query(Restaurant).all()
                self.send_response(200)
                self.send_header("Content-type","text/html")
                self.end_headers()
                website=""
                website+="<html><body>"
                website+="<h1><a href='./restaurants/new'>Make a New Restaurant Here</a></h1>"
                website+="<h1>Restaurants</h1>"
                website+="<ul>"
                for restaurant in restaurants:
                    website+="<li>"+restaurant.name+"</li>"
                    id=str(restaurant.id)
                    website+="<a href='./restaurants/"+id+"/edit'>Edit </a>"
                    website+="<br>"
                    website+="<a href='./restaurants/"+id+"/delete'>Delete</a>"
                    website+="<br><br>"                    
                website+="</ul>"
                website+="</body></html>"
                self.wfile.write(website.encode())

                return
            
            #page for the new resurant 
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header("Content-type","text/html")
                self.end_headers()
                message=""
                message+="<html><body>"
                message+="<h1>Add the new restaurant to the list</h1>"
                message+="<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input name='restaurantName' type='text'> <input type='submit' value='Create'> </form>"
                message+="</body></html>"
                self.wfile.write(message.encode())
                return
            #page to change the name of a restaurant 
            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header("Content-type","text/html")
                self.end_headers()
                
                # get the restastaunt id 

                numbersPath=self.path.split("/")
                
                id=[i for i in numbersPath if (i.isnumeric())]
                
                id=int(id[0])
        
                ##get the restaurant objts 
                
                theRestaurant=session.query(Restaurant).get(id)
                

                message=""
                message+="<html><body>"
                message+= "<h2>"+ theRestaurant.name +"</h2>"
                message+="<form method='POST' enctype='multipart/form-data' action='/restaurants/"+str(id)+"/edit'><input name='restaurantNewName' type='text'> <input type='submit' value='Rename'> </form>"
                message+="</body></html>"
                self.wfile.write(message.encode())

            #page to delete a restaurant 
            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header("Content-type","text/html")
                self.end_headers()

                # get the restastaunt id 

                numbersPath=self.path.split("/")
                
                id=[i for i in numbersPath if (i.isnumeric())]
                
                id=int(id[0])
        
                ##get the restaurant objts 
                
                theRestaurant=session.query(Restaurant).get(id)

                message=""
                message+="<html><body>"
                message+="<h2> Restaurant "+theRestaurant.name+" will be deleted </h2>" 
                message += "<form method='POST' enctype = 'multipart/form-data' action = '/restaurants/%s/delete'>" % theRestaurant.id
                message += "<input type = 'submit' value = 'Delete'>"
                message+="</body></html>"
                self.wfile.write(message.encode())              

        except IOError:
            self.send_error(404, "File Not Found: %s" %self.path)

    def do_POST(self):
        try:

            #create a new restaurant 
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
            
            #rename a restaurant 

            if self.path.endswith('/edit'):
                ctype, pdict=cgi.parse_header(self.headers['Content-type'])
                if ctype == 'multipart/form-data':
                    pdict['boundary']=bytes(pdict["boundary"],'utf-8')
                    fields=cgi.parse_multipart(self.rfile,pdict)
                    restaurantNewName=fields.get('restaurantNewName')

                    # get the restastaunt id 

                    numbersPath=self.path.split("/")
                    id=[i for i in numbersPath if (i.isnumeric())]
                    id=int(id[0])
    
                    ##get the restaurant objts 

                    theRestaurant=session.query(Restaurant).get(id)
                    theRestaurant.name=restaurantNewName[0]
                    session.add(theRestaurant)
                    session.commit()
                    print("Name modfied")
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location','/restaurants')
                    self.end_headers()
            
            #delete a restaurant 

            if self.path.endswith('/delete'):
                # get the restastaunt id 

                numbersPath=self.path.split("/")
        
                id=[i for i in numbersPath if (i.isnumeric())]
        
                id=int(id[0])

                ##get the restaurant objts 
        
                theRestaurant=session.query(Restaurant).get(id)

                session.delete(theRestaurant)

                session.commit()
                print("Restaurant Deleted")
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
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

            










