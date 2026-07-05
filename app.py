from flask import Flask,jsonify,request #Flask creates the actual server, jsonify turns our python dict to a json datatype (json=JS object Notation, which js can read,json is a datainterchange format) and thus the frontend can understand our data
#requests are the entire piece of data that our app.py aka the API collects including parameters,methods,URLs and we can access it by using request.args.get() function
from flask_cors import CORS #Allows requests from other hosts or ports since index.html and app.py (flask server) are in two different ports
from MetroPulse import dijkstra_opti, graph1, stop_coords, close_connection, reopen_connection
import math

app = Flask(__name__) #app is a variable and Flask(__name__) in this __name__ is a default option which refers to file name and thus the line means that the server/application is being hosted
CORS(app) #allow requests from other hosts

#maps a lowercase stop name -> the real, correctly-capitalized stop name
# e.g. "aluva" -> "Aluva", so user input in any case can be matched back to the real key
stop_lookup = {name.lower(): name for name in graph1}

@app.route("/route") #function decorator that adds extra content to a function without changing code.
#The decorator tells the function and flask specifically to execute the function whenever /route is visited(requests go to /route)
def get_route():
    start_input = request.args.get("start") #edited: renamed from "start" to "start_input" — this holds the RAW text the user typed, before any normalization
    end_input = request.args.get("end") #edited: renamed from "end" to "end_input" — same idea, raw text from the user

    #new: guard against missing input BEFORE calling .strip() on it — calling .strip() on None would crash
    if not start_input or not end_input:
        return jsonify({"error":"Both start and end are required"}),400

    #normalize whatever the user typed to lowercase, then look up the real name
    start = stop_lookup.get(start_input.strip().lower()) #edited: now reads from start_input (the raw text) instead of the undefined start_input... wait see note below
    end = stop_lookup.get(end_input.strip().lower())

    #Safety checks incase theres invalid inputs 
    if not start or not end: 
        return jsonify({"error":"Unknown stop name"}),400 #edited: merged with the typo-catching check below since stop_lookup.get() already returns None for both "missing" and "unknown name" cases
    
    path, total_time = dijkstra_opti(graph1, start, end) #calls our algorithm to do the searching

    if total_time == math.inf:
        return jsonify({"error": f"No route exists between {start} and {end}"}), 404
   
    return jsonify({ #jsonifies the output for frontend to read/use/display etc
        "route":path,
        "total_time":total_time
    })
@app.route("/stops") #decorator to tell flask to execute this function whenever /stops is visited
def get_stops():
    return jsonify(stop_coords) #stop coords are jsonified
# keeps track of connections we've closed, so we can restore them later
# key = (stop_a, stop_b), value = the original weight before closing
closed_connections = {}

@app.route("/disrupt")
def disrupt():
    stop_a_input = request.args.get("stop_a")
    stop_b_input = request.args.get("stop_b")

    if not stop_a_input or not stop_b_input:
        return jsonify({"error": "Both 'stop_a' and 'stop_b' are required"}), 400

    stop_a = stop_lookup.get(stop_a_input.strip().lower())
    stop_b = stop_lookup.get(stop_b_input.strip().lower())

    if not stop_a or not stop_b:
        return jsonify({"error": "Unknown stop name"}), 400

    removed_weight = close_connection(graph1, stop_a, stop_b)

    if removed_weight is None:
        return jsonify({"error": f"No direct connection between {stop_a} and {stop_b}"}), 404

    closed_connections[(stop_a, stop_b)] = removed_weight

    return jsonify({"message": f"Connection between {stop_a} and {stop_b} closed", "weight": removed_weight})

@app.route("/reopen")
def reopen():
    stop_a_input = request.args.get("stop_a")
    stop_b_input = request.args.get("stop_b")

    stop_a = stop_lookup.get(stop_a_input.strip().lower()) if stop_a_input else None
    stop_b = stop_lookup.get(stop_b_input.strip().lower()) if stop_b_input else None

    if not stop_a or not stop_b:
        return jsonify({"error": "Unknown stop name"}), 400

    key = (stop_a, stop_b)
    if key not in closed_connections:
        return jsonify({"error": "That connection wasn't closed"}), 400

    weight = closed_connections.pop(key)
    reopen_connection(graph1, stop_a, stop_b, weight)

    return jsonify({"message": f"Connection between {stop_a} and {stop_b} reopened"})
if __name__ == "__main__": #safety check to run the file itself instead of imports
    app.run(debug=True) #actually runs the file