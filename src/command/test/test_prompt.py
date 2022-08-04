import unittest

from command import Prompt


class TestCommandPrompt(unittest.TestCase):
    def setUp(self):
        self.cmd = Prompt()

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


if __name__ == '__main__':
    unittest.main()
