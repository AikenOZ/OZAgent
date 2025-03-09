"""
Модуль для управления историей диалогов (памятью) для Gemini Console
"""
import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

# Получение логгера
logger = logging.getLogger("GeminiConsole.Memory")

class MemoryController:
    """
    Контроллер для управления историей диалогов
    """
    def __init__(self, memory_dir: str = None):
        """
        Инициализация контроллера памяти
        
        Args:
            memory_dir (str, optional): Путь к директории для хранения памяти. 
                                       По умолчанию используется директория 'memory' в корне проекта.
        """
        # Определяем директорию для хранения памяти
        if memory_dir is None:
            # Если директория не указана, используем директорию 'memory' в корне проекта
            self.memory_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "memory")
        else:
            self.memory_dir = memory_dir
            
        # Создаем директорию, если она не существует
        os.makedirs(self.memory_dir, exist_ok=True)
        
        # Определяем путь к файлу с историей диалогов
        self.memory_file = os.path.join(self.memory_dir, "memory.json")
        
        # Загружаем историю диалогов
        self.conversation_history = self.load_conversation_history()
        
        logger.info(f"Контроллер памяти инициализирован. Путь к файлу памяти: {self.memory_file}")
    
    def load_conversation_history(self) -> List[Dict[str, Any]]:
        """
        Загружает историю диалога из файла
        
        Returns:
            list: История диалога
        """
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                logger.info(f"История диалога загружена из {self.memory_file}")
                return history
            else:
                logger.info("Файл истории диалога не существует, создаем новую историю")
                return []
        except Exception as e:
            logger.error(f"Ошибка при загрузке истории диалога: {e}")
            return []
    
    def save_conversation_history(self) -> bool:
        """
        Сохраняет историю диалога в файл
        
        Returns:
            bool: True если сохранение прошло успешно, иначе False
        """
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
            logger.info(f"История диалога сохранена в {self.memory_file}")
            return True
        except Exception as e:
            logger.error(f"Ошибка при сохранении истории диалога: {e}")
            return False
    
    def add_user_message(self, message: str) -> None:
        """
        Добавляет сообщение пользователя в историю
        
        Args:
            message (str): Текст сообщения
        """
        self.conversation_history.append({
            "role": "user", 
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        self.save_conversation_history()
    
    def add_assistant_message(self, message: str) -> None:
        """
        Добавляет сообщение ассистента в историю
        
        Args:
            message (str): Текст сообщения
        """
        self.conversation_history.append({
            "role": "assistant", 
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        self.save_conversation_history()
    
    def add_system_message(self, message: str) -> None:
        """
        Добавляет системное сообщение в историю
        
        Args:
            message (str): Текст сообщения
        """
        self.conversation_history.append({
            "role": "system", 
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        self.save_conversation_history()
    
    def clear_history(self) -> None:
        """
        Очищает историю диалога
        """
        self.conversation_history = []
        self.save_conversation_history()
        logger.info("История диалога очищена")
    
    def format_history_for_context(self) -> str:
        """
        Форматирует историю диалога для передачи в качестве контекста модели
        
        Returns:
            str: Отформатированная история диалога
        """
        formatted_history = []
        for message in self.conversation_history:
            role = "Пользователь" if message["role"] == "user" else "Gemini"
            if message["role"] != "system":  # Пропускаем системные сообщения в контексте
                formatted_history.append(f"{role}: {message['content']}")
        
        # Объединяем историю в одну строку с разделителями
        return "\n\n".join(formatted_history)
    
    def get_message_count(self) -> int:
        """
        Возвращает количество сообщений в истории
        
        Returns:
            int: Количество сообщений в истории
        """
        return len(self.conversation_history)
    
    def get_user_message_count(self) -> int:
        """
        Возвращает количество сообщений пользователя в истории
        
        Returns:
            int: Количество сообщений пользователя
        """
        return sum(1 for message in self.conversation_history if message["role"] == "user")