from collections import deque


class TerrainError(Exception):
    """Generic error from building a terrain"""
    pass


class HexTerrainNode:

    def __init__(self, weight):
        self.weight = weight
        self.left_node = None
        self.up_node = None
        self.right_node = None
        self.down_node = None

    def __str__(self):  # pragma: nocover
        return "<Node: %s>" % hex(self.weight)

    def __repr__(self):  # pragma: nocover
        return self.__str__()

    @property
    def neighbours(self):
        """Returns a list of neighbour nodes"""
        return [n for n in (self.left_node, self.right_node,
                            self.up_node, self.down_node) if n is not None]

    def set_left_node(self, node):
        self.left_node = node
        node.right_node = self

    def set_right_node(self, node):
        self.right_node = node
        node.left_node = self

    def set_up_node(self, node):
        self.up_node = node
        node.down_node = self

    def set_down_node(self, node):
        self.down_node = node
        node.up_node = self


class HexGridTerrain:
    """The terrain which a TraversalRobot can navigate through"""

    def __init__(self):
        self.start_node = None
        self.end_node = None
        self._nodes = set()

    @property
    def nodes(self):
        return self._nodes

    def set_start_node(self, node):
        self.start_node = node

    def set_end_node(self, node):
        self.end_node = node

    def add_node(self, node):
        self._nodes.add(node)

    @classmethod
    def load_from_input(cls, input_string):
        """Loads a terrain from a string.

        Each row in the terrain is represented by a set of hexadecimal numbers
        seperated by a single space, ending in a new line character.

        Example:
        46B E59  EA C1F 45E  63
        899 FFF 926 7AD C4E FFF
        E2E 323 6D2 976 83F C96
        9E9 A8B 9C1 461 F74 D05
        EDD E94 5F4 D1D D03 DE3
         89 925 CF9 CA0 F18 4D2

        - Will throw value error if input number cannot be converted to hex

        :return: HexGridTerrain
        """

        # Parse the input into lists (rows) of Nodes
        raw_rows = input_string.split('\n')
        rows = []
        for raw_row in raw_rows:
            rows.append([HexTerrainNode(int(weight, 16)) for weight in raw_row.split()])

        # Validate that each row has same amount of nodes
        row_size = len(rows[0])
        for row in rows[1:]:
            if len(row) != row_size:
                raise TerrainError('Terrain rows have mismatching number of nodes.')

        # Build the terrain
        terrain = cls()
        terrain.set_start_node(rows[0][0])
        terrain.set_end_node(rows[-1][-1])

        if terrain.start_node == terrain.end_node:
            raise TerrainError('Terrain only consists of 1 node. This is not allowed')

        for row_number in range(len(rows)):
            for column_number in range(len(rows[row_number])):
                current_node = rows[row_number][column_number]
                terrain.add_node(current_node)

                # Set connection with node above
                if row_number > 0:
                    above_node = rows[row_number - 1][column_number]
                    current_node.set_up_node(above_node)

                # Set connection with node on the right
                try:
                    right_node = rows[row_number][column_number + 1]
                    current_node.set_right_node(right_node)
                except IndexError:
                    pass

        return terrain


class TraversalRobot:
    """A smart robot that can find the least-cost-path through a HexGridTerrain"""

    def dijkstra(self, terrain):
        """Algorithm to optimise finding the lowest cost path.
        Returns visited nodes and all paths for those nodes
        """
        visited = {terrain.start_node: 0}
        path = {}

        nodes = set(terrain.nodes)

        while nodes:
            min_node = None
            for node in nodes:
                if node in visited:
                    if min_node is None:
                        min_node = node
                    elif visited[node] < visited[min_node]:
                        min_node = node
            if min_node is None:
                break

            nodes.remove(min_node)
            current_weight = visited[min_node]

            # Traverse through all neighbouring nodes - U D L R
            for neighbour_node in min_node.neighbours:
                weight = current_weight + neighbour_node.weight

                # Update the path if lower weight
                if neighbour_node not in visited or weight < visited[neighbour_node]:
                    visited[neighbour_node] = weight
                    path[neighbour_node] = min_node

        return visited, path

    def traverse_terrain(self, terrain):
        """Runs the dijkstra algorithm to calculate the minimum cost and the path
        to the destination node.
        The path will be in the format of l,r,u,d from start node to end node.

        :return: (hexstr, str)"""
        visited, paths = self.dijkstra(terrain)
        full_path = deque()

        # The node to come to the destination node from
        predestination_node = paths[terrain.end_node]

        # Traverse backwards to get each node from last to first
        while predestination_node != terrain.start_node:
            full_path.appendleft(predestination_node)
            predestination_node = paths[predestination_node]

        # Add the start and end node to the path
        full_path.appendleft(terrain.start_node)
        full_path.append(terrain.end_node)

        weight = visited[terrain.end_node]

        # Build the path
        full_path, path = list(full_path), []
        for i in range(1, len(full_path)):
            current_node = full_path[i]
            prior_node = full_path[i-1]
            if prior_node.left_node == current_node:
                path.append('l')
            elif prior_node.right_node == current_node:
                path.append('r')
            elif prior_node.up_node == current_node:
                path.append('u')
            elif prior_node.down_node == current_node:
                path.append('d')
            else:  # pragma: nocover
                raise ValueError('Bad Node Mapping!! Does not join correctly')
        return hex(weight), ",".join(path)

