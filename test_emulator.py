import unittest
import os
from emulator import ls, cd, date, rev, mv, log_action
from datetime import datetime
import json


class TestEmulator(unittest.TestCase):

    def setUp(self):
        # Создаем тестовые директории и файлы для виртуальной файловой системы
        self.test_dir = "/tmp/test_virtual_fs"
        os.makedirs(self.test_dir, exist_ok=True)

        self.sub_dir = os.path.join(self.test_dir, "sub_dir")
        os.makedirs(self.sub_dir, exist_ok=True)

        self.test_file = os.path.join(self.test_dir, "test_file.txt")
        with open(self.test_file, 'w') as f:
            f.write("This is a test file.")

        self.log_file_path = "/tmp/test_log.json"
        if os.path.exists(self.log_file_path):
            os.remove(self.log_file_path)

    def tearDown(self):
        # Удаляем тестовую файловую систему после тестов
        if os.path.exists(self.test_dir):
            for root, dirs, files in os.walk(self.test_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(self.test_dir)

        # Удаляем тестовый лог-файл
        if os.path.exists(self.log_file_path):
            os.remove(self.log_file_path)

    # Тест команды ls
    def test_ls(self):
        result = ls(self.test_dir)
        self.assertIn("test_file.txt", result)
        self.assertIn("sub_dir", result)

    # Тест команды cd
    def test_cd(self):
        result = cd(self.test_dir, "sub_dir")
        self.assertEqual(result, os.path.join(self.test_dir, "sub_dir"))

        result = cd(self.test_dir, "nonexistent_dir")
        self.assertTrue(result.startswith("Error"))

    # Тест команды date
    def test_date(self):
        result = date()
        current_date = datetime.now().strftime('%Y-%m-%d')
        self.assertTrue(result.startswith(current_date))

    # Тест команды rev
    def test_rev(self):
        result = rev("Hello")
        self.assertEqual(result, "olleH")

        result = rev("World")
        self.assertEqual(result, "dlroW")

    # Тест команды mv
    # def test_mv(self):
        source = os.path.join(self.test_dir, "test_file.txt")
        destination = os.path.join(self.test_dir, "renamed_file.txt")

        result = mv(source, destination)
        self.assertEqual(result, f"Moved {source} to {destination}")

        self.assertTrue(os.path.exists(destination))
        self.assertFalse(os.path.exists(source))

        # Тест ошибки перемещения
        result = mv(source, destination)
        self.assertTrue(result.startswith("Error"))

    # Тест логирования действий
    def test_log_action(self):
        user = "test_user"
        command = "ls"
        log_action(self.log_file_path, user, command)

        # Проверка, что лог записан
        with open(self.log_file_path, 'r') as log_file:
            logs = [json.loads(line) for line in log_file]

        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]['user'], user)
        self.assertEqual(logs[0]['command'], command)
        self.assertIn('timestamp', logs[0])


if __name__ == "__main__":
    unittest.main()
