"""Tests for the pattern and renaming logic in file_rename.py."""

import contextlib
import io
import os
import re
import tempfile
import unittest
from unittest import mock

import file_rename


class MakeStemTest(unittest.TestCase):
    def test_nn_is_replaced_by_zero_padded_index(self):
        self.assertEqual(file_rename.make_stem("image-NN", 3, ""), "image-03")

    def test_number_of_ns_sets_padding_width(self):
        self.assertEqual(file_rename.make_stem("shot_NNNN", 7, ""), "shot_0007")

    def test_index_wider_than_padding_is_not_truncated(self):
        self.assertEqual(file_rename.make_stem("img-NN", 123, ""), "img-123")

    def test_single_n_is_left_alone(self):
        self.assertEqual(file_rename.make_stem("N-NN", 1, ""), "N-01")

    def test_rnd_is_replaced_by_random_string(self):
        self.assertEqual(file_rename.make_stem("file-RND", 1, "a8f3k2xq"), "file-a8f3k2xq")

    def test_nn_and_rnd_can_be_combined(self):
        self.assertEqual(file_rename.make_stem("NN-RND", 2, "abcdefgh"), "02-abcdefgh")


class ValidatePatternTest(unittest.TestCase):
    def test_sequential_pattern_is_valid(self):
        self.assertIsNone(file_rename.validate_pattern("image-NN"))

    def test_random_pattern_is_valid(self):
        self.assertIsNone(file_rename.validate_pattern("file-RND"))

    def test_pattern_without_placeholder_is_rejected(self):
        self.assertIsNotNone(file_rename.validate_pattern("image"))

    def test_single_n_does_not_count_as_placeholder(self):
        self.assertIsNotNone(file_rename.validate_pattern("image-N"))


class BuildPlanTest(unittest.TestCase):
    def test_sequential_plan_numbers_files_in_order_and_keeps_extensions(self):
        plan = file_rename.build_plan(["a.jpg", "b.png", "c"], "pic-NN")
        self.assertEqual(plan, [("a.jpg", "pic-01.jpg"), ("b.png", "pic-02.png"), ("c", "pic-03")])

    def test_empty_file_list_gives_empty_plan(self):
        self.assertEqual(file_rename.build_plan([], "pic-NN"), [])

    def test_random_plan_gives_unique_eight_character_names(self):
        files = [f"f{i}.txt" for i in range(200)]
        plan = file_rename.build_plan(files, "x-RND")
        names = [new for _, new in plan]
        self.assertEqual(len(set(names)), len(files))
        for name in names:
            self.assertRegex(name, r"^x-[a-z0-9]{8}\.txt$")

    def test_random_plan_retries_a_repeated_string(self):
        draws = [list("aaaaaaaa"), list("aaaaaaaa"), list("bbbbbbbb")]
        with mock.patch.object(file_rename.random, "choices", side_effect=draws):
            plan = file_rename.build_plan(["one.txt", "two.txt"], "RND")
        self.assertEqual(plan, [("one.txt", "aaaaaaaa.txt"), ("two.txt", "bbbbbbbb.txt")])


class FolderTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = self._tmp.name
        self.src = os.path.join(self.root, "input")
        self.dst = os.path.join(self.root, "output")
        os.makedirs(self.src)

    def tearDown(self):
        self._tmp.cleanup()

    def touch(self, folder, name):
        with open(os.path.join(folder, name), "w") as fh:
            fh.write(name)

    def apply(self, plan, src, dst):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            file_rename.apply_plan(plan, src, dst)
        return out.getvalue()

    def test_get_files_is_sorted_and_skips_hidden_files_and_folders(self):
        for name in ["b.jpg", "a.jpg", ".DS_Store"]:
            self.touch(self.src, name)
        os.makedirs(os.path.join(self.src, "sub"))
        self.assertEqual(file_rename.get_files(self.src), ["a.jpg", "b.jpg"])

    def test_apply_moves_files_to_output_folder_and_creates_it(self):
        self.touch(self.src, "a.jpg")
        self.apply([("a.jpg", "pic-01.jpg")], self.src, self.dst)
        self.assertEqual(os.listdir(self.src), [])
        self.assertEqual(os.listdir(self.dst), ["pic-01.jpg"])

    def test_apply_in_place_renames_inside_input_folder(self):
        self.touch(self.src, "a.jpg")
        self.apply([("a.jpg", "pic-01.jpg")], self.src, self.src)
        self.assertEqual(os.listdir(self.src), ["pic-01.jpg"])
        self.assertFalse(os.path.exists(self.dst))

    def test_apply_skips_a_name_that_already_exists(self):
        self.touch(self.src, "a.jpg")
        os.makedirs(self.dst)
        self.touch(self.dst, "pic-01.jpg")
        out = self.apply([("a.jpg", "pic-01.jpg")], self.src, self.dst)
        self.assertEqual(os.listdir(self.src), ["a.jpg"])
        with open(os.path.join(self.dst, "pic-01.jpg")) as fh:
            self.assertEqual(fh.read(), "pic-01.jpg")
        self.assertTrue(re.search(r"1 skipped", out))


if __name__ == "__main__":
    unittest.main()
