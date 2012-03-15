#!/usr/bin/python
# -*- coding: utf-8 -*-

#inspirat per http://stackoverflow.com/questions/1823762/sendkeys-for-python-3-1-on-windows/2004267#2004267

import ctypes as ct
#from win32con import SW_MINIMIZE, SW_RESTORE
#from win32ui import FindWindow, error as ui_err
from time import sleep


class cls_KeyBdInput(ct.Structure):
    _fields_ = [
        ("wVk", ct.c_ushort),
        ("wScan", ct.c_ushort),
        ("dwFlags", ct.c_ulong),
        ("time", ct.c_ulong),
        ("dwExtraInfo", ct.POINTER(ct.c_ulong) )
    ]

class cls_HardwareInput(ct.Structure):
    _fields_ = [
        ("uMsg", ct.c_ulong),
        ("wParamL", ct.c_short),
        ("wParamH", ct.c_ushort)
    ]

class cls_MouseInput(ct.Structure):
    _fields_ = [
        ("dx", ct.c_long),
        ("dy", ct.c_long),
        ("mouseData", ct.c_ulong),
        ("dwFlags", ct.c_ulong),
        ("time", ct.c_ulong),
        ("dwExtraInfo", ct.POINTER(ct.c_ulong) )
    ]

class cls_Input_I(ct.Union):
    _fields_ = [
        ("ki", cls_KeyBdInput),
        ("mi", cls_MouseInput),
        ("hi", cls_HardwareInput)
    ]

class cls_Input(ct.Structure):
    _fields_ = [
        ("type", ct.c_ulong),
        ("ii", cls_Input_I)
    ]


def make_input_objects( l_keys ):

    p_ExtraInfo_0 = ct.pointer(ct.c_ulong(0))

    l_inputs = [ ]
    for n_key, n_updown in l_keys:
        ki = cls_KeyBdInput( n_key, 0, n_updown, 0, p_ExtraInfo_0 )
        ii = cls_Input_I()
        ii.ki = ki
        l_inputs.append( ii )

    n_inputs = len(l_inputs)

    l_inputs_2=[]
    for ndx in range( 0, n_inputs ):
        s2 = "(1, l_inputs[%s])" % ndx
        l_inputs_2.append(s2)
    s_inputs = ', '.join(l_inputs_2)


    cls_input_array = cls_Input * n_inputs
    o_input_array = eval( "cls_input_array( %s )" % s_inputs )

    p_input_array = ct.pointer( o_input_array )
    n_size_0 = ct.sizeof( o_input_array[0] )

    # these are the args for user32.SendInput()
    return ( n_inputs, p_input_array, n_size_0 )

    '''It is interesting that o_input_array has gone out of scope
    by the time p_input_array is used, but it works.'''


def send_input( t_inputs ):

    rv = ct.windll.user32.SendInput( *t_inputs )

    return rv



# define some commonly-used key sequences
t_ctrl_s = (  # save in many apps
    ( 0x11, 0 ),
    ( 0x53, 0 ),
    ( 0x11, 2 ),
)
t_ctrl_r = (  # reload in some apps
    ( 0x11, 0 ),
    ( 0x52, 0 ),
    ( 0x11, 2 ),
)


def test():

    # file > open; a non-invasive way to test
    t_ctrl_o = ( ( 0x11, 0 ), ( 0x4F, 0 ), ( 0x11, 2 ), )

    # writes "Hello\n"
    # 0x10 is shift.  note that to repeat a key, as with 4C here, you have to release it after the first press
    t_hello = ( ( 0x10, 0 ), ( 0x48, 0 ), ( 0x10, 2 ), ( 0x45, 0 ), ( 0x4C, 0 ), ( 0x4C, 2 ), ( 0x4C, 0 ), ( 0x4F, 0 ), ( 0x0D, 0 ), )


    l_keys = [ ]
    ## l_keys.extend( t_ctrl_o )
    l_keys.extend( t_hello )
    l_keys.extend( t_ctrl_s )

    t_inputs = make_input_objects( l_keys )

    n = send_input( window1, t_inputs )

    ## print( "SendInput returned: %r" % n )
    ## print( "GetLastError: %r" % ct.windll.kernel32.GetLastError() )
    ## input( 'press enter to close' )



if __name__ == '__main__':
    test()
