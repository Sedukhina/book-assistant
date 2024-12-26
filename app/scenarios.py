def process_command(command):
    """
    Обробляє текстову команду і повертає відповідь.
    """
    command = command.lower()
    if "порекомендуй книгу" in command:
        return "Рекомендую прочитати 'Гаррі Поттер' або 'Війна і мир'."
    elif "відкрий бібліотеку" in command:
        return "Відкриваю бібліотеку."
    else:
        return "Вибачте, я не розумію команду."
