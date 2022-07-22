# Dear programmer:
# When I wrote this code, only god and
# I knew how it worked.
# Now, only god knows it!
#
# Therefore, if you are trying to optimize
# this routine and it fails (most surely),
# please increase this counter as a
# warning for the next person:
#
# total_hours_wasted_here: 254

from time import sleep
import curses
import weakref
import vlc
import json
import os

#os.environ["VLC_VERBOSE"] = str("-1")

stdscr = curses.initscr()
curses.noecho()
curses.curs_set(0)
stdscr.keypad(1)
curses.mousemask(1)

ses = 40

loc = os.path.dirname(__file__)
with open(loc + '/data.json') as f:
    radio = json.load(f)


def auradio():
    stdscr.addstr('''                              
                                _ _        
       __ _ _   _ _ __ __ _  __| (_) ___   
      / _` | | | | '__/ _` |/ _` | |/ _ \  
     | (_| | |_| | | | (_| | (_| | | (_) | 
      \__,_|\__,_|_|  \__,_|\__,_|_|\___/  
                                           
    ''')
    stdscr.refresh()
    sleep(0.4)
    stdscr.clear()


def playerset(url):
    global ses

    vlc_instance = vlc.Instance('-q')
    player = vlc_instance.media_player_new()

    player.set_media(vlc_instance.media_new(url))
    player.audio_set_volume(ses)

    player.play()
    return player


def volbar():
    stdscr.addstr(0, 0, '┌')
    stdscr.addstr(0, 2, '┐')
    stdscr.addstr(11, 0, '└')
    stdscr.addstr(11, 2, '┘')

    for i in range(1, 11):
        stdscr.addstr(i, 0, '│')
        stdscr.addstr(i, 2, '│')
        stdscr.addstr(i, 1, '─')

    a = int(ses/10)
    while a > 0:
        stdscr.addstr(11 - a, 1, '▆')
        a = a - 1


def setvol(argument):
    switcher = {1: 100, 2: 90, 3: 80, 4: 70, 5: 60,
                6: 50, 7: 40, 8: 30, 9: 20, 10: 10, 11: 0, }
    return switcher.get(argument, "nothing")


def radioset():
    now = -1

    while True:
        radx = 4
        rady = 1

        for w in radio:
            stdscr.addstr(rady, radx, str(w["name"]))

            if (int(w["number"]) == now):
                stdscr.addstr(rady, radx, str(w["name"]), curses.A_BOLD)

            if rady == 10:
                rady = 0
                radx = radx + 23
                for i in range(1, 11):
                    stdscr.addstr(i, radx-2, '│')
            rady = rady + 1

        volbar()

        event = stdscr.getch()

        if event == curses.KEY_MOUSE:
            try: click = curses.getmouse()
            except: break

            if (click[2] <= 10 and click[2] >= 1 and click[1] < (int((len(radio)/10)*23)+2)):

                if click[1] < 3:
                    global ses
                    ses = setvol(click[2])
                    try:
                        scream.audio_set_volume(ses)
                        continue
                    except: pass

                # i dont know whats going on and
                # at this point i'm too afraid to ask
                now = (int((click[1]-2)/23)*10+click[2]-1)

                for w in radio:
                    if (str(w["number"]) == str(now)):
                        
                        try: scream.stop()
                        except: pass

                        scream = playerset(str(w["url"]))

        stdscr.refresh()

if __name__ == "__main__":
    stdscr.clear()
    stdscr.refresh()
    auradio()
    radioset()

curses.endwin()