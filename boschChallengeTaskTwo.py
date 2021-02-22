import json
from collections import defaultdict
import sys

edges = []
#flat the json
current_pos = sys.argv[1]

current_traffic_light = json.loads(str(sys.argv[2]))

keys = current_traffic_light.keys()
f = open("task2/log.txt", "a")
f.write(str(current_traffic_light) + "\n")
f.close()

with open('task2/taskTwo.json') as json_file:
    data = json.load(json_file)
    for p in data:
        for d in data[p]:
            edges.append((str(p),str(d), data[p][d]['Time'], data[p][d]['TrafficLight'], data[p][d]['TrafficLightDelay']))
            

class Graph():
    def __init__(self):
        self.edges = defaultdict(list)
        self.weights = {}
        self.traffic_light = {}
        self.traffic_light_delay = {}

    def add_edge(self, from_node, to_node, weight, traffic_light, traffic_light_delay):
        # Note: assumes edges are bi-directional
        self.edges[from_node].append(to_node)
        self.weights[(from_node, to_node)] = weight
        self.traffic_light[(from_node, to_node)] = traffic_light
        self.traffic_light_delay[(from_node, to_node)] = traffic_light_delay



def dijsktra(initial):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)

    graph = Graph()
    for edge in edges:
        graph.add_edge(*edge)

    end = 'D4'
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()
    
    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            traffic_light = graph.traffic_light[(current_node, next_node)]
            traffic_light_delay = graph.traffic_light_delay[(current_node, next_node)]

            if next_node in keys:
                for key in keys:
                    if(key == next_node):
                        if(current_traffic_light[key]['RedLight'] == 0):
                            weight += current_traffic_light[key]['RedLightDelay']
                            
            else:
                if(traffic_light == 0):
                    weight += traffic_light_delay
            f = open("task2/log.txt", "a")
            f.write(str(current_node) + "\n")
            f.write(str(next_node)+ "\n")
            f.write(str(weight) + "\n")
            f.close()
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)
        
        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        f = open("task2/log.txt", "a")
        f.write(str(next_destinations) + "\n")
        f.close() 
        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
    
    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    f = open("task2/log.txt", "a")
    f.write("Path" + "\n")
    f.write(str(path) + "\n")
    f.write("Out" + "\n")
    f.write(str(path[1]) + "\n")
    f.close() 
    print(path[1])
    return path

dijsktra(current_pos)
        
        
            
        