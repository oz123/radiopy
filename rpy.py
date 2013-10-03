from subprocess import Popen
import pty
import os
import sys
import pynotify


def parse_ICY(line):
    aline = line.split('\r\n')[-1]
    junk, info = aline.split('=', 1)
    try:
        info, junk = info.split(';', 1)
    except ValueError:
        pass
    artist, title = info.split('-')
    return artist.strip("'"), title.strip("'")

cmd = ['mplayer',
       '-playlist', 'http://www.radioparadise.com/musiclinks/rp_128aac.m3u']

if sys.argv[1:]:
    cmd = cmd[:1] + sys.argv[1:] + cmd[1:]

master, slave = pty.openpty()
proc = Popen(cmd, stdout=slave, stderr=slave)
stdout = os.fdopen(master)

ICYSTRING = ''

while True:
    line = stdout.readline(1)
    ICYSTRING = ICYSTRING + line
    if 'ICY Info' in ICYSTRING:
        for i in range(80):
            ICYSTRING = ICYSTRING + stdout.readline(1)
        a, t = parse_ICY(ICYSTRING)
        ICYSTRING = ''
        n = pynotify.Notification(a, t)
        n.set_timeout(10000)  # 10 sec
        n.set_category("device")
        pynotify.init("Timekpr notification")
        n.show()
        pynotify.uninit()
        ICYSTRING = ''
    sys.stdout.write(line)
