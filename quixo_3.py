import cherrypy
import sys
import random

class Server:
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # Deal with CORS
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        if cherrypy.request.method == "OPTIONS":
            return ''
        
        body = cherrypy.request.json
        body["you"] in body["players"] 
        #sides = [0, 1, 2, 3, 4, 5, 9, 10, 14, 15, 19, 20, 21, 22, 23, 24] 
        north = [0,1,2,3,4]
        #directions = ['N', 'S', 'E', 'W']
        changedirection = {'E' : 'W', 'W' : 'E','N' : 'S', 'S' :'N'}
        #increments = {'N': -5,'S': +5,'E': 1,'W': -1}
        forbidden = {'E': [4, 9, 14, 19, 24],'W': [0, 5, 10, 15, 20],'N': [0, 1, 2, 3, 4],'S': [20, 21, 22, 23, 24]} 
        if all (value is None for value in body["game"]) : #meaning it's the first round
            Move = {"cube": random.choice(north),"direction": changedirection['N']} 
            #while (Move["cube"] in forbidden[Move["direction"]]) : #verifies that the move is allowed
                 #Move = {"cube": random.choice(sides),"direction": random.choice(directions)} #first round is random
        else : 
            i = 0
            while body["game"][i] == None :
                i += 1
                cube_by = i 
                cube_now = cube_by + 5 #play the cube on its left
                direction = changedirection['N']
                
                Move = {"cube": cube_now,"direction": direction}
                while (body["game"][Move["cube"]] != None) and (Move["cube"] in forbidden[Move["direction"]]) :
                    Move = {"cube": cube_now,"direction": direction}
            
      
        print(body)
        return {"move": Move}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8080

    cherrypy.config.update({'server.socket_host' :'0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server())
