# TODO crossplatform join this tests with test_application.py
import sys
import os
import unittest
import subprocess
import time
#import pprint
#import pdb

sys.path.append(".")
from pywinauto.linux.application import Application, AppStartError, AppNotConnected

app_name = r"gtk_example.py"


def _test_app():
    test_folder = os.path.join(os.path.dirname
                               (os.path.dirname
                                (os.path.dirname
                                 (os.path.abspath(__file__)))),
                               r"apps/Gtk_samples")
    sys.path.append(test_folder)
    return os.path.join(test_folder, app_name)


def _test_app_cmd_line():
    return "python3.4 {}".format(_test_app())


sys.path.append(".")

if sys.platform != 'win32':
    class ApplicationTestCases(unittest.TestCase):

        """Unit tests for the application.Application class"""

        def setUp(self):
            """Set some data and ensure the application is in the state we want"""
            pass

        def tearDown(self):
            """Close the application after tests"""
            pass

        def test__init__(self):
            """Verify that Application instance is initialized or not"""
            self.assertRaises(ValueError, Application, backend='unregistered')

        def test_not_connected(self):
            """Verify that it raises when the app is not connected"""
            self.assertRaises(AppNotConnected, Application().__getattribute__, 'Hiya')
            self.assertRaises(AppNotConnected, Application().__getitem__, 'Hiya')
            self.assertRaises(AppNotConnected, Application().window_, title='Hiya')
            self.assertRaises(AppNotConnected, Application().top_window, )

        def test_start_problem(self):
            """Verify start_ raises on unknown command"""
            self.assertRaises(AppStartError, Application().start, 'Hiya')

        def test_start(self):
            """test start() works correctly"""
            app = Application()
            self.assertEqual(app.process, None)
            app.start(_test_app_cmd_line())
            self.assertNotEqual(app.process, None)
            app.kill()

        def test_connect_by_pid(self):
            """Create application wia subprocess then connect it to Application"""
            subprocess_app = subprocess.Popen(['python3.4', _test_app()], stdout=subprocess.PIPE, shell=False)
            time.sleep(1)
            app = Application()
            app.connect(process=subprocess_app.pid)
            self.assertEqual(app.process, subprocess_app.pid)
            app.kill()

        def test_connect_by_path(self):
            """Create application wia subprocess then connect it to Application by application name"""
            subprocess_app = subprocess.Popen(['python3.4', _test_app()], stdout=subprocess.PIPE, shell=False)
            time.sleep(1)
            app = Application()
            app.connect(path='python3.4 {}'.format(_test_app()))
            self.assertEqual(app.process, subprocess_app.pid)
            app.kill()

        def test_get_cpu_usage(self):
            app = Application()
            app.start(_test_app_cmd_line())
            time.sleep(1)
            self.assertGreater(app.cpu_usage(), 0)
            app.kill()

        def test_is_process_running(self):
            app = Application()
            app.start(_test_app_cmd_line())
            time.sleep(1)
            self.assertTrue(app.is_process_running())
            app.kill()

        def test_killed_app_not_running(self):
            app = Application()
            app.start(_test_app_cmd_line())
            time.sleep(1)
            app.kill()
            time.sleep(1)
            self.assertFalse(app.is_process_running())

        def test_kill_killed_app(self):
            app = Application()
            app.start(_test_app_cmd_line())
            time.sleep(1)
            app.kill()
            time.sleep(1)
            self.assertTrue(app.kill())

        def test_kill_connected_app(self):
            subprocess_app = subprocess.Popen(['python3.4', _test_app()], stdout=subprocess.PIPE, shell=False)
            time.sleep(1)
            app = Application()
            app.connect(process=subprocess_app.pid)
            app.kill()
            time.sleep(1)
            self.assertFalse(app.is_process_running())

if __name__ == "__main__":
    unittest.main()
