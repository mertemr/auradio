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
# total_hours_wasted_here: 254.32

if __import__("sys").platform == "win32":
    print("Sorry, Auradio is not working on windows 😒")
    exit(0)

import curses
import json

from pathlib import Path
from time import sleep

import vlc

# os.environ["VLC_VERBOSE"] = str("-1")
class Auradio(object):
    def __init__(self) -> None:
        self.stdscr = curses.initscr()
        self.stdscr.keypad(1)
        self.volume = 40    
        
        curses.noecho()
        curses.curs_set(0)
        curses.mousemask(1)
        
        with open(Path("data.json"), 'r') as f:
            self.radio: list[dict] = json.load(f)
        
        self.switcher = {i:100 - (i-1) * 10 for i in range(1, 12)}
        self.title()

    def title(self):
        self.addstr(
        """                              
                            _ _     
  __ _ _   _ _ __ __ _  __| (_) ___   
 / _` | | | | '__/ _` |/ _` | |/ _ \  
| (_| | |_| | | | (_| | (_| | | (_) | 
 \__,_|\__,_|_|  \__,_|\__,_|_|\___/  

    """)
        self.stdscr.refresh()
        sleep(1)
        self.stdscr.clear()
        


    def playerset(self, url: str):
        vlc_instance = vlc.Instance("-q")
        self.player = vlc_instance.media_player_new()

        self.player.set_media(vlc_instance.media_new(url))
        self.player.audio_set_volume(self.volume)

        self.player.play()

    def addstr(self, *args):
        self.stdscr.addstr(*args)

    def volbar(self):
        self.addstr(0, 0, "┌")
        self.addstr(0, 2, "┐")
        self.addstr(11, 0, "└")
        self.addstr(11, 2, "┘")

        for i in range(1, 11):
            self.addstr(i, 0, "│")
            self.addstr(i, 2, "│")
            self.addstr(i, 1, "─")

        a = int(self.volume / 10)
        while a > 0:
            self.addstr(11 - a, 1, "▆")
            a = a - 1

    def setvol(self, num: int):
        return self.switcher.get(num)

    def setradio(self):
        now = -1

        while True:
            radx = 4
            rady = 1

            for w in self.radio:
                self.addstr(rady, radx, str(w["name"]))

                if int(w["number"]) == now:
                    self.addstr(rady, radx, str(w["name"]), curses.A_BOLD)

                if rady == 10:
                    rady = 0
                    radx = radx + 23
                    for i in range(1, 11):
                        self.addstr(i, radx - 2, "│")
                rady = rady + 1

            self.volbar()

            event = self.stdscr.getch()

            if event == curses.KEY_MOUSE:
                try:
                    click = curses.getmouse()
                except Exception:
                    break
                except KeyboardInterrupt:
                    self.close()

                if (
                    click[2] <= 10
                    and click[2] >= 1
                    and click[1] < (int((len(self.radio) / 10) * 23) + 2)
                ):

                    if click[1] < 3:
                        self.volume = self.setvol(click[2])
                        try:
                            self.player.audio_set_volume(self.volume)
                            continue
                        except Exception:
                            pass

                    # i dont know whats going on and
                    # at this point i'm too afraid to ask
                    now = int((click[1] - 2) / 23) * 10 + click[2] - 1

                    for w in self.radio:
                        if str(w["number"]) == str(now):
                            try:
                                self.player.stop()
                            except:
                                pass
                            self.playerset(str(w["url"]))
            self.stdscr.refresh()

    def close(self):
        self.player.close()
        raise SystemExit()

if __name__ == "__main__":
    auradio = Auradio()
    try:
        auradio.setradio()
    except Exception as e:
        print(e)
    finally:
        curses.endwin()
