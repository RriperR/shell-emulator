import os
import tarfile
import xml.etree.ElementTree as ET
import json
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext


# Функция загрузки конфигурационного файла
def load_config(config_path):
    tree = ET.parse(config_path)
    root = tree.getroot()

    config = {
        'user': root.find('user').text,
        'hostname': root.find('hostname').text,
        'tar_fs_path': root.find('tar_fs_path').text,
        'log_file_path': root.find('log_file_path').text
    }

    return config


# Функция загрузки виртуальной файловой системы из архива tar
def load_virtual_fs(tar_fs_path):
    virtual_fs_path = '/tmp/virtual_fs'
    if not os.path.exists(virtual_fs_path):
        os.makedirs(virtual_fs_path)
    with tarfile.open(tar_fs_path) as tar:
        tar.extractall(virtual_fs_path)
    return virtual_fs_path


# Функция логирования действий в JSON файл
def log_action(log_file_path, user, command):
    log_data = {
        'user': user,
        'command': command,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    with open(log_file_path, 'a') as log_file:
        log_file.write(json.dumps(log_data) + '\n')


# Команды оболочки

# Команда ls - показ содержимого текущей директории
def ls(current_path):
    try:
        return "\n".join(os.listdir(current_path))
    except FileNotFoundError:
        return f"Error: {current_path} not found."


# Команда cd - переход в другую директорию
def cd(current_path, target_dir):
    new_path = os.path.join(current_path, target_dir)
    if os.path.isdir(new_path):
        return new_path
    else:
        return f"Error: {target_dir} not found."


# Команда date - вывод текущей даты и времени
def date():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# Команда rev - переворот строки
def rev(text):
    return text[::-1]


# Команда mv - перемещение/переименование файлов или директорий
def mv(source, destination):
    try:
        os.rename(source, destination)
        return f"Moved {source} to {destination}."
    except FileNotFoundError:
        return f"Error: {source} not found."
    except PermissionError:
        return "Error: Permission denied."


# Команда exit - выход из эмулятора
def exit_emulator():
    print("Exiting emulator.")
    exit()


# Класс GUI оболочки
class EmulatorGUI:
    def __init__(self, root, user, hostname, virtual_fs_path, log_file_path):
        self.root = root
        self.user = user
        self.hostname = hostname
        self.virtual_fs_path = virtual_fs_path
        self.log_file_path = log_file_path
        self.current_path = virtual_fs_path

        # Настройка GUI
        self.root.title("Shell Emulator")

        self.command_entry = tk.Entry(self.root, width=100)
        self.command_entry.pack()

        self.output_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=20)
        self.output_area.pack()

        # Привязка команды на нажатие Enter
        self.command_entry.bind("<Return>", self.execute_command)

    # Функция выполнения команд
    def execute_command(self, event):
        command_input = self.command_entry.get()
        command_parts = command_input.split()
        if not command_parts:
            return

        command = command_parts[0]
        args = command_parts[1:]

        self.output_area.insert(tk.END, f"{self.user}@{self.hostname}:{self.current_path}$ {command_input}\n")

        # Логирование команды
        log_action(self.log_file_path, self.user, command_input)

        # Обработка команд
        if command == 'ls':
            output = ls(self.current_path)
        elif command == 'cd':
            if args:
                new_path = cd(self.current_path, args[0])
                if not new_path.startswith("Error"):
                    self.current_path = new_path
                output = new_path
            else:
                output = "Error: cd requires a directory argument."
        elif command == 'date':
            output = date()
        elif command == 'rev':
            if args:
                output = rev(" ".join(args))
            else:
                output = "Error: rev requires a string argument."
        elif command == 'mv':
            if len(args) == 2:
                source = os.path.join(self.current_path, args[0])
                destination = os.path.join(self.current_path, args[1])
                output = mv(source, destination)
            else:
                output = "Error: mv requires source and destination arguments."
        elif command == 'exit':
            exit_emulator()
        else:
            output = f"Error: Command '{command}' not found."

        # Вывод результата в область вывода
        self.output_area.insert(tk.END, output + '\n')
        self.command_entry.delete(0, tk.END)


# Основная функция запуска эмулятора
def main():
    # Загрузка конфигурации
    config_path = 'config.xml'  # путь к конфигурационному файлу
    config = load_config(config_path)

    # Загрузка виртуальной файловой системы
    virtual_fs_path = load_virtual_fs(config['tar_fs_path'])

    # Запуск GUI
    root = tk.Tk()
    app = EmulatorGUI(root, config['user'], config['hostname'], virtual_fs_path, config['log_file_path'])
    root.mainloop()


if __name__ == "__main__":
    main()
