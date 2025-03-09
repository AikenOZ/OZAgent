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
        print("Нажмите F7 в любой момент для захвата скриншота (можно несколько раз).")
        print("Скриншоты будут отправлены вместе с текстом после нажатия Enter.")
        print("Введите 'exit' или 'quit' для выхода.")
        print("=====================================\n")

        # Добавляем обработчик клавиши F7
        def on_f7_press(e):
            if e.name == "f7":
                gemini_console.capture_screenshot()
                print("\n[Скриншот получен и будет отправлен с сообщением. Продолжайте ввод...]", end="\nВы: ", flush=True)
        
        # Регистрируем обработчик клавиши
        keyboard.on_press(on_f7_press)
        
        while True:
            # Получаем ввод от пользователя
            user_input = input("\nВы: ")
            
            # Проверяем команду выхода
            if user_input.lower() in ['exit', 'quit', 'выход']:
                print("Завершение работы...")
                break
            
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