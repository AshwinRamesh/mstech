from traversal_robot import HexGridTerrain

def test_load_correct_terrain():
    str_terrain = "46B E59  EA C1F 45E  63\n899 FFF 926 7AD C4E FFF\nE2E 323 6D2 976 83F C96\n9E9 A8B 9C1 461 F74 D05\nEDD E94 5F4 D1D D03 DE3\n89 925 CF9 CA0 F18 4D2"

    terrain = HexGridTerrain.load_from_input(str_terrain)
