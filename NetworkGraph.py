# -*- coding: utf-8 -*-

""" Classes related to list-based graphs. """

import numpy as np

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.neighbors = list()


    def add_neighbor(self, node_id, weight, sort = "weight"):
        """ Adds a neighboring node (i.e. connected node) and a weight connecting it to the node.
            Format is [neighbor_id, weight of edge]. """
        if node_id not in [node_id[0] for node_id in self.neighbors]:
            neighbor = [node_id, weight]
            self.neighbors.append(neighbor)
            return True
            if sort == "node_id":
                self.neighbors.sort()
            elif sort == "weight":
                self.neighbors.sort(key = lambda x: x[1])
            else:
                pass


    def remove_neighbor(self, node_id, sort = "weight"):
        """ Removes a neighboring node (i.e. connected node) and the weight connecting it to the node. """
        if node_id in [node_id[0] for node_id in self.neighbors]:
            self.neighbors = [neighbor for neighbor in self.neighbors if neighbor[0] != node_id]
            return True
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
                    self.neighbors.sort(key = lambda x: x[1])
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

    def graph_from_adj_mat(self, mat):
        """ Create a Graph object from a given adjacency matrix. """
        # Add a node for each vertex in the adjacency matrix
        for i in range(len(mat)):
            self.add_node(i)
        
        # Generate the weighted edges from the adjacency matrix
        for r in range(len(mat)):
            for c in range(len(mat)):
                if r != c and mat[r, c] != 0:
                    self.add_edge(r, c, mat[r, c])
                
    
    def add_node(self, node):
        """ Adds a new node, with no edges. """
        if isinstance(node, Node) and node.node_id not in self.nodes:
            self.nodes[node.node_id] = node # If supplied argument is a Node object, add it as is
            self.graph_nodes += 1
            return True
        elif (isinstance(node, int) or isinstance(node, int)) and node not in self.nodes:
            self.nodes[node] = Node(node) # If supplied argument is not a Node object, create one
            self.graph_nodes += 1
            return True
        else:
            return False

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
            t1 = self.nodes[n1].add_neighbor(n2, weight)
            t2 = self.nodes[n2].add_neighbor(n1, weight)
            # print(t1, t2)
            # Update the weight and edge count for the graph

            if t1 and t2:
                self.graph_weight += weight
                self.graph_edges += 1
                return True
        else:
            return False


    def remove_edge(self, n1, n2):
        """ Removes an edge between two nodes. """
        if n1 in self.nodes and n2 in self.nodes: # Check that both nodes are in the graph
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

    def sort_by_edge_weights(self, reverse = False):
        """ Sort nodes by weight of connections """
        sorted_edges = []
        skip = []
        for node in self.nodes:
            for n in self.nodes[node].neighbors:
                if [n[0], node] not in skip:
                    new_edge = [node, n[0], n[1]]
                    sorted_edges.append(new_edge)
                    skip.append([new_edge[0], new_edge[1]])
        sorted_edges.sort(key = lambda x: x[2], reverse = reverse)
        return sorted_edges

    def adj_mat(self):
        """ Returns a numpy array representing the adjaceny matrix of the graph. """
        # return (self.graph_nodes, self.graph_nodes)
        mat = np.zeros((self.graph_nodes, self.graph_nodes)) # Matrix of all zeros
        nodes = [nodes for nodes in self.nodes] # List of all node_id's in the graph
        nodes.sort() # Make sure they are sorted
        for node in nodes: # Loop through each node_id
            neighbors = len([node for node in self.nodes[node].neighbors]) # node_id's of current node's neighbors
            if neighbors == 0: # Check if the current node has any neighbors, and if not skip
                next
            else:
                l = [0] * len(nodes) # List of one zero for each node in the graph
                for ind in range(len(l)): # Loop through through the index for each node
                    if ind == nodes.index(node): # Skip if the index of the current node (preserve zero on diagonal)
                        next
                    else:
                        # Replace zeros with edge weights where they exist
                        l[ind] = sum([node[1] for node in self.nodes[node].neighbors if node[0] == nodes[ind]])
                mat[nodes.index(node)] = l # Set each row equal to the new edge weights
        return mat

    def has_cycle(self):
        """ Determine whether or not there areany cycles present in the current graph. """
        if self.graph_edges < 3: # Any graph with fewer than 3 edges cannot contain a cycle
            return False

        unvisited = [node for node in self.nodes] # Initially, all nodes are unvisited
        stack = [unvisited.pop()] # Pop the last node from unvisited to the stack (will traverse in reverse order)
        visited = [stack[0]] # Mark the first node as unvisited

        while len(stack) > 0: # Stack begins with 1 item, and the DFS is done if the stack is empty
            
                current_node = stack[-1] # The current node becomes the top item in the stack
                
                # The next_nodes are the neighbors of the current that have not yet been visited
                next_nodes = [node[0] for node in self.nodes[current_node].neighbors if node[0] not in visited]
                
                while len(next_nodes) > 0: # Loop as long as there are unvisited neighbor nodes
                    
                    parent = current_node # The current node is the parent
                    current_node = next_nodes.pop() # Traverse the network of unvisited neighbors, removing them as you go
                    
                    # Set the next nodes to visit to be the neighbors of the new current node 
                    next_nodes = [node[0] for node in self.nodes[current_node].neighbors if node[0] not in visited]
                    
                    # Check if any cycles are formed by the traveling to any of the current node's neighbors
                    for i in [node[0] for node in self.nodes[current_node].neighbors]: 
                        # A cycle is formed if the neighbor has been visited and is not the parent node
                        if i != parent and i in visited:
                            return True # Indicates there is a cycle and ends the function
                        
                    stack.append(current_node) # If no cycle is found, push the node to the stack
                    visited.append(current_node) # Mark the current node as visited
                    unvisited.remove(current_node) # Remove the current node from the list of unvisited nodes
                    
                stack.pop() # Pop off the top item in the stack
                
        return False # If the stack is empty, indicate that no cycles were found

    
    def mst(self):
        """ This is an implementation of Krsuskal's algorithm to find and return the 
            Mininmum Spanning Tree (MST) of the current graph """
        # Initialize an empty graph to add edges to (for construction of the MST)
        mst_tmp = Graph()

        # Add a node for each vertext
        for i in range(self.graph_nodes):
            mst_tmp.add_node(i)
        
        # The number of requires edges to terminate the algorithm
        required_edges = self.graph_nodes - 1 # A graph with nodes - 1 number of edges is spanning by definition
        sorted_edges = self.sort_by_edge_weights() # The list of edges to iterate through, sorted from least to most weighted
        
        # Loop while the graph is not spanning or there are still edges to check
        while mst_tmp.graph_nodes < required_edges or len(sorted_edges) > 0: 
            mst_tmp.add_edge(*sorted_edges[0]) # Add the current minimum edge to the appropriate nodes
            if mst_tmp.has_cycle(): # Check if a cycle is formed by adding the edge
                mst_tmp.remove_edge(*sorted_edges[0][:2]) # If so, remove the edge
            del sorted_edges[0] # Pop the edge off of the list of edges to test
        
        return mst_tmp
    
    def print_graph(self):
        """ Print the structure of the graph in plain English. Best used with smaller graphs. """
        for node, neighbors in self.nodes.items():
            print("Node %s has neighbor(s) and weight(s) %s" % (node, neighbors.neighbors))
