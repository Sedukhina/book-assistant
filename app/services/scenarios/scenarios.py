import inspect

from services.scenarios.book_scenarios import get_commands as book_commands
from services.scenarios.user_scenarios import get_commands as user_commands

commands = dict()
commands.update(book_commands())
commands.update(user_commands())

def execute_command(command):
    command = command.lower()

    for key, action in commands.items():
        for item in key:
            if item in command:
                params_count = len(inspect.signature(action).parameters)
                if params_count == 0:
                    return action()
                elif params_count == 1:
                    return action(command.replace(item,'').strip())
                elif params_count >1:
                    return action(command.replace(item,'').strip().split(',')) # dummy stub

    return 'Вибачте, я не розумію'