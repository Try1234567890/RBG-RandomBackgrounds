import os
import tkinter as tk, threading, image, logger, RBG, file, subprocess
from tkinter import scrolledtext, Spinbox, Frame

root = None


def schedule_create():
    if root is None:
        threading.Thread(target=create).start()
    else:
        create()


def create():
    global root
    if root and root.winfo_exists():
        root.deiconify()
        root.lift()
        return
    RBG.load_backgrounds()
    root = tk.Tk()
    root.title("🎨 RBG - RandomBackGround")
    root.iconbitmap(image.get_icon_path())
    root.geometry("675x350")
    root.resizable(False, False)
    root.configure(bg="#2c3e50")
    root.protocol("WM_DELETE_WINDOW", lambda: root.withdraw())
    font_small = ("Segoe UI", 8)

    header_frame = Frame(root, bg="#2c3e50", height=35)
    header_frame.pack(fill="x", padx=0, pady=0)
    header_frame.pack_propagate(False)

    title_label = tk.Label(header_frame, text="🎨 RBG Settings", font=("Segoe UI", 12, "bold"),
                           bg="#2c3e50", fg="#ecf0f1")
    title_label.pack(pady=8)

    main_frame = Frame(root, bg="#34495e")
    main_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    left_column = Frame(main_frame, bg="#34495e")
    left_column.pack(side="left", fill="both", expand=True, padx=(0, 4))

    right_column = Frame(main_frame, bg="#34495e")
    right_column.pack(side="right", fill="both", expand=True, padx=(4, 0))
    settings_frame = create_section_frame(left_column, "⚙️ Settings")
    create_debug(settings_frame, font_small)
    create_run_on_start(settings_frame, font_small)
    create_save_logs_on_quit(settings_frame, font_small)

    paths_frame = create_section_frame(left_column, "📁 Paths")
    create_bgs_path(paths_frame, font_small)
    create_logs_file(paths_frame, font_small)
    timing_frame = create_section_frame(right_column, "⏰ Timing")
    create_change_every(timing_frame, font_small)

    actions_frame = create_section_frame(right_column, "🎮 Actions")
    create_change_bg_button(actions_frame)
    create_close(actions_frame)
    create_reload(actions_frame)
    console_frame = create_section_frame(main_frame, "🔍 Debug Console")
    create_debug_console(console_frame)
    create_save_logs_buttons(console_frame)

    root.mainloop()

def create_section_frame(parent, title):
    section_frame = Frame(parent, bg="#34495e", relief="raised", bd=1)
    section_frame.pack(fill="x", padx=2, pady=4)
    title_frame = Frame(section_frame, bg="#3498db", height=25)
    title_frame.pack(fill="x")
    title_frame.pack_propagate(False)

    title_label = tk.Label(title_frame, text=title, font=("Segoe UI", 9, "bold"),
                           bg="#3498db", fg="white")
    title_label.pack(pady=4)
    content_frame = Frame(section_frame, bg="#34495e")
    content_frame.pack(fill="both", expand=True, padx=8, pady=6)

    return content_frame


def create_debug(parent, font):
    var = tk.BooleanVar()
    var.set(file.get_debug_enable())
    chk = tk.Checkbutton(parent, text="Debug Mode", variable=var, font=font,
                         bg="#34495e", fg="#ecf0f1", selectcolor="#2c3e50",
                         activebackground="#34495e", activeforeground="#ecf0f1",
                         command=lambda: file.set_debug_enable(var.get()))
    chk.pack(anchor="w", pady=1)


def create_save_logs_on_quit(parent, font):
    var = tk.BooleanVar()
    var.set(file.get_save_logs_on_quit())
    chk = tk.Checkbutton(parent, text="Save Logs On Quit", variable=var, font=font,
                         bg="#34495e", fg="#ecf0f1", selectcolor="#2c3e50",
                         activebackground="#34495e", activeforeground="#ecf0f1",
                         command=lambda: file.set_save_logs_on_quit(var.get()))
    chk.pack(anchor="w", pady=1)


def create_run_on_start(parent, font):
    var = tk.BooleanVar()
    var.set(file.get_run_on_start())
    chk = tk.Checkbutton(parent, text="Run on Start", variable=var, font=font,
                         bg="#34495e", fg="#ecf0f1", selectcolor="#2c3e50",
                         activebackground="#34495e", activeforeground="#ecf0f1",
                         command=lambda: file.set_run_on_start(var.get()))
    chk.pack(anchor="w", pady=1)


def create_logs_file(parent, font):
    var = tk.StringVar()
    var.set(file.get_logs_file())

    def on_path_change(*args):
        file.set_logs_file(var.get())

    var.trace_add("write", on_path_change)

    lbl = tk.Label(parent, text="📄 Logs File:", font=font, bg="#34495e", fg="#ecf0f1")
    lbl.pack(anchor="w", pady=(0, 2))

    entry = tk.Entry(parent, textvariable=var, font=font, bg="#ecf0f1", fg="#2c3e50",
                     relief="flat", bd=3, width=25)
    entry.pack(fill="x", ipady=2)


