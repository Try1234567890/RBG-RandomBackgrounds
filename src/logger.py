import tkinter, file
from enum import Enum
from tkinter import scrolledtext

debug_console = None


class DebugLevel(Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2


def debug(msg: str, level: DebugLevel = DebugLevel.INFO):
    if debug_console is None:
        return
    if not isinstance(debug_console, scrolledtext.ScrolledText):
        return
    if not file.get_debug_enable():
        return
    log(msg, level)


def log(msg: str, level: DebugLevel):
    debug_console.configure(state="normal")
    prefix = {
        DebugLevel.WARNING: "[WARNING] ",
        DebugLevel.ERROR: "[ERROR] ",
        DebugLevel.INFO: "[INFO] "
    }.get(level, "[INFO] ")
    debug_console.insert(tkinter.INSERT, prefix + msg + "\n")
    debug_console.configure(state="disabled")
    debug_console.see(tkinter.END)

