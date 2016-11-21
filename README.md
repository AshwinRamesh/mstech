# Mathspace Technical Challenge

## Question

A robot which can move down and right is traversing some terrain that can be represented as a hex grid. Find the least cost path from top left to bottom right through such a grid. Return the path for the robot to follow.

Sample input
46B E59  EA C1F 45E  63
899 FFF 926 7AD C4E FFF
E2E 323 6D2 976 83F C96
9E9 A8B 9C1 461 F74 D05
EDD E94 5F4 D1D D03 DE3
 89 925 CF9 CA0 F18 4D2

Sample output
r,r,d,d,r,d,d,r,r,d

Bonus: Consider allowing the robot to move up and left.

## Technology Used

   * Python 3.5
   * PyTest


## Assumptions Made

   * Weight is only added as the robot moves to a new node. Thus the start node will never be part of the weight, but the end node will.

   * The terrain will always be N x M in size. i.e. Rectangular in shape

   * The first least-costly path will be returned


## Installation

   1. Create a virtualenv:  `virtualenv -p python3 env3`
   2. Activate the venv: `source env3/bin/activate`
   3. Install requirements: `pip3 install -r requirements.txt`
   4. Use as required!!

## Usage

To use the algorithm, you must first create a valid Terrain. The Terrain is then fed into an instance of the Robot, which will return the lowest cost and the path taken from start (top-left) to finish (bottom-right) node.


    # Terrain String
    str_terrain = "46B E59  EA C1F 45E  63\n899 FFF 926 7AD C4E FFF\nE2E 323 6D2 976 83F C96\n9E9 A8B 9C1 461 F74 D05\nEDD E94 5F4 D1D D03 DE3\n89 925 CF9 CA0 F18 4D2"

    # Create a terrain from the string
    terrain = HexGridTerrain.load_from_input(str_terrain)

    # Create a robot and pass in the terrain
    weight, path = TraversalRobot().traverse_terrain(terrain)

    print(path)

    >> "r,r,d,d,r,d,d,r,r,d"


## Tests

To run tests, use the command: `py.test --cov=traversal_robot --cov-report term-missing tests.py`. This will give a coverage report and run the tests against the code.
