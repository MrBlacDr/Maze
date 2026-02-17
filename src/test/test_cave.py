import unittest

from src.cave_gen import *


class TestMainFunctions(unittest.TestCase):
    def test_raw_cave(self):
        cave = generate_cave(4, 4)
        self.assertEqual(len(cave), 4)
        self.assertEqual(len(cave[0]), 4)

    def test_check_boards(self):
        cave = [[0 for _ in range(2)] for _ in range(2)]
        dead_cells = check_boards(0, 0, cave)
        expected = 0
        self.assertEqual(dead_cells, expected)
        cave[1][1] = 1
        expected = 1
        dead_cells = check_boards(0, 0, cave)
        self.assertEqual(dead_cells, expected)

    def test_one_iteration(self):
        cave = generate_cave(4, 4)
        new_cave = [[cave[i][j] for j in range(4)] for i in range(4)]
        new_cave = make_iteration(new_cave, 5, 3)
        self.assertNotEqual(new_cave, cave)

    def test_one_iteration_with_one_dead_cell(self):
        cave = [[0 for _ in range(3)] for _ in range(3)]
        cave[1][1] = 1
        cave = make_iteration(cave, 6, 6)
        self.assertEqual(cave[1][1], 0)
        self.assertEqual(cave[2][2], 0)

    def test_one_iteration_with_one_dead_cell_become_alive(self):
        cave = [[0 for _ in range(3)] for _ in range(3)]
        cave[1][1] = 1
        cave = make_iteration(cave, 3, 6)
        self.assertEqual(cave[1][1], 0)
        self.assertEqual(cave[2][2], 0)

    def test_many_iterations_for_steady_cave(self):
        cave = [[0 for _ in range(3)] for _ in range(3)]
        cave[1][1] = 1
        cave[2][0] = 1
        cave[0][2] = 1
        copy_cave = [[cave[i][j] for j in range(3)] for i in range(3)]
        cave = create_cave(cave, 7, 5)
        self.assertListEqual(cave, copy_cave)


if __name__ == '__main__':
    unittest.main()
