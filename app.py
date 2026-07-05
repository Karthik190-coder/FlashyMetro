from flask import Flask,jsonify,request #Flask creates the actual server, jsonify turns our python dict to a json datatype (json=JS object Notation, which js can read,json is a datainterchange format) and thus the frontend can understand our data
#requests are the entire piece of data that our app.py aka the API collects including parameters,methods,URLs and we can access it by using request.args.get() function
from flask_cors import CORS #Allows requests from other hosts or ports since index.html and app.py (flask server) are in two different ports
from MetroPulse import dijkstra,graph1,stop_coords #Imports the algorithm from metropulse.py

app = Flask(__name__) #app is a variable and Flask(__name__) in this __name__ is a default option which refers to file name and thus the line means that the server/application is being hosted
CORS(app) #allow requests from other hosts

@app.route("/route") #function decorator that adds extra content to a function without changing code.
#The decorator tells the function and flask specifically to execute the function whenever /route is visited(requests go to /route)
def get_route():
    start = request.args.get("start") #gets start from request
    end = request.args.get("end") #gets end from the request

    path,total_time = dijkstra(graph1,start,end) #calls our algorithm to do the searching

    return jsonify({ #jsonifies the output for frontend to read/use/display etc
        "route":path,
        "total_time":total_time
    })
@app.route("/stops") #decorator to tell flask to execute this function whenever /stops is visited
def get_stops():
    return jsonify(stop_coords) #stop coords are jsonified
if __name__=="__main__": #safety check to run the file itself instead of imports
    app.run(debug=True) #actually runs the file


