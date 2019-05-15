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
        left= [0,5,10,15,20] #always starts on the left side
        #next_cube = {0:1,1:2,2:3,3:4,4:0,5:6,6:7,7:8,8:9,9:5,10:11,11:12,12:13,13:14,14:10,15:16,16:17,17:18,18:19,19:15,20:21,21:22,22:23,23:24,24:20}
        directions = ['N', 'S', 'E', 'W']
        changedirection = {'E' : 'W', 'W' : 'E','N' : 'S', 'S' :'N'}
        forbidden = {'E': [4, 9, 14, 19, 24],'W': [0, 5, 10, 15, 20],'N': [0, 1, 2, 3, 4],'S': [20, 21, 22, 23, 24]}
        #me = body['players'].index('sln') #to know if i'm 0 or 1
        if all (value is None for value in body["game"]) : #if it's the first round
            Move = {"cube": random.choice(left),"direction": random.choice(directions)} 
            while (Move["cube"] in forbidden[Move["direction"]]) : #check if it's not forbidden
                    Move = {"cube": random.choice(left),"direction": random.choice(directions)}
                   
        else : 
            i = 0
            while body["game"][i] == None : #looks for an already played cube
                if i <= 23 :
                    i += 1
                else :
                    break
            #while body["game"][i] != me: #check that it's me
                #if i <= 23 :
                    #i += 1
                #else :
                    #break
            while body["game"][i] !=  None: #looks for the first cube not played next to it
                if i <= 23 :
                     i += 1
                else :
                    break    
            cube_by = i 
            #cube_now = next_cube[cube_by]
            #print (cube_now)
            if cube_by in forbidden['E'] : 
                direction = changedirection['E']
            elif cube_by in forbidden['W'] :
                direction = changedirection['W']
            elif cube_by in forbidden['N'] :
                direction = changedirection['N']
            elif cube_by in forbidden['S'] :
                direction = changedirection['S']
            Move = {"cube": cube_by,"direction": direction}
            while (Move["cube"] in forbidden[Move["direction"]]) :
                        Move = {"cube": cube_by,"direction": direction}
                        #Move = body['moves']
            print(Move)    


            
      
        #print(body)
        return {"move": Move}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8080

    cherrypy.config.update({'server.socket_host':'0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server())