import copy

class Node(object):
    """Represents a node in the graph"""
    def __init__(self, name):
        self.name = str(name)

    def get_name(self):
        return self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        # This function is necessary so that Nodes can be used as
        # keys in a dictionary, even though Nodes are mutable
        return self.name.__hash__()


class Edge(object):
    """Represents an edge in the dictionary. Includes a source and
    a destination."""
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest

    def get_source(self):
        return self.src

    def get_destination(self):
        return self.dest

    def __str__(self):
        return '{}->{}'.format(self.src, self.dest)


class WeightedEdge(Edge):
    def __init__(self, src, dest, total_distance, outdoor_distance):
        self.src = src
        self.dest = dest
        self.total_distance = total_distance
        self.outdoor_distance = outdoor_distance
        # TODO

    def get_total_distance(self):
        return self.total_distance
        # TODO

    def get_outdoor_distance(self):
        return self.outdoor_distance
        # TODO

    def __str__(self):
        return '{}->{} ({}, {})'.format(self.src, self.dest, self.total_distance, self.outdoor_distance)
        # TODO


class Digraph(object):
    """Represents a directed graph of Node and Edge objects"""
    def __init__(self):
        self.nodes = set([])
        self.edges = {}  # must be a dict of Node -> list of edges

    def __str__(self):
        edge_strs = []
        for edges in self.edges.values():
            for edge in edges:
                edge_strs.append(str(edge))
        edge_strs = sorted(edge_strs)  # sort alphabetically
        return '\n'.join(edge_strs)  # concat edge_strs with "\n"s between them

    def get_edges_for_node(self, node):
        return self.edges[node]

    def has_node(self, node):
        return node in self.nodes

    def add_node(self, node):
        """Adds a Node object to the Digraph. Raises a ValueError if it is
        already in the graph."""
        if self.has_node(node) != True:
            self.nodes.add(node)
        else:
            raise ValueError("Node {} is already in the graph.".format(node.get_name()))

    # TODO

    def add_edge(self, edge):
        """Adds an Edge or WeightedEdge instance to the Digraph. Raises a
        ValueError if either of the nodes associated with the edge is not
        in the  graph."""
        source = edge.get_source()
        dest = edge.get_destination()
        if source not in self.nodes or dest not in self.nodes:
            raise ValueError("Either node is not in the graph.")
        else:
            try:
                self.edges[source].append(edge)
            except KeyError:
                self.edges[source] = [edge]

def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """

    # TODO
    print("Loading map from file...")
    f = open(map_filename)
    line_list = []
    for line in f:
        clean_line = line.rstrip()
        line_list.append(clean_line)

    src_li = []
    dest_li = []
    weighted_edge_li = []

    for string in line_list:
        param = string.split(' ')
        src_li.append(Node(param[0]))
        dest_li.append(Node(param[1]))
        edge = WeightedEdge(src_li[-1], dest_li[-1], int(param[2]), int(param[3]))
        weighted_edge_li.append(edge)

    map = Digraph()
    for i in range(len(src_li)):
        try:
            map.add_node(src_li[i])
            map.add_node(dest_li[i])
        except ValueError as error:
            print(error)
            continue # will go next iter of this for-loop directly, skipping any code below it

    for i in range(len(src_li)):
        try:
            map.add_edge(weighted_edge_li[i])
        except ValueError as error1:
            print(error1)
            continue

    return map

# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out

# import os
# path = 'C:\\Users\\Duc Pham\\temp\\MIT\\MIT OCW intro course\\6.0002\\ps2'
# os.chdir(path)
# test_map = load_map('test_load_map.txt')
# print(test_map)

#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer: The objective function is to minimize total distance travelled. The constraints are maximum distance travelled
# outdoors.
#

# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist,
                  best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    # TODO

    if Node(start) and Node(end) not in digraph.nodes:
        raise ValueError("Either start or end not in map.")
    elif Node(start) == Node(end):
        # update the global variables appropriately
        print("cycle route")
        exit()
    else:
        start_edges = digraph.get_edges_for_node(Node(start))
        start_stem_edges = [edge for edge in start_edges if edge.get_source() == Node(start)]
        print("Start stem edges length:", len(start_stem_edges))
        # child_nodes = [edge.get_destination() for edge in start_edges if edge.get_source() == start]
        for edge in start_stem_edges:
            # print(path)
            current_path = copy.deepcopy(path)
            try:
                best_path = current_best_path
                best_dist = current_best_dist
            except UnboundLocalError:
                pass
            print("Best distance:", best_dist, "\nBest path:", best_path)
            print("Path original param:", current_path)
            print("Edge:", edge)
            if edge == start_stem_edges[-1]:
                print("Last edge from the current starting node.")
            dest_node = edge.get_destination().get_name()
            if dest_node not in current_path[0]:
                current_path[0].append(dest_node)
            else:
                print("Destination already in path list!")
                continue
            # print("Path new param:", current_path)
            # print(path)
            print("Path list:", current_path[0])
            try_path = [current_path[0], current_path[1] + edge.get_total_distance(), current_path[2]
                    + edge.get_outdoor_distance()]
            print("Try path:", try_path)

            try:
                if try_path[1] > best_dist:
                    print("Total distance exceeds best distance!")
                    continue
            except TypeError:
                pass
            if try_path[2] > max_dist_outdoors:
                print("Outdoor distance exceeds!")
                continue # may be improved by throwing a warning somewhere about strict constraints because sometimes
                            # the only possible start -> end path cannot satisfy certain constraints
            elif try_path[2] == max_dist_outdoors and edge.get_destination() != Node(end):
                print("Max outdoor distance reached, but hasn't got to the end!")
                continue
            else:
                if edge.get_destination() == Node(end):
                    if best_dist == None or try_path[1] < best_dist:
                        best_path = try_path[0]
                        print("Found new best path:", best_path)
                        best_dist = try_path[1]
                        return [best_path, best_dist]
                        break
                else:
                    new_start = edge.get_destination()
                    print("New start:", new_start)
                    [current_best_path, current_best_dist] = get_best_path(digraph, new_start, end, try_path,
                                                                           max_dist_outdoors, best_dist, best_path)
    return (best_path, best_dist)

map = load_map("mit_map.txt")
path = get_best_path(map, "12", "66", [["12"], 0, 0], 200, None, None)
print("Final best path:", path[0], "\nTotal distance:", path[1])
