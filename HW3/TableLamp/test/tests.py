import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
try:
    import unittest as ut
except ImportError: #If you don't have the package, install it
    import pip
    pip.main(['install', '--user', 'unittest'])
    import unittest as ut
try:
    from contextlib import redirect_stdout
except ImportError: #If you don't have the package, install it
    import pip
    pip.main(['install', '--user', 'contextlib'])
    from contextlib import redirect_stdout
import io
try:
    import TableLamp.src.Lightbulb.Lightbulb as lb
    import TableLamp.src.Button.PushButton as pb
    import TableLamp.src.Button.Button as bu
except ImportError:
    print("Please make sure you are running tests.py from the test folder")


class Tests(ut.TestCase):

    def setUp(self):
        self.f = io.StringIO()

    def test_button(self):
        lightbulb = lb.Lightbulb()
        button = bu.Button(lightbulb)

        with redirect_stdout(self.f):
            button.switchOn()
            self.assertEqual(self.f.getvalue(), "Button switched to ON"
                                                "\nLightbulb on\n")
        self.f = io.StringIO()
        with redirect_stdout(self.f):
            button.switchOff()
            a = self.f.getvalue()
            self.assertEqual(self.f.getvalue(), "Button switched to OFF"
                                                "\nLightbulb off\n")

    def test_pushbutton(self):
        lightbulb = lb.Lightbulb()
        button = pb.PushButton(lightbulb)

        with redirect_stdout(self.f):
            button.PushButton()
            self.assertEqual(self.f.getvalue(), "Button switched to ON\nLightbulb on\n")
            self.assertTrue(button.on)
        self.f = io.StringIO()
        with redirect_stdout(self.f):
            button.PushButton()
            self.assertEqual(self.f.getvalue(), "Button switched to OFF\nLightbulb off\n")
            self.assertFalse(button.on)


if __name__ == "__main":

    ut.main()
