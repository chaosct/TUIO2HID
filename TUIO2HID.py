#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TUIO2HID
(c) 2012 Carles F. Julià
This program translates TUIO events from reacTIVision
into keyboard events.
Change the file "mapping.txt" to change the mapping
between fiducial IDs and Keys.
"""

import keys
import keydict
from time import sleep
import tuio

def sendKeyEvent(s,updown):
        "Send a KeyBoard event"
        if s in keydict.CODES:
                code = keydict.CODES[s]
        elif len(s) == 1:
                code = ord(s.upper())
        else:
                print "ignoring unknown key: "+s
                return
        keys.send_input( keys.make_input_objects( ((code,updown),)) )

def pushK(s):
        "Send a Key Push event"
        sendKeyEvent(s,0)

def releaseK(s):
        "Send a Key Release event"
        sendKeyEvent(s,2)

def update():
        "Check if there are any changes in objets' presences"
        global objects
        tracking.update()
        nobjects = list(tracking.objects())
        newobjects = [o for o in nobjects if o not in objects]
        lostobjects = [o for o in objects if o not in nobjects]
        for obj in newobjects:
                newobject(obj)
        for obj in lostobjects:
                removeobject(obj)
        objects = nobjects

def newobject(o):
        "Callback when appearing a recognized fiducial in the image"
        if o.id in mapping:
                pushK(mapping[o.id])
def removeobject(o):
        "Callback when removing a recognized fiducial from the image"
        if o.id in mapping:
                releaseK(mapping[o.id])

def main():
        "Main function that starts the TUIO server and sends eyboard events"
        global tracking, objects, mapping
        try:
                filemapping = open("mapping.txt")
                mapping = eval(''.join(filemapping.readlines()),{},{})
        except IOError:
                mapping = { 0:'LEFT',1:'RIGHT'}
                fmapping = open("mapping.txt",'w')
                fmapping.write(
"""# TUIO2HID Mapping
#
# Format:
# {
#   fiducial_id : 'key_name',
#   fiducial_id : 'key_name',
#   fiducial_id : 'key_name',
# }
#
# fiducial_id must be an integer
# key_name is either a character or a value in this list:
#
""")
                for code in keydict.CODES:
                        fmapping.write("# "+code+"\n")
                fmapping.write("\n{\n0:'LEFT',\n1:'RIGHT',\n}\n")
                fmapping.close()

        tracking = tuio.Tracking(host='')
        objects = {}
        print (
"""
TUIO2HID
(c) 2012 Carles F. Julià
This program translates TUIO events from reacTIVision
into keyboard events.
Change the file "mapping.txt" to change the mapping
between fiducial IDs and Keys.

Press Ctrl-C to stop the program
""")

        try:
                while True:
                        update()
                        sleep(0.05)
        except KeyboardInterrupt:
                pass

if __name__ == "__main__":
        main()
