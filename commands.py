import argparse
import sys
import typing as T
import unittest


class CommandHandler(T.Protocol):  # more like 'commandler' haha
    def __call__(self, *args: str): ...


class CommandPrompt:
    def __init__(self):
        self._commands = {}

    def register_command(self, symbol: str, command_handler: CommandHandler):
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


class TestCommandPrompt(unittest.TestCase):
    def setUp(self):
        self.cmd = CommandPrompt()

    def test_fire_command_none_registered(self):
        with self.assertRaises(ValueError):
            self.cmd.fire_command('test')

    def test_register(self):
        tokens = []
        handler = lambda *t: tokens.extend(t)
        self.cmd.register_command('test', handler)
        self.cmd.fire_command('test', 'some', 'strings')
        self.assertEqual(2, len(tokens))
        self.assertIn('some', tokens)
        self.assertIn('strings', tokens)

    def test_register_duplicate(self):
        handler = lambda *_: ...
        self.cmd.register_command('test', handler)
        with self.assertRaises(ValueError):
            self.cmd.register_command('test', handler)

    def test_input_string_command_only(self):
        tokens = []
        handler = lambda *_: tokens.extend(('some', 'strings'))
        self.cmd.register_command('test', handler)
        self.cmd.process_input_string('test')
        self.assertEqual(2, len(tokens))
        self.assertIn('some', tokens)
        self.assertIn('strings', tokens)

    def test_input_string_command_not_registered(self):
        with self.assertRaises(ValueError):
            self.cmd.process_input_string('test some strings')

    def test_input_string(self):
        tokens = []
        handler = lambda *t: tokens.extend(t)
        self.cmd.register_command('test', handler)
        self.cmd.process_input_string('test some strings')
        self.assertEqual(2, len(tokens))
        self.assertIn('some', tokens)
        self.assertIn('strings', tokens)


def main():
    prompt = CommandPrompt()
    resume = True

    def quit_handler(*args):
        nonlocal resume
        resume = False

    def echo_handler(*args):
        print(*args)

    prompt.register_command('quit', quit_handler)
    prompt.register_command('q', quit_handler)
    prompt.register_command('echo', echo_handler)

    while resume:
        input_string = input('Input a command: ')
        try:
            prompt.process_input_string(input_string)
        except ValueError as e:
            print(*e.args)


def parse_cli_args():
    args = argparse.ArgumentParser(description='Example command console')
    args.add_argument('-t', '--test', help='Run script tests', action='store_true')
    cli = args.parse_args()
    return cli


if __name__ == '__main__':
    cli = parse_cli_args()
    if cli.test:
        argv = [sys.argv[0]]
        unittest.main(argv=argv)
    else:
        main()
