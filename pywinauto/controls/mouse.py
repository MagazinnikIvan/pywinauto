from Xlib.display import Display
from Xlib import X
from Xlib.ext.xtest import fake_input


BUTTON_MAPPING = {'left': 1, 'middle': 2, 'right': 3, 'up_scroll': 4,
                  'down_scroll': 5, 'left_scroll': 6, 'right_scroll': 7}


def user_click(coord=(0, 0)):
    _perform_click('left', coord)


def user_double_click(coord=(0, 0)):
    _perform_click('left', coord)
    _perform_click('left', coord)


def user_right_click(coord=(0, 0)):
    _perform_click('right', coord)


def move_mouse(coords=(0, 0)):
    fake_input(_display, X.MotionNotify, x=int(coords[0]), y=int(coords[1]))
    _display.sync()


def user_press_mouse(coord=(0, 0)):
    _perform_click('left', coord, True, False)


def user_release_mouse(coord=(0, 0)):
    _perform_click('left', coord, False, True)


def user_vertical_scroll(wheel_dist=1, coord=(0, 0)):
    if wheel_dist == 0:
        return
    if wheel_dist > 0:
        button = 'up_scroll'
    if wheel_dist < 0:
        button = 'down_scroll'
    for i in range(abs(wheel_dist)):
        _perform_click(button, coord)


def user_horizontal_scroll(wheel_dist=1, coord=(0, 0)):
    if wheel_dist == 0:
        return
    if wheel_dist > 0:
        button = 'left_scroll'
    if wheel_dist < 0:
        button = 'right_scroll'
    for i in range(abs(wheel_dist)):
        _perform_click(button, coord)


def user_user_wheel_click(coord=(0, 0)):
    _perform_click('middle', coord)


def _perform_click(button='left', coord=(0, 0),
                   button_down=True, button_up=True):
    move_mouse(coord)
    button = BUTTON_MAPPING[button]
    if button_down:
        fake_input(_display, X.ButtonPress, button)
        _display.sync()
    if button_up:
        fake_input(_display, X.ButtonRelease, button)
        _display.sync()

_display = Display()
