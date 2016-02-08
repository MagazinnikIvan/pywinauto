"Test for mouse.py"

import time
import ctypes
import locale
import re
import subprocess
import sys
import os
import win32clipboard
import unittest
from pywinauto.application import Application
from pywinauto.SendKeysCtypes import SendKeys
sys.path.append(os.path.split
                (os.path.dirname
                 (os.path.abspath(__file__)))[0])
import mouse


def _test_app():
    test_folder = os.path.join(os.path.split
                               (os.path.split
                                (os.path.dirname
                                 (os.path.abspath(__file__)))[0])[0],
                               r"apps/MouseTester")
    if sys.platform == 'linux':
        return os.path.join(test_folder, "mousebuttons")
    elif sys.platform == 'win32':
        return os.path.join(test_folder, "mousebuttons.exe")


class MouseTests(unittest.TestCase):

    def setUp(self):
        #self.app = subprocess.Popen(_test_app())
        self.app = Application()
        self.app.start(_test_app())
        self.dlg = self.app.mousebuttons

    def tearDown(self):
        time.sleep(1)
        self.app.kill_()

    def __get_pos(self, shift):
        rect = self.dlg.Rectangle()
        return rect.left + shift, rect.top + shift

    def __get_text(self):
        SendKeys('^a')
        SendKeys('^c')
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        return data

    def test_position(self):
        left, top = self.__get_pos(50)
        mouse.click((left, top))
        data = self.__get_text()
        self.assertNotEqual(data.find(str(top)), -1)
        self.assertNotEqual(data.find(str(left)), -1)

    def test_click(self):
        mouse.click((self.__get_pos(50)))
        data = self.__get_text()
        self.assertNotEqual(data.find("LeftButton"),
                            data.rfind("LeftButton"))
        self.assertNotEqual(data.find("Mouse Press"), -1)
        self.assertNotEqual(data.find("Mouse Release"), -1)

    def test_double_click(self):
        mouse.double_click((self.__get_pos(50)))
        data = self.__get_text()
        self.assertNotEqual(data.find("Mouse DoubleClick"), -1)

    def test_pres_release(self):
        left, top = self.__get_pos(50)
        left1, top1 = self.__get_pos(20)
        mouse.press((left, top))
        mouse.release((left1, top1))
        data = self.__get_text()
        self.assertNotEqual(data.find(str(top)), data.find(str(top1)))
        self.assertNotEqual(data.find(str(left)), data.find(str(left1)))

    def test_right_click(self):
        mouse.right_click((self.__get_pos(50)))
        data = self.__get_text()
        self.assertNotEqual(data.find("RightButton"),
                            data.rfind("RightButton"))

    def test_vertical_scrol(self):
        mouse.scroll(5, (self.__get_pos(50)))
        mouse.scroll(-5, (self.__get_pos(50)))
        data = self.__get_text()
        self.assertNotEqual(data.find("UP"), -1)
        self.assertNotEqual(data.find("DOWN"), -1)

    def test_wheel_click(self):
        mouse.wheel_click((self.__get_pos(50)))
        data = self.__get_text()
        self.assertNotEqual(data.find("MiddleButton"),
                            data.rfind("MiddleButton"))

if __name__ == "__main__":
    unittest.main()
