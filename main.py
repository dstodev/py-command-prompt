import argparse
import enum
import multiprocessing as mp

from command import Prompt


class Signal(enum.Enum):
    QUIT = enum.auto()
    UNKNOWN = enum.auto()


def main():
    ctx = mp.get_context()
    input_strings = ctx.Queue()
    responses = ctx.Queue()
    process = ctx.Process(target=process_commands, args=(input_strings, responses))
    process.start()

    response = None

    while response != Signal.QUIT:
        input_string = input('Input a command: ')
        input_strings.put(input_string)
        response = responses.get()
        try:
            print(*response)
        except TypeError:
            print(response)

    process.join()


def process_commands(input_strings: mp.Queue, responses: mp.Queue):
    resume = True

    def quit_handler(*_args):
        nonlocal resume
        resume = False
        responses.put(Signal.QUIT)

    def echo_handler(*args):
        responses.put(args)

    def default_handler(*_args):
        # The main process will block waiting for a response,
        # so even unrecognized commands must put some response
        responses.put(Signal.UNKNOWN)

    prompt = Prompt()
    prompt.register_default(default_handler)
    prompt.register_command('quit', quit_handler)
    prompt.register_command('q', quit_handler)
    prompt.register_command('echo', echo_handler)

    while resume:
        try:
            input_string = input_strings.get()
            prompt.process_input_string(input_string)
        except ValueError as e:
            print(*e.args)


def parse_cli_args():
    args = argparse.ArgumentParser(description='Example command console')
    args.add_argument('-t', '--test', help='Run project tests', action='store_true')
    return args.parse_args()


if __name__ == '__main__':
    cli = parse_cli_args()
    if cli.test:
        import unittest as ut

        test_loader = ut.TestLoader()
        test_suite = test_loader.discover('src')
        test_runner = ut.TextTestRunner()
        test_runner.run(test_suite)
    else:
        main()
