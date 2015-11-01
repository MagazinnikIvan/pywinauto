__author__ = 'ivan'
import sys
if sys.platform == 'linux':
    from Xlib.display import Display
    from Xlib import X
    from Xlib.ext.xtest import fake_input

if sys.platform == 'win32':
    from pywinauto import win32functions
    from pywinauto import win32defines
    from pywinauto.timings import Timings
    from pywinauto import win32structures
    import time
    import win32api

BUTTON_MAPPING = {'left': 1, 'middle': 2, 'right': 3, 'up_scroll': 4,
                  'down_scroll': 5, 'left_scroll': 6, 'right_scroll': 7}


if sys.platform == 'linux':
    _display = Display()
    def _perform_click_input(button='left', coord=(0, 0),
                             button_down=True, button_up=True, double = False):
        move(coord)
        button = BUTTON_MAPPING[button]
        if button_down:
            fake_input(_display, X.ButtonPress, button)
            _display.sync()
        if button_up:
            fake_input(_display, X.ButtonRelease, button)
            _display.sync()


elif sys.platform == 'win32':
    def _perform_click_input(
    button = "left",
    coords = (None, None),
    button_down = True,
    button_up = True,
    double = False,
    wheel_dist = 0,
    pressed = "",
    key_down = True,
    key_up = True,
    ):

        """Peform a click action using SendInput

        All the *ClickInput() and *MouseInput() methods use this function.

        Thanks to a bug report from Tomas Walch (twalch) on sourceforge and code
        seen at http://msdn.microsoft.com/en-us/magazine/cc164126.aspx this
        function now always works the same way whether the mouse buttons are
        swapped or not.

        For example if you send a right click to Notepad.Edit - it will always
        bring up a popup menu rather than 'clicking' it.
        """

        # Handle if the mouse buttons are swapped
        if win32functions.GetSystemMetrics(win32defines.SM_SWAPBUTTON):
            if button.lower() == 'left':
                button = 'right'
            elif button.lower() == 'right':
                button = 'left'

        events = []
        if button.lower() == 'left':
            if button_down:
                events.append(win32defines.MOUSEEVENTF_LEFTDOWN)
            if button_up:
                events.append(win32defines.MOUSEEVENTF_LEFTUP)
        elif button.lower() == 'right':
            if button_down:
                events.append(win32defines.MOUSEEVENTF_RIGHTDOWN)
            if button_up:
                events.append(win32defines.MOUSEEVENTF_RIGHTUP)
        elif button.lower() == 'middle':
            if button_down:
                events.append(win32defines.MOUSEEVENTF_MIDDLEDOWN)
            if button_up:
                events.append(win32defines.MOUSEEVENTF_MIDDLEUP)
        elif button.lower() == 'move':
            events.append(win32defines.MOUSEEVENTF_MOVE)
            events.append(win32defines.MOUSEEVENTF_ABSOLUTE)
        elif button.lower() == 'x':
            if button_down:
                events.append(win32defines.MOUSEEVENTF_XDOWN)
            if button_up:
                events.append(win32defines.MOUSEEVENTF_XUP)

        if button.lower() == 'wheel':
            events.append(win32defines.MOUSEEVENTF_WHEEL)


        # if we were asked to double click (and we are doing a full click
        # not just up or down.
        if double and button_down and button_up:
            events *= 2



        # set the cursor position
        win32api.SetCursorPos((coords[0], coords[1]))
        time.sleep(Timings.after_setcursorpos_wait)

        inp_struct = win32structures.INPUT()
        inp_struct.type = win32defines.INPUT_MOUSE

        keyboard_keys = pressed.lower().split()
        if ('control' in keyboard_keys) and key_down:
            SendKeys.VirtualKeyAction(SendKeys.VK_CONTROL, up = False).Run()
        if ('shift' in keyboard_keys) and key_down:
            SendKeys.VirtualKeyAction(SendKeys.VK_SHIFT, up = False).Run()
        if ('alt' in keyboard_keys) and key_down:
            SendKeys.VirtualKeyAction(SendKeys.VK_MENU, up = False).Run()


        inp_struct.mi.dwFlags = 0
        for event in events:
            inp_struct.mi.dwFlags |= event

        dwData = 0
        if button.lower() == 'wheel':
            dwData = wheel_dist
            inp_struct.mi.mouseData = wheel_dist
        else:
            inp_struct.mi.mouseData = 0

        if button.lower() == 'move':
            #win32functions.SendInput(     # vvryabov: SendInput() should be called sequentially in a loop [for event in events]
            #    win32structures.UINT(1),
            #    ctypes.pointer(inp_struct),
            #    ctypes.c_int(ctypes.sizeof(inp_struct)))
            X_res = win32functions.GetSystemMetrics(win32defines.SM_CXSCREEN)
            Y_res = win32functions.GetSystemMetrics(win32defines.SM_CYSCREEN)
            X_coord = int(float(coords[0]) * (65535. / float(X_res - 1)))
            Y_coord = int(float(coords[1]) * (65535. / float(Y_res - 1)))
            win32api.mouse_event(inp_struct.mi.dwFlags, X_coord, Y_coord, dwData)
        else:
            for event in events:
                inp_struct.mi.dwFlags = event
                win32api.mouse_event(inp_struct.mi.dwFlags, coords[0], coords[1], dwData)
                time.sleep(Timings.after_clickinput_wait)

        time.sleep(Timings.after_clickinput_wait)

        if ('control' in keyboard_keys) and key_up:
            SendKeys.VirtualKeyAction(SendKeys.VK_CONTROL, down = False).Run()
        if ('shift' in keyboard_keys) and key_up:
            SendKeys.VirtualKeyAction(SendKeys.VK_SHIFT, down = False).Run()
        if ('alt' in keyboard_keys) and key_up:
            SendKeys.VirtualKeyAction(SendKeys.VK_MENU, down = False).Run()




def click(coord=(0, 0)):
    _perform_click_input('left', coord)


def double_click(coord=(0, 0)):
    _perform_click_input('left', coord)
    _perform_click_input('left', coord)


def right_click(coord=(0, 0)):
    _perform_click_input('right', coord)


def move(coords=(0, 0)):
    fake_input(_display, X.MotionNotify, x=int(coords[0]), y=int(coords[1]))
    _display.sync()


def press(coord=(0, 0)):
    _perform_click_input('left', coord, True, False)


def release(coord=(0, 0)):
    _perform_click_input('left', coord, False, True)


def vertical_scroll(wheel_dist=1, coord=(0, 0)):
    if wheel_dist == 0:
        return
    if wheel_dist > 0:
        button = 'up_scroll'
    if wheel_dist < 0:
        button = 'down_scroll'
    for i in range(abs(wheel_dist)):
        _perform_click_input(button, coord)


def horizontal_scroll(wheel_dist=1, coord=(0, 0)):
    if wheel_dist == 0:
        return
    if wheel_dist > 0:
        button = 'left_scroll'
    if wheel_dist < 0:
        button = 'right_scroll'
    for i in range(abs(wheel_dist)):
        _perform_click_input(button, coord)


def wheel_click(coord=(0, 0)):
    _perform_click_input('middle', coord)
