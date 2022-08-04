import argparse
import sys
import unittest

from command import Prompt


def main():
    prompt = Prompt()
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