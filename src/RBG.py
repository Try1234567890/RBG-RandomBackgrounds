import ctypes
import file
import image
import logger
import os
import psutil
import random
import subprocess
import time
import tray_icon as it
import datetime
from pathlib import Path

start_up_folder = os.getenv('APPDATA') + os.sep + r'Microsoft\Windows\Start Menu\Programs\Startup'
backgrounds = []

def load_backgrounds():
    bgs_path = file.get_bgs_path().replace("[current_dir]", os.getcwd()).replace("[date]", str(datetime.datetime.now()).replace(":", "_"))
    if not os.path.isdir(bgs_path):
        return
    for filename in os.listdir(bgs_path):
        full_path = os.path.join(bgs_path, filename)
        if image.is_image(full_path):
            backgrounds.append(full_path)


def change_bg():
    index = random.randint(0, backgrounds.__len__() - 1)
    path = backgrounds[index]
    logger.debug(f"Selected Background: {path} ({index})")
    if image.is_image(path):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
    return path


def already_in_start_up():
    exe = file.get_exe().replace(".exe", "")
    link = os.path.join(start_up_folder, Path(exe).stem + ".lnk")
    return os.path.isfile(link)


def delete_to_start_up():
    exe = file.get_exe().replace(".exe", "")
    link = os.path.join(start_up_folder, Path(exe).stem + ".lnk")
    if os.path.isfile(link):
        os.remove(link)
    else:
        logger.debug(f"Unable to delete link to start-up apps. {file} not exists or is not a file.",
                     logger.DebugLevel.WARNING)


def add_to_start_up(exe):
    link = os.path.join(start_up_folder, Path(exe).stem + ".lnk")
    ps_cmd = f"$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('{link}'); $Shortcut.TargetPath = '{exe}'; $Shortcut.Save();"
    try:
        subprocess.run(
            ["powershell", "-Command", ps_cmd],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        logger.debug(f"""
            Error while creating link to start-up apps. You can do it manually: \n
              - Create a link of RBG exe;\n
              - Copy the link created;\n
              - Press WIN + R;\n
              - Write: \"shell:startup\";\n
              - Paste the link inside the folder.\n
            Error: {e.stderr.strip()}""",
            logger.DebugLevel.WARNING
        )


def close():
    file.save_config()
    if file.get_save_logs_on_quit():
        file.save_logs()
    name = file.get_exe_name()
    logger.debug(f"Searched process name: {name}")
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'].lower() == name.lower():
                logger.debug(f"Killing {proc.info['name']} with PID {proc.info['pid']}")
                proc.terminate()
                proc.wait(timeout=5)
                logger.debug(f"Process {proc.info['pid']} killed.")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            logger.debug(f"""
                         Error while terminating process. You can do it manually:\n
                            - Press CTRL + SHIFT + ESC.\n
                            - In search bar on top write: \"{name}\"\n
                            - Right click on the result that as the same icon as RBG\n
                            - Click \"End task\"\n
                         Error: {e}""", logger.DebugLevel.ERROR)

def start():
    file.load_config()
    load_backgrounds()
    if backgrounds.__len__() == 0:
        logger.debug("No backgrounds found. Make sure \"BGsPath\" parameter inside the config is correct.",
                     logger.DebugLevel.WARNING)
        return
    if file.get_run_on_start() and not already_in_start_up():
        add_to_start_up(file.get_exe())
    elif not file.get_run_on_start() and already_in_start_up():
        delete_to_start_up()
    it.show()
    while True:
        change_bg()
        delay = file.get_change_every()
        logger.debug(f"Wait {delay} seconds.")
        time.sleep(delay)


if __name__ == '__main__':
    start()
