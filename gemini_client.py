"""
Модуль для взаимодействия с Gemini API
"""
import os
import logging
import threading
from io import BytesIO
from PIL import ImageGrab
from typing import Dict, Any, List, Optional

# Импорт зависимостей для работы с Google Generative AI
from dotenv import load_dotenv
from google.generativeai import GenerativeModel, configure

# Получение логгера
logger = logging.getLogger("GeminiConsole")

# Загрузка переменных окружения
load_dotenv()

# Получение API-ключа из переменных окружения
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    logger.error("GEMINI_API_KEY не найден в переменных окружения")
    logger.error("Создайте файл .env с содержимым: GEMINI_API_KEY=ваш_ключ_api")
    exit(1)

# Конфигурация Gemini API
configure(api_key=api_key)

class GeminiConsole:
    """
    Консольный интерфейс для взаимодействия с Gemini API
    """
    def __init__(self):
        """Инициализация консольного интерфейса для Gemini"""
        # Используем модель gemini-2.0-flash
        self.model = GenerativeModel('gemini-2.0-flash')
        self.img_res = 1080
        self.conversation_history = []
        self.screenshot_queue = []  # Очередь для хранения скриншотов
        logger.info("Консоль Gemini инициализирована с моделью gemini-2.0-flash")
        
    def resize_image(self, image):
        """
        Изменяет размер изображения для оптимальной обработки
        
        Args:
            image: Исходное изображение
            
        Returns:
            Изображение с измененным размером
        """
        try:
            W, H = image.size
            image = image.resize((self.img_res, int(self.img_res * H / W)))
            return image
        except Exception as e:
            logger.error(f"Ошибка при изменении размера изображения: {e}")
            return image
    
    def capture_screenshot(self):
        """
        Захватывает скриншот экрана в фоновом режиме
        
        Returns:
            PIL.Image: Скриншот экрана
        """
        def _capture():
            try:
                screenshot = ImageGrab.grab()
                resized_screenshot = self.resize_image(screenshot)
                self.screenshot_queue.append(resized_screenshot)
                logger.info(f"Скриншот экрана получен и добавлен в очередь (всего: {len(self.screenshot_queue)})")
            except Exception as e:
                logger.error(f"Ошибка при захвате экрана: {e}")
        
        # Запускаем захват в отдельном потоке
        capture_thread = threading.Thread(target=_capture)
        capture_thread.daemon = True
        capture_thread.start()
    
    def send_message(self, message):
        """
        Отправляет сообщение в Gemini API
        
        Args:
            message (str): Текстовое сообщение
            
        Returns:
            str: Ответ от Gemini
        """
        try:
            # Добавление сообщения в историю
            self.conversation_history.append({"role": "user", "content": message})
            
            # Формирование контента для запроса
            content = []
            if message:
                content.append(message)
            
            # Добавляем все скриншоты из очереди
            if self.screenshot_queue:
                for screenshot in self.screenshot_queue:
                    content.append(screenshot)
                logger.info(f"Отправка запроса в Gemini с {len(self.screenshot_queue)} изображениями")
                # Очищаем очередь скриншотов после добавления в запрос
                self.screenshot_queue = []
            else:
                logger.info("Отправка запроса в Gemini без изображений")
                
            # Используем gemini-2.0-flash для всех типов запросов
            response = self.model.generate_content(content)
                
            # Получение ответа
            response_text = response.text
            
            # Добавление ответа в историю
            self.conversation_history.append({"role": "assistant", "content": response_text})
            
            return response_text
            
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения: {e}")
            return f"Произошла ошибка: {str(e)}"