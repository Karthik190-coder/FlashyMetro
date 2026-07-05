import math
import heapq
'''
def dijkstra(graph, start, end):
    unvisited = list(graph.keys())
    distance = {}

    for stop in graph:
        distance[stop] = math.inf #Routes we dont know are infinitely far till we map em
    distance[start] = 0 #source is 0 obv
    
    previous = {}
    for stop in graph:
        previous[stop] = None #at the start, the previous stop is nothing/non existent
    
    while unvisited:
        current = min(unvisited, key=lambda stop: distance[stop]) #the lambda part means to compare distance values instead of alphabetic keys
                                                                   #Also, current is the min distance between source and unvisited locations
        if current == end:
            break #Break if we reach destination
            
        for neighbour, time in graph[current].items():
            new_distance = distance[current] + time #Calculate time taken to get here + to get to neighboring locations out of EVERY reachable stop from current location
            #now, if distance to every stop is the smallest possible one out of all our options, it gets added to the dictionary
            if new_distance < distance[neighbour]: 
                distance[neighbour] = new_distance
                previous[neighbour] = current
        unvisited.remove(current) #remove the locations we visited
    
    path = [] #Clean list to display our path
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    #We do it in reverse since we go from the start to the end, now we get the data by moving back and then we reverse it to make it presentable
    path.reverse()
    return path, distance[end]

'''

def dijkstra_opti(graph,start,end):
    priority_queue = [(0,start)]
    #Using dict comprehension, we write a dictionary we map out the distance of our starting position (0) and to every other stop in the graph as infinity
    distance = {stop:math.inf for stop in graph} #Order doesnt affect the correctness of the dijkstra algorithm
    distance[start] = 0
    previous = {stop:None for stop in graph}
    visited = set() #duplicates are omitted
    while priority_queue:
        current_distance,current=heapq.heappop(priority_queue) #current distance is time taken to that spot and current is the location itself
        if current == end: #break immediately after finding destination since thats the shortest path
            break
        
        if current in visited: #skips the redundant data as in outdated slower routes
            continue
        visited.add(current) #keeps adding the locations that we have visited
        for neighbour, time in graph[current].items():
                if neighbour in visited:
                    continue
            
                new_distance = current_distance + time
            
                if new_distance < distance[neighbour]:
                    distance[neighbour] = new_distance
                    previous[neighbour] = current
                    heapq.heappush(priority_queue, (new_distance, neighbour))
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()

    return path, distance[end]

def close_connection(graph, stop_a, stop_b):
    # stores the removed weight so it can be restored later, returns None if there was nothing to remove
    removed = None
    if stop_a in graph and stop_b in graph[stop_a]:
        removed = graph[stop_a].pop(stop_b)
    if stop_b in graph and stop_a in graph[stop_b]:
        graph[stop_b].pop(stop_a)
    return removed

def reopen_connection(graph, stop_a, stop_b, weight):
    # restores a previously closed connection in both directions
    graph[stop_a][stop_b] = weight
    graph[stop_b][stop_a] = weight

# Real Kochi Metro Blue Line, Aluva -> Tripunithura (25 stations, official KMRL order)
# Travel times are an approximation (based on published ~46 min average end-to-end pace),
# not exact KMRL timetable data
graph1 = {
    "Aluva": {"Pulinchodu": 2},
    "Pulinchodu": {"Aluva": 2, "Companypady": 2},
    "Companypady": {"Pulinchodu": 2, "Ambattukavu": 2},
    "Ambattukavu": {"Companypady": 2, "Muttom": 2},
    "Muttom": {"Ambattukavu": 2, "Kalamassery": 2},
    "Kalamassery": {"Muttom": 2, "Cochin University": 2},
    "Cochin University": {"Kalamassery": 2, "Pathadipalam": 2},
    "Pathadipalam": {"Cochin University": 2, "Edapally": 2},
    "Edapally": {"Pathadipalam": 2, "Changampuzha Park": 2},
    "Changampuzha Park": {"Edapally": 2, "Palarivattom": 2},
    "Palarivattom": {"Changampuzha Park": 2, "JLN Stadium": 2},
    "JLN Stadium": {"Palarivattom": 2, "Kaloor": 2},
    "Kaloor": {"JLN Stadium": 2, "Town Hall": 2},
    "Town Hall": {"Kaloor": 2, "MG Road": 2},
    "MG Road": {"Town Hall": 2, "Maharaja's College": 2},
    "Maharaja's College": {"MG Road": 2, "Ernakulam South": 2},
    "Ernakulam South": {"Maharaja's College": 2, "Kadavanthra": 2},
    "Kadavanthra": {"Ernakulam South": 2, "Elamkulam": 2},
    "Elamkulam": {"Kadavanthra": 2, "Vyttila": 2},
    "Vyttila": {"Elamkulam": 2, "Thaikoodam": 2},
    "Thaikoodam": {"Vyttila": 2, "Petta": 2},
    "Petta": {"Thaikoodam": 2, "Vadakkekotta": 2},
    "Vadakkekotta": {"Petta": 2, "SN Junction": 2},
    "SN Junction": {"Vadakkekotta": 2, "Tripunithura": 2},
    "Tripunithura": {"SN Junction": 2}
}
stop_coords = {
    "Aluva": (10.1004, 76.3570),
    "Pulinchodu": (10.0938, 76.3564),
    "Companypady": (10.0873, 76.3557),
    "Ambattukavu": (10.0808, 76.3551),
    "Muttom": (10.0742, 76.3545),
    "Kalamassery": (10.0677, 76.3538),
    "Cochin University": (10.0611, 76.3532),
    "Pathadipalam": (10.0546, 76.3526),
    "Edapally": (10.0480, 76.3519),
    "Changampuzha Park": (10.0415, 76.3513),
    "Palarivattom": (10.0350, 76.3507),
    "JLN Stadium": (10.0284, 76.3500),
    "Kaloor": (10.0219, 76.3494),
    "Town Hall": (10.0153, 76.3488),
    "MG Road": (10.0088, 76.3481),
    "Maharaja's College": (10.0022, 76.3475),
    "Ernakulam South": (9.9957, 76.3469),
    "Kadavanthra": (9.9892, 76.3462),
    "Elamkulam": (9.9826, 76.3456),
    "Vyttila": (9.9761, 76.3450),
    "Thaikoodam": (9.9695, 76.3444),
    "Petta": (9.9630, 76.3437),
    "Vadakkekotta": (9.9565, 76.3431),
    "SN Junction": (9.9499, 76.3425),
    "Tripunithura": (9.9500, 76.3500)
}

#path, total_time = dijkstra(graph1, "Aluva", "Ernakulam South")
#print("Best route:", " → ".join(path))
#print("Total time:", total_time, "minutes")