def create_bgs_path(parent, font):
    var = tk.StringVar()
    var.set(file.get_bgs_path())

    def on_path_change(*args):
        file.set_bgs_path(var.get())

    var.trace_add("write", on_path_change)

    lbl = tk.Label(parent, text="🖼️ BGs Path:", font=font, bg="#34495e", fg="#ecf0f1")
    lbl.pack(anchor="w", pady=(0, 2))

    entry = tk.Entry(parent, textvariable=var, font=font, bg="#ecf0f1", fg="#2c3e50",
                     relief="flat", bd=3, width=25)
    entry.pack(fill="x", ipady=2)


def create_change_every(parent, font):
    var = tk.StringVar()
    var.set(str(file.get_change_every()))

    def on_change(*args):
        try:
            value = int(var.get())
            if value > 0:
                file.set_change_every(value)
        except ValueError:
            if var.get() == "":
                return
            logger.debug("\"Change Every\" parameter cannot contains non-number chars. Setting default: 3600",
                         logger.DebugLevel.WARNING)
            var.set(str(3600))
            file.set_change_every(3600)

    var.trace_add("write", on_change)

    lbl = tk.Label(parent, text="⏱️ Change Every (sec):", font=font,
                   bg="#34495e", fg="#ecf0f1")
    lbl.pack(anchor="w", pady=(0, 2))

    spin = Spinbox(parent, from_=1, to=99999, textvariable=var, font=font, width=10,
                   bg="#ecf0f1", fg="#2c3e50", relief="flat", bd=3)
    spin.pack(anchor="w", ipady=2)


def create_change_bg_button(parent):
    btn = tk.Button(parent, text="🔄 Change BG", command=RBG.change_bg,
                    font=("Segoe UI", 9, "bold"), bg="#27ae60", fg="white",
                    relief="flat", bd=0, pady=8, cursor="hand2",
                    activebackground="#229954", activeforeground="white")
    btn.pack(fill="x", pady=2)

    def on_enter(e):
        btn.configure(bg="#229954")

    def on_leave(e):
        btn.configure(bg="#27ae60")

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)


def create_close(parent):
    def close():
        RBG.close()

    btn = tk.Button(parent, text="❌ Close App", command=close,
                    font=("Segoe UI", 9, "bold"), bg="#e74c3c", fg="white",
                    relief="flat", bd=0, pady=8, cursor="hand2",
                    activebackground="#c0392b", activeforeground="white")
    btn.pack(fill="x", pady=2)

    def on_enter(e):
        btn.configure(bg="#c0392b")

    def on_leave(e):
        btn.configure(bg="#e74c3c")

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)


def create_reload(parent):
    def reload_app():
        exe_dir = os.path.dirname(file.get_exe())
        exe_name = file.get_exe_name()
        command = f'powershell -Command "cd "{exe_dir}"; Start-Process ".\\{exe_name}""'
        subprocess.Popen(command, shell=True)
        RBG.close()

    btn = tk.Button(parent, text="🔁 Reload App", command=reload_app,
                    font=("Segoe UI", 9, "bold"), bg="#2980b9", fg="white",
                    relief="flat", bd=0, pady=8, cursor="hand2",
                    activebackground="#2471a3", activeforeground="white")
    btn.pack(fill="x", pady=(0, 2))

    def on_enter(e):
        btn.configure(bg="#2471a3")

    def on_leave(e):
        btn.configure(bg="#2980b9")

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)


def create_debug_console(parent):
    text_area = scrolledtext.ScrolledText(parent, width=70, height=12,
                                          font=("Consolas", 8), bg="#2c3e50", fg="#ecf0f1",
                                          relief="flat", bd=3, wrap=tk.WORD)
    text_area.pack(fill="both", expand=True, pady=2)
    text_area.configure(state='disabled')
    logger.debug_console = text_area


def create_save_logs_buttons(parent):
    buttons_frame = Frame(parent, bg="#34495e")
    buttons_frame.pack(fill="x", pady=(4, 2))

    btn_save = tk.Button(buttons_frame, text="💾 Save Logs", command=file.save_logs,
                         font=("Segoe UI", 9, "bold"), bg="#f39c12", fg="white",
                         relief="flat", bd=0, pady=6, cursor="hand2",
                         activebackground="#e67e22", activeforeground="white")
    btn_save.pack(side="left", fill="x", expand=True, padx=(0, 2))

    def on_enter_save(e):
        btn_save.configure(bg="#e67e22")

    def on_leave_save(e):
        btn_save.configure(bg="#f39c12")

    btn_save.bind("<Enter>", on_enter_save)
    btn_save.bind("<Leave>", on_leave_save)

    def save_logs_and_clear():
        file.save_logs()
        if logger.debug_console:
            logger.debug_console.configure(state='normal')
            logger.debug_console.delete(1.0, tk.END)
            logger.debug_console.configure(state='disabled')

    btn_save_clear = tk.Button(buttons_frame, text="💾🗑️ Save Logs And Clear", command=save_logs_and_clear,
                               font=("Segoe UI", 9, "bold"), bg="#9b59b6", fg="white",
                               relief="flat", bd=0, pady=6, cursor="hand2",
                               activebackground="#8e44ad", activeforeground="white")
    btn_save_clear.pack(side="right", fill="x", expand=True, padx=(2, 0))

    def on_enter_save_clear(e):
        btn_save_clear.configure(bg="#8e44ad")

    def on_leave_save_clear(e):
        btn_save_clear.configure(bg="#9b59b6")

    btn_save_clear.bind("<Enter>", on_enter_save_clear)
    btn_save_clear.bind("<Leave>", on_leave_save_clear)
