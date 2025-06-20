import json
import os
import datetime
import logger
import tkinter as tk

config_path = f"{os.curdir}\\configs"
config_file = f"{config_path}\\config.json"

config = {}


def save_logs():
    file_logs = get_logs_file().replace("[current_dir]", os.getcwd()).replace("[date]", str(datetime.datetime.now()).replace(":", "_"))
    directory = os.path.dirname(file_logs)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(file_logs, "w") as f:
        if logger.debug_console is None:
            return
        content = logger.debug_console.get('1.0', tk.END)
        if content.strip() != "":
            f.write(content)


def load_config():
    if not os.path.isfile(config_file):
        create_config()
    with open(config_file, "r") as file:
        global config
        config = json.loads(file.read())


def save_config():
    if not os.path.isfile(config_file):
        create_config()
    with open(config_file, "w") as file:
        json.dump(config, file)


def create_config():
    if not os.path.exists(config_path):
        os.makedirs(config_path)
    with open(config_file, "w") as file:
        content = {
            "ChangeEvery": 5,
            "BGsPath": "[current_dir]\\images\\",
            "RunOnStart": True,
            "Debug": {
                "Enable": False,
                "SaveLogsOnQuit": True,
                "LogsFile": "[current_dir]\\logs\\log-[date].txt"
            }
        }
        json.dump(content, file)


def get_change_every() -> int:
    return config["ChangeEvery"]


def get_bgs_path() -> str:
    return config["BGsPath"]

def get_run_on_start() -> bool:
    return config["RunOnStart"]


def get_debug_enable() -> bool:
    return config["Debug"]["Enable"]


def get_save_logs_on_quit() -> bool:
    return config["Debug"]["SaveLogsOnQuit"]


def get_logs_file() -> str:
    return config["Debug"]["LogsFile"]

def set_change_every(value: int):
    config["ChangeEvery"] = value


def set_bgs_path(value: str):
    config["BGsPath"] = value

def set_run_on_start(value: bool):
    config["RunOnStart"] = value

def set_debug_enable(value: bool):
    config["Debug"]["Enable"] = value

def set_save_logs_on_quit(value: bool):
    config["Debug"]["SaveLogsOnQuit"] = value

def set_logs_file(value: str):
    config["Debug"]["LogsFile"] = value

def get_exe_name():
    for file_name in os.listdir(os.getcwd()):
        if file_name.endswith(".exe"):
            return file_name
    return None


def get_exe():
    return os.getcwd() + os.sep + get_exe_name()
