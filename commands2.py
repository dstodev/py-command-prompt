import argparse


class CommandPrompt:
    def __init__(self):
        self.resume = True
        self._parser = argparse.ArgumentParser(description='My example command prompt')
        self._parser.add_argument('-q', '--quit', help='Quit the program', action='store_true')

    def process_input(self, input_string: str):
        args = self._parse_input_string(input_string)
        try:
            cli = self._parser.parse_args(args)
        except argparse.ArgumentError:
            pass
        else:
            if cli.quit:
                self.resume = False

    @staticmethod
    def _parse_input_string(input_string: str):
        return input_string.split()

    @staticmethod
    def print():
        print('Input command: ')


def main():
    prompt = CommandPrompt()
    while prompt.resume:
        prompt.print()
        input_string = input()
        prompt.process_input(input_string)


if __name__ == '__main__':
    main()
