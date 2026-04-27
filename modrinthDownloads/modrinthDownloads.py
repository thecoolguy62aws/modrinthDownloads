from . import __version__
import curses
from curses.textpad import Textbox, rectangle
import requests
import threading
import os
import time

headers = {
    'User-Agent': 'thecoolguy62aws/modrinthDownloads',
}

def get_modrinth_user(scr):
    def validate_enter(ch):
            if ch == 10:
                return 7
            return ch
    sh, sw = scr.getmaxyx()
    h, w = 1, 40
    y, x = (sh - h) // 2, (sw - w) // 2

    win = curses.newwin(h, w, y, x)
    rectangle(scr, y-1, x-1, y+h, x+w)
    scr.refresh()

    box = Textbox(win)
    scr.addstr(y-2, x, "Which Modrinth user?")
    scr.refresh()
    box.edit(validate_enter)
    if requests.get(f"https://api.modrinth.com/v2/user/{box.gather().strip()}", headers=headers).status_code != 200:
        del box
        scr.clear()
        win = curses.newwin(h, w, y, x)
        rectangle(scr, y-1, x-1, y+h, x+w)
        scr.refresh()
        box = Textbox(win)
        scr.addstr(y-2, x, "User not found! Try again.")
        scr.refresh()
        box.edit(validate_enter)
    
    return box.gather().strip()

def print_bold_center(win, text):
    h, w = win.getmaxyx()

    y = h // 2
    x = (w // 2) - (len(text) // 2)

    win.addstr(y, x, text, curses.A_BOLD)
    win.refresh()
    
def print_center_one_up(win, text):
    h, w = win.getmaxyx()

    y = (h // 2) - 1
    x = (w // 2) - (len(text) // 2)

    win.addstr(y, x, text)
    win.refresh()
    
def print_center_top(win, text):
    h, w = win.getmaxyx()

    y = 0
    x = (w // 2) - (len(text) // 2)

    win.addstr(y, x, text)
    win.refresh()

def quit_thread_task(scr):
    height, width = scr.getmaxyx()
    message = "Press Q to quit"
    message_y = height - 1
    message_x = width - len(message)
    while True:
        try:
            scr.addstr(message_y, message_x, message)
        except curses.error:
            pass
        scr.refresh()
        if scr.getch() == ord('q'):
            curses.endwin()
            os._exit(0)

def main(stdscr):
    stdscr.nodelay(True)
    stdscr.clear()
    
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    stdscr.bkgd(' ', curses.color_pair(1))
    stdscr.refresh()
    
    username = get_modrinth_user(stdscr)
    stdscr.clear()
    stdscr.refresh()
    
    quit_thread = threading.Thread(target=quit_thread_task, args=(stdscr,), daemon=True)
    quit_thread.start()
    
    while True:
        response = requests.get(f"https://api.modrinth.com/v2/user/{username}/projects", headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            
            downloads = 0
            for item in response_data:
                downloads += item["downloads"]

            print_center_top(stdscr, f"Viewing: {username}")
            print_center_one_up(stdscr, f"Live Downloads:")
            print_bold_center(stdscr, f"{str(downloads)}")
            stdscr.refresh()
        time.sleep(10)
