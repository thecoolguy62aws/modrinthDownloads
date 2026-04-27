from .modrinthDownloads import main
import curses

def start():
    curses.wrapper(main)

if __name__ == "__main__":
    start()
