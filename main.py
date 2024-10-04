import os
import zipfile
import sys


class SimpleShell:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self.file_system = {}

        if not zipfile.is_zipfile(zip_path):
            raise ValueError("Provided file is not a valid zip file.")

        # Загрузка виртуальной файловой системы
        self.load_virtual_file_system()

    def load_virtual_file_system(self):
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            self.file_system = {name: zip_ref.read(name) for name in zip_ref.namelist()}

    def list_files(self):
        print("Содержимое виртуальной файловой системы:")
        for filename in self.file_system.keys():
            print(f"- {filename}")

    def cat(self, filename):
        if filename in self.file_system:
            print(self.file_system[filename].decode())
        else:
            print("Ошибка: Файл не найден.")

    def change_directory(self, directory):
        if directory == "..":
            if self.current_dir:
                self.current_dir = '/'.join(self.current_dir.split('/')[:-1])
        elif directory in self.file_system:
            self.current_dir = directory if directory.endswith('/') else directory + '/'
        else:
            print(f"cd: {directory}: Файл не найден")

    def tac(self, filename):
        if filename in self.file_system:
            content = self.file_system[filename].decode('utf-8').splitlines()
            for line in reversed(content):
                print(line)
        else:
            print(f"tac: {filename}: Файл не найден")

    def rmdir(self, directory):
        # Check if the directory is empty (i.e., has no files)
        is_empty = all(not filename.startswith(directory) for filename in self.file_system.keys())
        if is_empty:
            # Remove the directory by just changing the current directory's representation
            print(f"Удаленная директория: {directory}")
        else:
            print(f"rmdir: {directory}: Директория не пуста")

    def run_command(self, command):
        parts = command.split()
        if not parts:
            return

        cmd = parts[0]

        if cmd == 'ls':
            self.list_files()
        elif cmd == 'cat':
            if len(parts) < 2:
                print("Использование: cat <имя файла>")
            else:
                self.cat(parts[1])
        elif cmd.startswith("cd"):
            if len(parts) > 1:
                self.change_directory(parts[1])
            else:
                print("cd: отстутсвует аргумент")
        elif cmd == 'tac':
            if len(parts) > 1:
                self.tac(parts[1])
            else:
                print("tac: пропущен аргумент файл")
        elif cmd.startswith("rmdir"):
            if len(parts) > 1:
                self.rmdir(parts[1])
            else:
                print("rmdir: пропущен аргумент директория")
        elif cmd == 'exit':
            sys.exit(0)
        else:
            print(f"Ошибка: команда '{cmd}' не найдена.")

    def start(self):
        print(f"Эмулятор оболочки запущен. Используйте 'ls' для отображения файлов и 'exit' для выхода.")
        while True:
            command = input("$> ")
            self.run_command(command)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python shell_emulator.py <путь к zip файлу>")
        sys.exit(1)

    zip_file_path = sys.argv[1]
    shell = SimpleShell(zip_file_path)
    shell.start()
