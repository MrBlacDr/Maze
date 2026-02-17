import unittest

import os
import sys

sys.path.insert(0, os.path.abspath('../'))

from maze_solution import find_path, make_solution, convert_from_file


class TestFindPath(unittest.TestCase):

    def test_right_path_1(self):
        start = (0, 0)
        end = (1, 0)
        expected_path = [(0, 0), (0, 0), (0, 1), (1, 1), (2, 1), (2, 0), (1, 0), (1, 0)]
        _, _, maze = convert_from_file("../mazes/from_readme.txt")
        _, path = find_path(maze, start, end, [start, start])
        self.assertListEqual(path, expected_path)

    def test_right_path_2(self):
        start = (1, 2)
        end = (3, 0)
        expected_path = [(1, 2), (1, 2), (1, 1), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (2, 2), (3, 2), (3, 1), (3, 0),
                         (3, 0)]
        _, _, maze = convert_from_file("../mazes/from_readme.txt")
        _, path = find_path(maze, start, end, [start, start])
        self.assertListEqual(path, expected_path)

    def test_point_out_of_range(self):
        with self.assertRaises(ValueError):
            make_solution("../mazes/from_readme.txt", (1, 1), (1, 4),
                          '../image/maze.png', '../image/modified_maze.png')


if __name__ == '__main__':
    unittest.main()
