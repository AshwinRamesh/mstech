class HexTerrainNode:

    def __init__(self, weight):
        self.weight = weight
        self.left_node = None
        self.up_node = None
        self.right_node = None
        self.down_node = None

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
        self._nodes = []

    def set_start_node(self, node):
        self.start_node = node

    def set_end_node(self, node):
        self.end_node = node

    def add_node(self, node):
        if node not in self._nodes:
            self._nodes.append(node)

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
                raise ValueError('Terrain rows have mismatching number of nodes.')

        # Build the terrain
        terrain = cls()
        terrain.set_start_node = rows[0][0]
        terrain.set_end_node = rows[-1][-1]

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
    pass
