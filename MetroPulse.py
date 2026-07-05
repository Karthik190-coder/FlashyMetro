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


graph1 = {
    "Aluva":{"Edapally":15, "Kalamassery" :10},
    "Kalamassery":{"Edapally":7,"Aluva":10},
    "Edapally":{"Aluva":15,"Kalamassery":7,"Kaloor":12},
    "Kaloor":{"Edapally":12,"Ernakulam South":8},
    "Ernakulam South":{"Kaloor":8}
}
stop_coords = {
    "Aluva": (10.1004, 76.3570),
    "Kalamassery": (10.0544, 76.3212),
    "Edapally": (10.0261, 76.3083),
    "Kaloor": (9.9931, 76.2998),
    "Ernakulam South": (9.9816, 76.2999)
}
#path, total_time = dijkstra(graph1, "Aluva", "Ernakulam South")
#print("Best route:", " → ".join(path))
#print("Total time:", total_time, "minutes")

