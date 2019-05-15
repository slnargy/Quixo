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
        sides = [0, 1, 2, 3, 4, 5, 9, 10, 14, 15, 19, 20, 21, 22, 23, 24] #contours du plateau
        directions = ['N', 'S', 'E', 'W']
        forbidden = {'E': [4, 9, 14, 19, 24],'W': [0, 5, 10, 15, 20],'N': [0, 1, 2, 3, 4],'S': [20, 21, 22, 23, 24]} #combinaison interdites
        randomMove = {"cube": random.choice(sides),"direction": random.choice(directions)} 
        while (body["game"][randomMove["cube"]] != None) and (randomMove["cube"] in forbidden[randomMove["direction"]]) : #vérifier que la case est vide et que le mouvement est autorisé
                randomMove = {"cube": random.choice(sides),"direction": random.choice(directions)}
      
        print(body)
        return {"move": randomMove}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8080

    cherrypy.config.update({'server.socket_host':'0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server())

