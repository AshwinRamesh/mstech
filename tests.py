import pytest
from traversal_robot import HexGridTerrain, TraversalRobot, TerrainError, \
    HexTerrainNode


@pytest.fixture
def robot():
    return TraversalRobot()

def test_load_correct_terrain(robot):
    str_terrain = "46B E59  EA C1F 45E  63\n899 FFF 926 7AD C4E FFF\nE2E 323 6D2 976 83F C96\n9E9 A8B 9C1 461 F74 D05\nEDD E94 5F4 D1D D03 DE3\n89 925 CF9 CA0 F18 4D2"

    terrain = HexGridTerrain.load_from_input(str_terrain)
    assert len(terrain.start_node.neighbours) == 2
    weight, path = robot.traverse_terrain(terrain)

    assert path == 'r,r,d,d,r,d,d,r,r,d'

def test_up_left_movement(robot):
    str_terrain = "1 100 1 1 1\n1 1 1 100 1\n100 100 100 1 1\n100 100 100 1 100\n100 100 100 1 1"

    terrain = HexGridTerrain.load_from_input(str_terrain)
    weight, path = robot.traverse_terrain(terrain)

    assert weight == hex(12)
    assert path == 'd,r,r,u,r,r,d,d,l,d,d,r'

def test_single_row_terrain(robot):
    str_terrain = "1 100 100 100 1"
    terrain = HexGridTerrain.load_from_input(str_terrain)
    weight, path = robot.traverse_terrain(terrain)
    assert weight == '0x301'
    assert path == 'r,r,r,r'

def test_single_row_single_node(robot):
    str_terrain = "1"
    with pytest.raises(TerrainError):
        terrain = HexGridTerrain.load_from_input(str_terrain)

def test_zeroed_terrain(robot):
    str_terrain = "0 0 0\n0 0 0\n0 0 0"
    terrain = HexGridTerrain.load_from_input(str_terrain)
    weight, path = robot.traverse_terrain(terrain)
    assert weight == '0x0'

def test_bad_terrain(robot):
    str_terrain = "0 0 0\n0 0 0\n0 0"
    with pytest.raises(TerrainError):
        terrain = HexGridTerrain.load_from_input(str_terrain)


def test_bad_hex(robot):
    str_terrain = "g 0 0\n0 0 0\n0 0"
    with pytest.raises(ValueError):
        terrain = HexGridTerrain.load_from_input(str_terrain)


def test_node_connections():
    a = HexTerrainNode(1)
    b = HexTerrainNode(2)
    c = HexTerrainNode(3)
    d = HexTerrainNode(4)

    a.set_left_node(b)
    b.set_down_node(c)
    c.set_right_node(d)
    d.set_up_node(a)

    assert b.right_node == a
    assert c.up_node == b
    assert d.left_node == c
    assert a.down_node == d
