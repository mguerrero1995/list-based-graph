# -*- coding: utf-8 -*-

""" Classes related to list-based graphs. """

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.neighbors = list()

    
    def add_neighbor(self, node_id, weight, sort = "none"):
        """ Adds a neighboring node (i.e. connected node) and a weight connecting it to the node.
            Format is [neighbor_id, weight of edge]. """
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
        """ Updates the weight of the edge connecting the node to a given neighboring node. """
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
            
        
        
class Graph:
    """ Creates a graph to which nodes can be added or removed. Edges between nodes
    with an associated weight can be added, removed, or updated using the class methods. """
    
    # Summary information about the graph
    graph_weight = 0
    graph_edges = 0
    graph_nodes = 0
    
    def __init__(self):
        self.nodes = {}

    
    def add_node(self, node):
        """ Adds a new node, with no edges. """
        if isinstance(node, Node) and node.node_id not in self.nodes:
            self.nodes[node.node_id] = node # If supplied argument is a Node object, add it as is
            self.graph_nodes += 1
            return True
        else:
            self.nodes[node] = Node(node) # If supplied argument is not a Node object, create one
            self.graph_nodes += 1
            return True
    
    def remove_node(self, node):
        """ Remvoes a node and all of its associated edges. """
        if node in self.nodes: # Check that the node is in the graph
            # List the node_id's of the Nodes's neighbors
            neighbors = self.nodes[node].neighbors
            neighbors = [node_id[0] for node_id in neighbors] 
            
            if len(neighbors) > 0:
                edges = len(neighbors) # Number of edges is equal to the number of neighboring nodes
                weight = sum([node_id[1] for node_id in self.nodes[node].neighbors]) # Calculate the sum of weights for the edges
                for i in neighbors: # Remove the Node from the neighbors lists for its own neighbors
                    self.nodes[i].remove_neighbor(node)
                    
            # Remove the Node object from the graph
            del self.nodes[node]
            self.graph_nodes += -1
            
            # Update the weight and edge count of the graph
            self.graph_weight += -weight 
            self.graph_edges += -edges
        else:
            return False

    
    def add_edge(self, n1, n2, weight):
        """ Adds an edge with a weight between two nodes. """
        if n1 in self.nodes and n2 in self.nodes: # Check that both nodes are in the graph
            # Connect the nodes to each other and update both nodes' information
            self.nodes[n1].add_neighbor(n2, weight) 
            self.nodes[n2].add_neighbor(n1, weight)
            
            # Update the weight and edge count for the graph            
            self.graph_weight += weight
            self.graph_edges += 1
            return True
        else:
            return False

    
    def remove_edge(self, n1, n2):
        """ Removes an edge between two nodes. """
        if n1 in self.nodes and n2 in self.nodes: # Check that bpth nodes are in the graph
            # Get the node_id's of the neighbors for each input node
            n1_neighbors = self.nodes[n1].neighbors
            n1_neighbors = [node_id[0] for node_id in n1_neighbors]
            n2_neighbors = self.nodes[n2].neighbors
            n2_neighbors = [node_id[0] for node_id in n2_neighbors]
            
            if n1 in n2_neighbors and n2 in n1_neighbors: # Check that nodes are neighbors of each other
                # Get the weight of the edge to be removed
                for i, neighbor in enumerate(self.nodes[n1].neighbors):
                    # i is the index of the current neighbor in n1's neighbors list
                    # neighbor is the list [node_id, weight] of the neighbor
                    if neighbor[0] == n2: # Check that the current neighbor's node_id matches n2
                        weight = self.nodes[n1].neighbors[i][1] # If True, get the weight for that edge
                        
                # Remove each node from the other's list of neighbors
                self.nodes[n1].remove_neighbor(n2)
                self.nodes[n2].remove_neighbor(n1)
                
                # Update the weight and edge count of the graph
                self.graph_weight += -weight 
                self.graph_edges += -1 
                return True
            else: 
                return False
        else:
            return False
       
    
    def update_edge(self, n1, n2, weight):
        """ Update the value a the weight for an edge between two nodes. """
        if n1 in self.nodes and n2 in self.nodes: # Check that both nodes are in the graph
            # Get the node_id's for each of the Node's neighbors
            n1_neighbors = self.nodes[n1].neighbors 
            n1_neighbors = [node_id[0] for node_id in n1_neighbors]
            
            n2_neighbors = self.nodes[n2].neighbors
            n2_neighbors = [node_id[0] for node_id in n2_neighbors]
            
            if n1 in n2_neighbors and n2 in n1_neighbors: # Check that nodes are actually neighbors
                current_weight = [node_id[1] for node_id in n1_neighbors] # Get the current weight of the edge
                
                # Update the weight information for both of the connected nodes
                self.nodes[n1].update_weight(n2, weight) 
                self.nodes[n2].update_weight(n1, weight)
                
                # Update the weight of graph
                self.graph_weight += weight - current_weight
            return True
        else: 
            return False
        
    def print_graph(self):
        for node, neighbors in g.nodes.items():
            print("Node %s has neighbor(s) and weight(s) %s" % (node, neighbors.neighbors))
    

# Initialize an empty graph
g = Graph()   

# Create 3 node object
n1 = Node("a")
n2 = Node("b")
n3 = Node("c")

# Add the nodes to the graph
g.add_node(n1)
g.add_node(n2)
g.add_node(n3)

# Create a fully connected graph
g.add_edge("a", "b", 5) # Add an edge from node a to node b, with weight 5
g.add_edge("a", "c", 10) # Add an edge from node a to node c, with weight 10
g.add_edge("b", "c", 15) # Add an edge from node b to node c, with weight 15

# Check the summary statistics about the graph
print(g.graph_weight, g.graph_edges, g.graph_nodes)

# Remove the edge between a and b
g.remove_edge("a", "b")

# See the new summary - weight should be reduced by 5, edges by reduced by 1, and nodes unchanged
print(g.graph_weight, g.graph_edges, g.graph_nodes)

g.add_edge("a", "b", 5) # Replace the removed node
print(g.graph_weight, g.graph_edges, g.graph_nodes)

# Use the node removal method to completely remove node b and its edges
g.remove_node("b")

# See the new summary - weight should be reduced by 20, edges by reduced by 2, and nodes reduced by 1
print(g.graph_weight, g.graph_edges, g.graph_nodes)

# Print out all the nodes and their neighbors/weights
g.print_graph()

