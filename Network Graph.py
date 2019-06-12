# -*- coding: utf-8 -*-

""" Classes related to list-based network graphs. """

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.neighbors = list()

    
    def add_neighbor(self, node_id, weight, sort = "none"):
        """ Adds a neighboring node (i.e. connected node) and a weight connecting it to the node. """
        if node_id not in [node_id[0] for node_id in self.neighbors]:
            neighbor = [node_id, weight]
            self.neighbors.append(neighbor)
            if sort == "node_id":
                self.neighbors.sort()
            elif sort == "weight":
                self.neighbors.sort(key = lambda x: x[1])
            else: 
                pass
    
    
    def remove_neighbor(self, node_id, sort = "none"):
        """ Removes a neighboring node (i.e. connected node) and the weight connecting it to the node. """
        if node_id in [node_id[0] for node_id in self.neighbors]:
            self.neighbors = [neighbor for neighbor in self.neighbors if neighbor[0] != node_id]
            if sort == "node_id":
                self.neighbors.sort()
            elif sort == "weight":
                self.neighbors.sort(key = lambda x: x[1])
            else: 
                pass
    
    
    def update_weight(self, node_id, new_weight):
        """ Updates the weight of the edge connecting the node to a give neighboring node. """
        if node_id in [node_id[0] for node_id in self.neighbors]:
            old_neighbor = [neighbor for neighbor in self.neighbors if neighbor[0] == node_id]
            for ind, weight in enumerate(self.neighbors):
                if old_neighbor == [self.neighbors[ind]]:
                    self.neighbors[ind] = [node_id, new_weight]
                    return True
            return False
        else:
            return False
    
    
    def sort_by_id(self, increasing = True):
        """ Sort all neighbors by their node_id. """
        self.neighbors.sort(reverse = not increasing) 
     
    
    def sort_by_weights(self, increasing = True):
        """ Sort all neighbors by their weights. """
        self.neighbors.sort(key = lambda x: x[1], reverse = not increasing) 
            
class Network:
    """ Creates a network to which nodes can be added or removed. Edges between nodes
    with associated weight can be added, removed, or updated using the class methods below. """

    def __init__(self):
        self.nodes = {}

    
    def add_node(self, node):
        """ Adds a new node, with no edges. """
        if isinstance(node, Node) and node.node_id not in self.nodes:
            self.nodes[node.node_id] = node
            return True
        # else if isinstance(node, tuple(int, str)): 
        #     self.nodes[node] = Node(node)
        else:
            return False

    
    def remove_node(self, node):
        """ Remvoes a node and all of its associated edges. """
        if node in self.nodes:
            neighbors = self.nodes[node].neighbors
            neighbors = [node_id[0] for node_id in neighbors]
            if len(neighbors) > 0:
                for i in neighbors:
                    self.nodes[i].remove_neighbor(node)
            del self.nodes[node]
        else:
            return False

   
    def add_edge(self, n1, n2, weight):
        """ Adds an edge with a weight between two nodes. """
        if n1 in self.nodes and n2 in self.nodes:
            self.nodes[n1].add_neighbor(n2, weight)
            self.nodes[n2].add_neighbor(n1, weight)
            return True
        else:
            return False

    
    def remove_edge(self, n1, n2):
        """ Removes an edge between two nodes. """
        if n1 in self.nodes and n2 in self.nodes:    
            n1neighbors = self.nodes[n1].neighbors
            n1neighbors = [node_id[0] for node_id in n1neighbors]
            
            n2neighbors = self.nodes[n2].neighbors
            n2neighbors = [node_id[0] for node_id in n2neighbors]
            
            if n1 in n2neighbors and n2 in n1neighbors:
                self.nodes[n1].remove_neighbor(n2)
                self.nodes[n2].remove_neighbor(n1)
                return True
        else:
            return False
       
    
    def update_edge(self, n1, n2, weight):
        """ Update the value a the weight for an edge between two nodes. """
        if n1 in self.nodes and n2 in self.nodes:    
            n1neighbors = self.nodes[n1].neighbors
            n1neighbors = [node_id[0] for node_id in n1neighbors]
            
            n2neighbors = self.nodes[n2].neighbors
            n2neighbors = [node_id[0] for node_id in n2neighbors]
            
            if n1 in n2neighbors and n2 in n1neighbors:
                self.nodes[n1].update_weight(n2, weight)
                self.nodes[n2].update_weight(n1, weight)
            return True
        else: 
            return False
                

# net = Network()   
    
# n1 = Node("a")
# n2 = Node("b")
# n3 = Node("c")

# net.add_node(n1)
# net.add_node(n2)
# net.add_node(n3)

# net.add_edge("a", "b", 5)
# net.add_edge("a", "c", 10)
# net.add_edge("b", "c", 15)


# print(net.nodes["a"].neighbors)
# print(net.nodes["c"].neighbors)

# net.update_edge("a", "b", 4)

# print(net.nodes["a"].neighbors)
# print(net.nodes["b"].neighbors)

# print(net.nodes["a"].neighbors)
# print(net.nodes["c"].neighbors)

# net.remove_node("b")

# print(net.nodes["a"].neighbors)
# print(net.nodes["c"].neighbors)
# print(net.nodes["b"].neighbors)
