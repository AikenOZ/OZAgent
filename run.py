"""
Скрипт для запуска консоли Gemini в cmd
"""
import os
import subprocess

def main():
    """
    Основная функция для запуска консоли в cmd
    """
    # Определяем текущую директорию, где находится скрипт
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Путь к main.py
    main_script = os.path.join(current_dir, "main.py")
    
    # Запускаем cmd и выполняем скрипт
    cmd_command = f'cmd /k python "{main_script}"'
    
    try:
        # Для Windows
        if os.name == 'nt':
            subprocess.Popen(cmd_command, shell=True)
        # Для Linux/Mac
        else:
            subprocess.Popen(['python3', main_script], shell=False)
    except Exception as e:
        print(f"Ошибка при запуске консоли: {e}")

if __name__ == "__main__":
    main()