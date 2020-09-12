
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build Preliminaries Map of PacMan Game"""

import queue
from pacman.utils import (
    load_map, prettify_map, uncompress_map_with_rle, simplify_map)
from pacman.constants import WALL, POINTS, ENERGIZER, ROCK, GO

DEFAULT_START_NODE = (13, 22)


class Map:
    """A class define Pac-Man map"""

    def __init__(self, data):
        """The Constructor of Map class
        Arguments:
            data {list} -- the content of a Pac-Man map file.
        """
        self.data = data
        self.width = self.get_width()
        self.height = self.get_height()
        self.grip = self.get_grip()
        self.pretty_map = self._get_pretty_map(self.data)
        self.wall_coordinates = self.__get_wall_coordinates_list()
        self.point_coordinates = self.__get_points_coordinates_list()[0]
        self.energizer_coordinates = self.__get_points_coordinates_list()[1]
        self.weighted_graph = []
        self.graph = {}

    def get_width(self):
        """Get width of the grip"""
        width_list = [len(line) for line in self.data]
        return max(width_list)

    def get_height(self):
        """Get height of the grip"""
        return len(self.data)

    def get_grip(self):
        """Get grip of the map"""
        grip = []
        for line in self.data:
            if len(line) != self.width:
                sub = (self.width - len(line))*" "
                line += sub
            grip.append(list(line))
        return grip

    @staticmethod
    def load_map(file_pathname):
        """Load Pac-Man Map
        Arguments:
            file_pathname {str} -- the file path name of a Pac-Man map
        Raises:
            FileNotFoundError: Provided file path name is not found
            IOError: Provided file path name can not accessible by read mode
        Returns:
            list -- A list of lines of Pac-Man Map
        """
        file_type = ''.join(file_pathname.split("/")).split(".")[-1]
        contents = load_map(file_pathname)
        if file_type == 'rle':
            return Map(uncompress_map_with_rle(contents))
        if file_type == 'map':
            return Map(contents)
        if file_type == 'amap':
            return Map(simplify_map(contents))
        raise ValueError("Do not support this type of file")

    @staticmethod
    # Get pretty map
    def _get_pretty_map(data):
        return prettify_map(data)

    # Get a list of WALL coordinates
    def __get_wall_coordinates_list(self):
        wall_coordinates = []
        for row in range(self.height):
            for col in range(self.width):
                if self.grip[row][col] == WALL:
                    wall_coordinates.append((row, col))
        return wall_coordinates

    # Get 2 list of POINTS amd ENERGIZER in provided map
    def __get_points_coordinates_list(self):
        points_coordinates = []
        energizer = []
        for row in range(self.height):
            for col in range(self.width):
                symbol = self.grip[row][col]
                if symbol == POINTS:
                    points_coordinates.append((row, col))
                elif symbol == ENERGIZER:
                    energizer.append((row, col))

        return points_coordinates, energizer

    def __create_cell_objects(self):
        # create a dictionary with key is the coordinate of the given point
        # and value is its cell objects
        cell_objects_dict = {}
        for y in range(self.height):
            for x in range(self.width):
                cell_objects_dict[x, y] = Cell(
                    self.__identify_id(x, y, self.width-1), x, y)
        return cell_objects_dict

    def build_graph(self, x, y):
        """Build graph maze of the Pacman Game

        Arguments:
            x {int} -- x-location of the cell in the map
            y {int} -- y-location of the cell in the map

        Raises:
            ValueError: provided x, y are not the integers

        Returns:
            list -- list of objects Cell corresponding to connected cells,
            i.e., the walkable tiles of the maze (graph).
        """
        if not all([isinstance(i, int) for i in (x, y)]):
            raise ValueError("The location x, y must be the intergers")
        # Get a first walkable
        cell = (x, y)
        # Initialize an cell as a mark to end the loop
        end_mark = -1
        # Initialize a stack with `end_mark` at the first element.
        stack = [end_mark]
        # Create a dict with key is coordinates and values is its Cell Object
        cell_objects = self.__create_cell_objects()
        # Initialize a dic to store all walkable step in maze
        result_graph = {}

        # We will loop from the first walkable Cell
        #  1.At each of cell, find all legal neighbors of this point (it's not a
        #       WALL(*) or GO(-) or ROCK(x)) and add them to stack.
        #  2.Then take respectively each of them from the stack, consider if
        #       it is walkable in maze or not, then remove it from the stack.
        #  3. Continute loop until there's no cell apart from the end_mark
        count = 0
        while not (stack[-1] == end_mark and count != 0):
            count += 1
            # Do nothing if the step is wall
            if (y, x) in self.wall_coordinates:
                continue

            # Get all legal neighbor cell objects
            neighbors = self.__get_legal_neighbor_cells(cell)

            # Check condition to add neighbor point to stack
            for point in neighbors:
                cell_objects[cell].add_neighbor_cell(cell_objects[point])
                cell_objects[point].add_neighbor_cell(cell_objects[cell])
                if point in result_graph:
                    continue
                if point in stack:
                    continue
                stack.append(point)

            # Take the last element of stack to check then remove it to stack
            temp_cell = stack.pop()

            # Update the Cell for next turn
            cell = temp_cell
            if temp_cell in result_graph:
                continue
            result_graph.setdefault(temp_cell, cell_objects[temp_cell])
            # print(count, result_graph)
        # del cell_objects
        self.graph = result_graph
        return list(result_graph.values())

    def build_weighted_graph(self, x, y):
        """Build a weighted graph of the Pacman Game

        Arguments:
            x {int} -- x-location of the cell in the map
            y {int} -- y-location of the cell in the map

        Raises:
            ValueError: provided x, y are not the integers

        Returns:
            list -- list of objects Node corresponding to connected cells
        """
        if not all([isinstance(i, int) for i in (x, y)]):
            raise ValueError("The location x, y must be the intergers")

        intersection_cells = self.__get_intersection(x, y)
        weighted_graph = {}
        for cell in intersection_cells:
            weighted_graph[cell] = Node(cell)
        for cell in intersection_cells:
            node = weighted_graph[cell]
            dic = self.__get_intersection_neighbors(cell, intersection_cells)
            for neighbor, distance in dic.items():
                # Create Node Object and add its neighbors
                neighbor_node = weighted_graph[neighbor]
                node.add_neighbor_node(neighbor_node, distance)
        return list(weighted_graph.values())

    def find_shortest_path(self, source_node, destination_node):
        """Find the shorteds path from source node to destination
            Dijkstra's algorithm.

        Arguments:
            source_node {Node object} -- node where to start
            destination_node {Node object} -- destination

        Returns:
            list --  a list of objects Node corresponding to the shortest
                route from source_node to destination_node.
        """
        # Manage weighted node dictionary with keys are Node objects and
        # value is its index
        weighted_node_dic = self.__get_weighted_node_dict()
        # Get the shortest path to all Node
        path = self.__implement_dijkstra(source_node, weighted_node_dic)
        # Get the index of destination node
        destination = weighted_node_dic[destination_node]
        # Initialize a list trace back through destinations in shortest path
        shortest_route = [destination]
        # Loop to find shortest route until reaching the source
        while shortest_route[-1] != weighted_node_dic[source_node]:
            next_step = path[destination]
            shortest_route.append(next_step)
            destination = next_step

        shortest_route.reverse()
        # Return a route of objects Node
        return [key for id_ in shortest_route for key, val
                in weighted_node_dic.items() if id_ == val]

    @staticmethod
    # Find the shortest path from source node to all node of
    # weighted_node_dict, using Dijkstra's algorithm.
    def __implement_dijkstra(source_node, weighted_node_dic):
        # Set up a PriorityQueue
        priority_queue = queue.PriorityQueue()
        priority_queue.put(source_node)

        # A list to constantly calculate the smallest distance
        distances = [int(1e9) for i in range(len(weighted_node_dic))]
        # A list to track the visited node
        path = [-1 for i in range(len(weighted_node_dic))]

        while not priority_queue.empty():
            # Get the next node with smallest distance to starting
            top = priority_queue.get()
            index = weighted_node_dic[top]
            dis = top.distance
            # For each connection, update its path and total distance from
            # starting node if the total distance is less than the current dis
            for neighbor_tuple in top.neighbor_nodes:
                distance, neighbor = neighbor_tuple
                if dis + distance < distances[weighted_node_dic[neighbor]]:
                    neighbor.distance = distance + dis
                    distances[weighted_node_dic[neighbor]] = dis + distance
                    # Take andvantages of `put()` of PriorityQueue, an element
                    # with high priority (smallest distance) is dequeued before
                    # an element with low priority
                    priority_queue.put(neighbor)
                    path[weighted_node_dic[neighbor]] = index

        return path

    def _get_weighted_graph(self):
        if self.weighted_graph == []:
            x, y = DEFAULT_START_NODE
            self.weighted_graph = self.build_weighted_graph(x, y)
        return self.weighted_graph

    def __get_weighted_node_dict(self):
        # Get a dictionary with keys are Node objects and value is its index
        graph = self._get_weighted_graph()
        weighted_node_dic = {}
        for i, node in enumerate(graph):
            weighted_node_dic[node] = i
        return weighted_node_dic

    def __get_intersection(self, x, y):
        # Get a list of all the intersection in :maze
        graph = self.build_graph(x, y)
        return [cell for cell in graph if cell.is_intersection()]

    @staticmethod
    # Get all neighbors of the given intersection
    # Return a dictionary with key is the Cell object (a neighbor of
    # the given point) and value is distance corresponds to the number of
    # cells to traverse from the given point and its neighbor
    def __get_intersection_neighbors(point, intersection_list):
        # Initialize the result dictionary
        intersection_neighbors = {}
        stack = [-1]
        temp_list = [point]
        count = 0
        # From the given point (an intersection) --> Loop to get ALL neighbors
        # (until there's no cell apart from -1 )
        while not (stack[-1] == -1 and count != 0):
            count += 1
            distance = 0
            if count != 1:
                temp_cell = stack.pop()
                point = temp_cell
                if temp_cell in temp_list:
                    continue
                temp_list.append(temp_cell)
            # From the given point(an intersection) --> Loop to get ONE neighbor
            # (until it catchs another intersection)
            c = 0
            while True:
                c += 1
                distance += 1
                neighbors = point.neighbor_cells
                for neighbor in neighbors:
                    if neighbor in temp_list:
                        continue
                    if neighbor in stack:
                        continue
                    stack.append(neighbor)
                temp_cell = stack.pop()
                point = temp_cell
                if temp_cell in temp_list:
                    continue

                temp_list.append(temp_cell)
                if temp_cell in intersection_list:
                    if count != 1:
                        distance += 1
                    intersection_neighbors.setdefault(temp_cell, distance)
                    break

        # del temp_list
        return intersection_neighbors


    def get_the_nearest_intersection(self, current):
        stack = []
        count = 0
        graph = self.graph

        for cell, obj in graph.items():
            if (cell[0], cell[1]) == current:
                current_cell = obj
        temp_list = [current_cell]
        weighted_graph_id = [(cell.x, cell.y) for cell in self.weighted_graph]

        # From the given current(an intersection) --> Loop to get ONE neighbor
        # (until it catchs another intersection)
        while True:
            count += 1
            neighbors = current_cell.neighbor_cells
            for neighbor in neighbors:
                if neighbor in temp_list:
                    continue
                if neighbor in stack:
                    continue
                stack.append(neighbor)
            temp_cell = stack.pop()
            current_cell = temp_cell
            if temp_cell in temp_list:
                continue
            temp_list.append(temp_cell)
            if (temp_cell.x, temp_cell.y) in weighted_graph_id:
                break
        return temp_cell

    @staticmethod
    # Get the coordinate of 4 neighbor of the given point(x, y)
    def __define_4_neighbors(x, y, height, width):
        neighbors = (
            (x, max(y - 1, 0)),
            (min(x+1, width - 1), y),
            (x, min(y+1, height - 1)),
            (max(x - 1, 0), y))
        neighbors = list(set(neighbors))
        return neighbors

    # Get all legal neighbor cells
    def __get_legal_neighbor_cells(self, cell):
        x, y = cell
        legal_neighbor = [
            cell for cell in self.__define_4_neighbors(
                x, y, self.height, self.width)
            if self.grip[cell[1]][cell[0]] != WALL
            and self.grip[cell[1]][cell[0]] != ROCK
            and self.grip[cell[1]][cell[0]] != GO]
        return legal_neighbor

    @staticmethod
    # Return an id of given (x, y) and width as the width of the map
    def __identify_id(x, y, width):
        return y * width + (x + y)


class Cell:
    """A class Cell represent walkable tiles of the Pac-Man maze"""

    def __init__(self, id_, x, y):
        """The constructor of Cell class

        Arguments:
            id {int} -- The unique identification of the cell in the map
            x {int} -- x-location of the cell in the map
            y {int} -- y-location of the cell in the map

        ValueError: provided id, x, y are not the integers

        """
        if not isinstance(id_, int):
            raise ValueError("The identification must be a interger")
        if not all([isinstance(i, int) for i in (x, y)]):
            raise ValueError("The location x, y must be the intergers")
        self.__id = id_
        self.__x = x
        self.__y = y
        self.neighbor_cells = []

    @property
    def x(self):
        """Represent to x-location of the cell in the map """
        return self.__x

    @property
    def y(self):
        """Represent to y-location of the cell in the map """
        return self.__y

    @property
    def id(self):
        """Represent to the unique identification of the cell in the map"""
        return self.__id

    def __repr__(self):
        """Return a string representation of this cell"""
        return f'{self.__class__.__name__}(x={self.x}, y={self.y}, id={self.id})'

    def add_neighbor_cell(self, other):
        """Add `other` as an neighbor

        Arguments:
            other {pacman.Cell object}
        """
        if other not in self.neighbor_cells:
            self.neighbor_cells.append(other)

    def is_intersection(self):
        """Check if given cell is intersection or not

        Returns:
            [boolean]
            `True` if this cell is an intersection of several routes of
                a maze (i.e., the cell is connected to 3 or 4 neighbor cells)
            `False` otherwise
        """
        if len(self.neighbor_cells) >= 3:
            return True
        return False


class Node:
    """A Class represents to Node"""

    # Function to initialise the node object
    def __init__(self, cell):
        """The constructor of the class Node

        Arguments:
            cell {model.map.Cell object}
        """
        self.__cell = cell
        self.neighbor_nodes = []
        self.id = self.cell.id
        self.x = self.cell.x
        self.y = self.cell.y
        self.distance = 0

    @property
    def cell(self):
        """Represent to the cell object"""
        return self.__cell

    def add_neighbor_node(self, node, distance):
        """Add neighbor nodes of the provided node

        Arguments:
            node {Node Object} -- the neighbor node
            distance {int} --  the number of cells to traverse from the
                current node self to this node node
        """
        if not isinstance(distance, int):
            raise ValueError("Distance must be an integer")
        self.neighbor_nodes.append((distance, node))

    def __lt__(self, other):
        return self.distance <= other.distance
