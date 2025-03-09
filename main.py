"""
Главный файл для запуска консоли Gemini в cmd
"""
import os
import sys
import logging
import keyboard
import time
from gemini_client import GeminiConsole

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("gemini_console.log", mode="a")
    ]
)
logger = logging.getLogger("GeminiConsole")

def console_input(gemini_console):
    """
    Функция для получения ввода от пользователя в консоли
    
    Args:
        gemini_console: Экземпляр GeminiConsole
    """
    try:
        os.system('cls' if os.name == 'nt' else 'clear')  # Очистка экрана
        print("\n=== Gemini Console (gemini-2.0-flash) ===")
        print("Введите сообщение и нажмите Enter для отправки.")
        print("Горячие клавиши:")
        print("  F7 - захватить скриншот (можно несколько раз)")
        print("Скриншоты будут отправлены вместе с текстом после нажатия Enter.")
        print("Специальные команды:")
        print("  /clear - очистить историю диалога")
        print("  /exit, /quit или exit, quit - выход из программы")
        print("=====================================\n")

        # Проверяем, есть ли история диалога
        history_count = gemini_console.memory.get_user_message_count()
        if history_count > 0:
            print(f"[Загружена история диалога: {history_count} сообщений]")

        # Добавляем обработчики клавиш
        def on_key_press(e):
            if e.name == "f7":
                gemini_console.capture_screenshot()
                print("\n[Скриншот получен и будет отправлен с сообщением. Продолжайте ввод...]", end="\nВы: ", flush=True)

        
        # Регистрируем обработчик клавиш
        keyboard.on_press(on_key_press)
        
        while True:
            # Получаем ввод от пользователя
            user_input = input("\nВы: ")
            
            # Проверяем команду выхода
            if user_input.lower() in ['exit', 'quit', 'выход', '/exit', '/quit']:
                print("Завершение работы...")
                break
                
            # Проверяем команду очистки истории
            if user_input.lower() == '/clear':
                response = gemini_console.clear_history()
                print(f"\nСистема: {response}")
                continue
            
            # Отправляем сообщение со всеми накопленными скриншотами
            print("\nGemini: ", end="", flush=True)
            response = gemini_console.send_message(user_input)
            
            # Выводим ответ с задержкой для более естественного вида
            for char in response:
                print(char, end="", flush=True)
                time.sleep(0.005)
            print()
            
    except KeyboardInterrupt:
        print("\nРабота прервана пользователем")
    finally:
        # Удаляем обработчик клавиши при завершении
        keyboard.unhook_all()

def check_dependencies():
    """Проверка наличия необходимых зависимостей"""
    try:
        import google.generativeai
        from dotenv import load_dotenv
        from PIL import ImageGrab
        return True
    except ImportError as e:
        logger.error(f"Необходимые библиотеки не установлены: {e}")
        print("Необходимые библиотеки не установлены. Установите их с помощью pip:")
        print("pip install google-generativeai python-dotenv pillow keyboard")
        return False

def main():
    """
    Основная функция для запуска консоли Gemini
    """
    try:
        # Проверка зависимостей
        if not check_dependencies():
            return

        # Запуск консоли
        gemini_console = GeminiConsole()
        console_input(gemini_console)
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    # Запуск в новом окне cmd, если не запущено оттуда
    if os.name == 'nt' and 'PROMPT' not in os.environ:
        os.system(f'start cmd /k python "{os.path.abspath(__file__)}"')
    else:
        main()