# Общее описание
Эмулятор сеанса shell в UNIX-подобной ОС.
Эмулятор запускается из реальной командной строки, а файл с виртуальной файловой системой не распаковывается у пользователя.
Эмулятор принимает образ виртуальной файловой системы в виде файла формата tar. Эмулятор работает в режиме GUI.

# Описание всех функций и настроек
Конфигурационный файл имеет формат xml и содержит:
• Имя пользователя для показа в приглашении к вводу.
• Имя компьютера для показа в приглашении к вводу.
• Путь к архиву виртуальной файловой системы.
• Путь к лог-файлу.
Лог-файл имеет формат json и содержит все действия во время последнего
сеанса работы с эмулятором. Для каждого действия указан пользователь
В эмуляторе поддержаны комманды ls, cd, exit, date, rev, mv.

# Описание команд для сборки проекта.
```
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
```

# Примеры использования
![image](https://github.com/user-attachments/assets/47defef0-a8f6-4705-ae43-1179a705166c)
![image](https://github.com/user-attachments/assets/75b899c5-9d01-4186-aac3-dc711634daad)

# Результаты прогона тестов.
![image](https://github.com/user-attachments/assets/3b555a8e-9231-4ee2-8448-80a8abcaa793)
