import unittest

import os
import sys

sys.path.insert(0, os.path.abspath('../'))

from src.ML.q_learning import *
from src.ML.q_solve import *


class TestLearningFunctions(unittest.TestCase):
    def test_right_moves_to_goal(self):
        maze = [[Place(0, 0, 0), Place(1, 0, 2)], [Place(2, 0, 2), Place(3)]]
        col = 2
        end = maze[1][1]
        t1 = action_moves_agent_to_goal_state(col, maze[0][0], maze[0][1], end)
        t2 = action_moves_agent_to_goal_state(col, maze[0][0], maze[1][0], end)
        t3 = action_moves_agent_to_goal_state(col, maze[1][0], maze[0][0], end)
        t4 = action_moves_agent_to_goal_state(col, maze[1][0], maze[1][1], end)
        t5 = action_moves_agent_to_goal_state(col, maze[1][1], maze[1][1], end)
        self.assertTrue(t4)
        self.assertTrue(t5)
        self.assertFalse(t1)
        self.assertFalse(t2)
        self.assertFalse(t3)

    def test_right_valid_action(self):
        maze = [[Place(0, 0, 0), Place(1, 0, 2)], [Place(2, 0, 2), Place(3)]]
        col = 2
        t1 = action_is_valid(col, maze[0][0], maze[0][1])
        t2 = action_is_valid(col, maze[0][0], maze[1][0])
        t3 = action_is_valid(col, maze[0][1], maze[1][1])
        self.assertTrue(t1)
        self.assertTrue(t2)
        self.assertFalse(t3)

    def test_right_reward(self):
        maze = [Place(0, 0, 0), Place(1, 2, 2), Place(2, 0, 2), Place(3)]
        r = [[0 for _ in range(4)] for _ in range(4)]
        end = maze[3]
        for i in range(4):
            for j in range(4):
                reward(r, 2, maze[i], maze[j], end)
        expected = [[-1, 0, 0, -1],
                    [0, -1, -1, -1],
                    [0, -1, -1, 1],
                    [-1, -1, 0, 1]]
        self.assertEqual(r, expected)

    def test_right_connector(self):
        maze = [[Place(0, 0, 0), Place(1, 0, 2)], [Place(2, 0, 2), Place(3)]]
        d = connector(maze)
        self.assertTupleEqual(d[0], (0, 0))
        self.assertTupleEqual(d[3], (1, 1))

    def test_right_valid_next_states(self):
        maze = [Place(0, 0, 0), Place(1, 2, 2), Place(2, 0, 2), Place(3)]
        r = [[0 for _ in range(4)] for _ in range(4)]
        end = maze[3]
        for i in range(4):
            for j in range(4):
                reward(r, 2, maze[i], maze[j], end)
        ns = get_valid_next_states(1, r)
        self.assertListEqual(ns, [0])

    def test_right_normalize(self):
        q = [[0 for _ in range(4)] for _ in range(4)]
        q[1][1] = 2
        q[2][2] = 4
        s = normalize(q)
        expected_q = [[0 for _ in range(4)] for _ in range(4)]
        expected_q[1][1] = 0.5
        expected_q[2][2] = 1.0
        expected_s = 1.5
        self.assertListEqual(expected_q, q)
        self.assertEqual(expected_s, s)


class TestSolvingFunctions(unittest.TestCase):
    def test_get_right_best_states(self):
        maze = [Place(0, 0, 0), Place(1, 2, 2), Place(2, 0, 2), Place(3)]
        r = [[0 for _ in range(4)] for _ in range(4)]
        end = maze[3]
        for i in range(4):
            for j in range(4):
                reward(r, 2, maze[i], maze[j], end)
        index = get_best_next_state(r[3])
        self.assertEqual(index, 3)

    def test_right_found_path(self):
        expected_path = [(2, 0), (2, 1), (1, 1), (0, 1), (0, 2), (1, 2)]
        path = solve("../ML/origin_3x3.txt", (2, 0))
        self.assertListEqual(expected_path, path)


if __name__ == '__main__':
    unittest.main()
