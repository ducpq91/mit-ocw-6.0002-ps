# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer: The graph's nodes represent buildings/locations. The graph's edges represent the route between any two
# locations. The distances are represented as two parameters of the WeightedEdge object, total_distance and
# outdoor_distance.


# Problem 2b: Implementing load_map
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

    f.close()

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

    import copy

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
            else:
                if edge.get_destination() == Node(end):
                    if best_dist == None or try_path[1] < best_dist:
                        best_path = try_path[0]
                        print("Found new best path:", best_path)
                        best_dist = try_path[1]
                        return [best_path, best_dist]
                else:
                    new_start = edge.get_destination()
                    print("New start:", new_start)
                    [best_path, best_dist] = get_best_path(digraph, new_start, end, try_path,
                                                                           max_dist_outdoors, best_dist, best_path)
    return (best_path, best_dist)



# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    # TODO
    solution = get_best_path(digraph, start, end, [[start], 0, 0], max_dist_outdoors, max_total_dist, None)
    if solution[0] == None:
        raise ValueError
    else:
        return solution[0]


# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9']) #isn't this less optimal

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    unittest.main()
