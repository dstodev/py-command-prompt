from command.handler import Handler


class Prompt:
    def __init__(self):
        self._commands = {}

    def register_command(self, symbol: str, command_handler: Handler):
        if symbol in self._commands:
            raise ValueError(f'Command "{symbol}" is already registered!')
        self._commands[symbol] = command_handler

    def process_input_string(self, input_string: str):
        if input_string:
            tokens = self.parse_input_string(input_string)
            self.fire_command(*tokens)  # 'symbol' arg is the first token in the list

    @staticmethod
    def parse_input_string(input_string: str):
        return input_string.split()

    def fire_command(self, symbol: str, *args: str):
        try:
            self._commands[symbol](*args)
        except KeyError:
            # Convert to ValueError because a command name is abstract from the storage medium, i.e. not a 'key'
            raise ValueError(f'Command "{symbol}" is not registered!')
