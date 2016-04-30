"Test for mouse.py"

import time
import copy
import ctypes
import locale
import subprocess
import re
import sys
import os
import unittest
if sys.platform == 'win32':
    import win32clipboard
    from pywinauto.application import Application
    from pywinauto.SendKeysCtypes import SendKeys
    from pywinauto import mouse
else:
    from Xlib.display import Display
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)
    import mouse
    send_keys_dir = os.path.join(parent_dir, r"Linux/")
    sys.path.insert(0, send_keys_dir)
    from SendKeys import SendKeys
    import clipboard


def _test_app():
    test_folder = os.path.join(os.path.dirname
                               (os.path.dirname
                                (os.path.dirname
                                 (os.path.abspath(__file__)))),
                               r"apps/MouseTester")
    if sys.platform == 'win32':
        return os.path.join(test_folder, "mousebuttons.exe")
    else:
        return os.path.join(test_folder, "mousebuttons")


class MouseTests(unittest.TestCase):

    def setUp(self):
        if sys.platform == 'win32':
            self.app = Application()
            self.app.start(_test_app())
            self.dlg = self.app.mousebuttons
        else:
            self.display = Display()
            self.app = subprocess.Popen(_test_app(), shell=True)
            time.sleep(1)

    def tearDown(self):
        time.sleep(1)
        if sys.platform == 'win32':
            self.app.kill_()
        else:
            self.app.kill()

    def __get_pos(self, shift):
        if sys.platform == 'win32':
            rect = self.dlg.Rectangle()
            return rect.left + shift, rect.top + shift
        else:
            root = self.display.screen().root
            left_pos = root.get_geometry().width / 2
            top_pos = root.get_geometry().height / 2
            return 300+shift, 300+shift

    def __get_text(self):
        # this function will be change after clipboard.py changes
        data = ''
        SendKeys('^a')
        SendKeys('^c')
        if sys.platform == 'win32':
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
        else:
            data = clipboard.get_data()
            print(data)
        return data

    def test_position(self):
        left, top = self.__get_pos(60)
        mouse.click(coords=(left, top))
        data = self.__get_text()
        self.assertTrue(str(top) in data)
        self.assertTrue(str(left) in data)

    def test_click(self):
        mouse.click(coords=(self.__get_pos(50)))
        data = self.__get_text()
        self.assertTrue("LeftButton" in data)
        self.assertTrue("Mouse Press" in data)
        self.assertTrue("Mouse Release" in data)

    def test_double_click(self):
        mouse.double_click(coords=(self.__get_pos(50)))
        data = self.__get_text()
        self.assertTrue("Mouse DoubleClick" in data)

    def test_press_release(self):
        left, top = self.__get_pos(50)
        left1, top1 = self.__get_pos(20)
        mouse.press(coords=(left, top))
        mouse.release(coords=(left1, top1))
        data = self.__get_text()
        self.assertEqual(str(top) in data, str(top1) in data)
        self.assertEqual(str(left) in data, str(left1) in data)

    def test_right_click(self):
        mouse.right_click((self.__get_pos(50)))
        data = self.__get_text()
        self.assertTrue("Mouse Press" in data)
        self.assertTrue("Mouse Release" in data)
        self.assertTrue("RightButton" in data)

    def test_vertical_scroll(self):
        mouse.scroll((self.__get_pos(50)), 5)
        mouse.scroll((self.__get_pos(50)), -5)
        data = self.__get_text()
        self.assertTrue("UP" in data)
        self.assertTrue("DOWN" in data)

    def test_wheel_click(self):
        mouse.wheel_click((self.__get_pos(50)))
        data = self.__get_text()
        self.assertTrue("Mouse Press" in data)
        self.assertTrue("Mouse Release" in data)
        self.assertTrue("MiddleButton" in data)
    if sys.platform != 'win32':
        def test_swapped_buttons(self):
            current_map = self.display.get_pointer_mapping()
            swapped_map = copy.copy(current_map)
            swapped_map[0], swapped_map[2] = swapped_map[2], swapped_map[0]
            self.display.set_pointer_mapping(swapped_map)
            try:
                mouse.right_click((self.__get_pos(50)))
                data = self.__get_text()
                self.assertTrue("RightButton" in data)
            finally:
                self.display.set_pointer_mapping(current_map)

if __name__ == "__main__":
    unittest.main()
