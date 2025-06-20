import threading, gui, image, RBG
from pystray import Icon, MenuItem as item, Menu


def create():
    icon = Icon(
        "RBG",
        image.get_icon(),
        "RandomBackGround",
        menu=Menu(
            item("Open", gui.schedule_create),
            item("Close", RBG.close)
        )
    )
    icon.run()

def show():
    threading.Thread(target=create).start()
