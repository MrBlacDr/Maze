import unittest

from src.maze_genv3 import *


class TestInitial(unittest.TestCase):

    def test_fill_empty_values(self):
        expect = [Place(0), Place(0)]
        self.assertListEqual(maze_fill_empty_value(2), expect)

    def test_assign_unique_values(self):
        expect = [Place(0), Place(0)]
        expect[0].set = 1
        expect[1].set = 2
        line = maze_fill_empty_value(2)
        maze_assign_unique_set(line)
        self.assertListEqual(line, expect)


class TestSupportingFunctions(unittest.TestCase):

    def test_right_hash(self):
        line = [Place(0), Place(0), Place(0)]
        line[0].set = 1
        line[0].right_wall = 0
        line[1].set = 1
        line[2].set = 2
        expected_d = {1: [0, 1], 2: [2]}
        d = maze_hash_for_mutable_sets(line)
        self.assertDictEqual(d, expected_d)

    def test_right_merge(self):
        line = [Place(0) for _ in range(5)]
        expected_line = [Place(0) for _ in range(5)]
        for i in range(5):
            line[i].set = i + 1
        line[1].set = 1
        line[4].set = 1
        for i in range(5):
            expected_line[i].set = 4
        expected_line[2].set = 3
        d = maze_hash_for_mutable_sets(line)
        index = 3
        maze_merge_set(line, d, index)
        expected_d = {4: [3, 0, 1, 4], 3: [2]}
        self.assertDictEqual(d, expected_d)
        self.assertListEqual(line, expected_line)

    def test_list_of_unique(self):
        line = maze_fill_empty_value(5)
        line[0].set = 10
        line[1].set = 11
        list_unique = maze_get_list_of_unique(line)
        expected_list = [0, 10, 11]
        self.assertListEqual(list_unique, expected_list)

    def test_indices_for_choice(self):
        line = maze_fill_empty_value(5)
        line[0].set = 1
        line[1].set = 1
        line[2].set = 2
        for_choice = maze_list_indices_for_choice(line, line[1])
        expected_list = [0, 1]
        self.assertListEqual(for_choice, expected_list)


class TestBaseFunctions(unittest.TestCase):
    def test_first_line(self):
        line = maze_make_first_line(6)
        # проверка, что есть хотя бы один проход вниз
        assert any(line[i].down_wall == 0 for i in range(6))
        # проверка, что есть хотя бы одна стена справа
        assert any(line[i].right_wall == 2 for i in range(6))

    def test_next_line(self):
        line = maze_make_first_line(6)
        new_line = maze_make_other_line(6, line)
        list_unique = maze_get_list_of_unique(new_line)
        count_down_gapes = 0
        for i in range(6):
            if new_line[i].down_wall == 0:
                count_down_gapes += 1
        # проверка, что количество проходов вниз не меньше количества множеств
        assert count_down_gapes >= len(list_unique)

    def test_last_line(self):
        line = maze_make_first_line(6)
        new_line = maze_make_other_line(6, line)
        last_line = maze_make_last_line(6, new_line)
        list_unique = maze_get_list_of_unique(last_line)
        # проверка, что в последней строчке все множества объединились в одно
        assert len(list_unique) == 1


if __name__ == '__main__':
    unittest.main()
