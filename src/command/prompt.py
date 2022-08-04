from .handler import Handler


class Prompt:
    def __init__(self):
        self._commands = {}
        self._default = None

    def register_command(self, symbol: str, command_handler: Handler):
        """Register a command with associated callback.

        :param symbol: The name of the command.
        :param command_handler: Callback fired when command is provided;
            all tokens after the command name are passed as parameters.
        """
        if symbol in self._commands:
            raise ValueError(f'Command "{symbol}" is already registered!')
        self._commands[symbol] = command_handler

    def register_default(self, default_handler: Handler):
        """Register a default callback.

        Callback is fired when the input text is not recognized as a registered command.

        :param default_handler: Callback fired when unrecognized command is provided;
            all tokens are passed as parameters.
        """
        self._default = default_handler

    def process_input_string(self, input_string: str):
        """Accept a string of input from the user.

        If ``input_string`` starts with a valid command name, the associated callback
        is fired, and all tokens after the command name are passed as parameters.

        :param input_string: String to process.
        """
        tokens = self._parse_input_string(input_string)
        self.fire_command(*tokens)  # 'symbol' arg is the first token in the list

    @staticmethod
    def _parse_input_string(input_string: str):
        tokens = input_string.split()
        if tokens:
            return tokens
        else:
            return ['']

    def fire_command(self, symbol: str, *args: str):
        """Fire callback associated with command, passing all additional arguments as parameters.

        :param symbol: Name of the command to fire.
        :param args: Optional list of arguments to pass to the command callback.
        """
        try:
            self._commands[symbol](*args)
        except KeyError:
            registered_default = self._default is not None

            if registered_default:
                self._default(symbol, *args)
            else:
                # Convert to ValueError because a command name is abstract from the storage medium, i.e. not a 'key'
                raise ValueError(f'Command "{symbol}" is not registered!')
