
import tkinter as tk
from tkinter import simpledialog, messagebox
import subprocess
import json
import os
import sys
import math
from datetime import datetime


def get_script_dir():
    """Dynamically finds the true folder directory of the running script."""
    try:
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.realpath(sys.modules['__main__'].__file__ or __file__))
    except Exception:
        return os.getcwd()


def load_custom_commands():
    config_path = os.path.join(get_script_dir(), "commands.json")

    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except Exception:
            return {}

    return {}


def get_current_time():
    """Returns the current date and time for the terminal output."""
    return datetime.now().strftime("%A, %d %B %Y | %H:%M:%S")


def launch_sentinel():
    """Launches Sentinel from the same directory as this terminal."""
    script_dir = get_script_dir()

    possible_names = [
        "Sentinel.py",
        "sentinel.py",
        "ORBIT.py",
        "orbit.py",
        "SystemMonitor.py",
        "system_monitor.py"
    ]

    sentinel_path = None

    for filename in possible_names:
        possible_path = os.path.join(script_dir, filename)
        if os.path.isfile(possible_path):
            sentinel_path = possible_path
            break

    # Also allow names such as Sentinel_Main.py.
    if sentinel_path is None:
        try:
            for filename in os.listdir(script_dir):
                lowered = filename.lower()
                if lowered.endswith(".py") and (
                    "sentinel" in lowered or "orbit" in lowered
                ):
                    sentinel_path = os.path.join(script_dir, filename)
                    break
        except OSError:
            pass

    if sentinel_path is None:
        raise FileNotFoundError(
            "Could not find Sentinel.py in the terminal's directory."
        )

    subprocess.Popen(
        [sys.executable, sentinel_path],
        cwd=script_dir
    )

    return os.path.basename(sentinel_path)


def evaluate_math(expression):
    """Evaluates mathematical expressions."""
    try:
        expr = expression.replace("^", "**")
        expr = expr.replace("√", "math.sqrt")

        safe_dict = {
            "math": math,
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "pi": math.pi,
            "e": math.e
        }

        result = eval(expr, {"__builtins__": None}, safe_dict)

        if isinstance(result, float):
            if result.is_integer():
                return str(int(result))
            return f"{result:.4f}"

        return str(result)

    except Exception:
        return "[MATH ERROR] Invalid expression."


def main():

    root = tk.Tk()
    root.withdraw()

    # 1. System Config Dialogs

    header = simpledialog.askstring(
        "System Config",
        "Enter System Banner Header:",
        parent=root
    )

    if not header:
        root.destroy()
        return

    description = simpledialog.askstring(
        "System Config",
        "Enter System Description:",
        parent=root
    )

    if not description:
        root.destroy()
        return

    frequency_str = simpledialog.askstring(
        "System Config",
        "How often to flash? (seconds):",
        parent=root
    )

    if not frequency_str:
        root.destroy()
        return

    try:
        frequency = int(frequency_str) * 1000

        if frequency < 1000:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter a valid time of at least 1 second."
        )
        root.destroy()
        return

    # 2. Window Layout Setup

    shell = tk.Toplevel(root)
    shell.title("Custom OS Shell")
    shell.resizable(True, True)
    shell.attributes("-topmost", True)

    screen_width = shell.winfo_screenwidth()
    shell.geometry(f"{screen_width}x40+0+0")

    bg_normal = "#1E1E24"
    bg_flash = "#ff00d4"         #"#C0392B"

    shell.configure(bg=bg_normal)

    # 3. Grid-Based Columns

    shell.grid_columnconfigure(0, weight=0)
    shell.grid_columnconfigure(1, weight=0)
    shell.grid_columnconfigure(2, weight=1)
    shell.grid_columnconfigure(3, weight=2)

    shell.grid_rowconfigure(0, weight=1)

    lbl_header = tk.Label(
        shell,
        text=f" {header.upper()} |",
        font=("Courier New", 11, "bold"),
        fg="#3498DB",
        bg=bg_normal
    )

    lbl_header.grid(row=0, column=0, padx=(10, 5), sticky="w")

    lbl_desc = tk.Label(
        shell,
        text=f"({description}) ",
        font=("Helvetica", 10, "italic"),
        fg="#A6ACAF",
        bg=bg_normal
    )

    lbl_desc.grid(row=0, column=1, padx=5, sticky="w")

    initial_status = "[READY] Engine Active. Use: calc <expr> | time | launch sentinel"

    lbl_status = tk.Label(
        shell,
        text=initial_status,
        font=("Courier New", 10),
        fg="#00FF00",
        bg="#111116",
        padx=10,
        relief=tk.FLAT
    )

    lbl_status.grid(row=0, column=2, padx=5, sticky="nswe")

    flash_enabled = True
    is_flashing = False
    flash_timer_id = None
    current_frequency = frequency

    cmd_frame = tk.Frame(shell, bg=bg_normal)
    cmd_frame.grid(row=0, column=3, padx=(5, 15), sticky="ew")

    lbl_prompt = tk.Label(
        cmd_frame,
        text="cmd:~$ ",
        font=("Courier New", 10, "bold"),
        fg="#3498DB",
        bg=bg_normal
    )

    lbl_prompt.pack(side=tk.LEFT)

    # ACTUAL COMMAND INPUT

    cmd_input = tk.Entry(
        cmd_frame,
        font=("Courier New", 10),
        bg="#111116",
        fg="#FFFFFF",
        insertbackground="white",
        relief=tk.FLAT
    )

    cmd_input.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def set_colours(background, header_colour, desc_colour):

        shell.configure(bg=background)

        lbl_header.configure(
            bg=background,
            fg=header_colour
        )

        lbl_desc.configure(
            bg=background,
            fg=desc_colour
        )

        cmd_frame.configure(bg=background)

        lbl_prompt.configure(
            bg=background,
            fg=header_colour
        )

    def snap_to_top_and_flash():

        nonlocal is_flashing, flash_timer_id

        if not flash_enabled:
            is_flashing = False
            set_colours(bg_normal, "#3498DB", "#A6ACAF")
            flash_timer_id = None
            return

        if not is_flashing:

            current_width = shell.winfo_width()
            current_height = shell.winfo_height()

            shell.geometry(
                f"{current_width}x{current_height}+0+0"
            )

            set_colours(bg_flash, "#FFFFFF", "#FFFFFF")

            is_flashing = True

            flash_timer_id = shell.after(
                800,
                snap_to_top_and_flash
            )

        else:

            set_colours(bg_normal, "#3498DB", "#A6ACAF")

            is_flashing = False

            flash_timer_id = shell.after(
                current_frequency,
                snap_to_top_and_flash
            )

    flash_timer_id = shell.after(
        current_frequency,
        snap_to_top_and_flash
    )

    # 4. Command Input Handler Engine

    def handle_command(event=None):

        nonlocal flash_enabled
        nonlocal current_frequency
        nonlocal flash_timer_id
        nonlocal is_flashing

        cmd_text = cmd_input.get().strip()

        if not cmd_text:
            return

        cmd_input.delete(0, tk.END)

        cmd_lower = cmd_text.lower()

        custom_apps = load_custom_commands()

        if cmd_lower == "flash":

            flash_enabled = not flash_enabled

            if flash_enabled:

                lbl_status.config(
                    text="[SYSTEM] Flash loop RESUMED.",
                    fg="#00FF00"
                )

                if flash_timer_id:
                    shell.after_cancel(flash_timer_id)

                is_flashing = False
                set_colours(bg_normal, "#3498DB", "#A6ACAF")

                flash_timer_id = shell.after(
                    current_frequency,
                    snap_to_top_and_flash
                )

            else:

                if flash_timer_id:
                    shell.after_cancel(flash_timer_id)

                flash_timer_id = None
                is_flashing = False

                set_colours(bg_normal, "#3498DB", "#A6ACAF")

                lbl_status.config(
                    text="[SYSTEM] Flash loop PAUSED.",
                    fg="#E74C3C"
                )

        elif cmd_lower == "flash stop":

            flash_enabled = False

            if flash_timer_id:
                shell.after_cancel(flash_timer_id)

            flash_timer_id = None
            is_flashing = False

            set_colours(bg_normal, "#3498DB", "#A6ACAF")

            lbl_status.config(
                text="[SYSTEM] Flash loop PAUSED.",
                fg="#E74C3C"
            )

        elif cmd_lower == "flash start":

            if not flash_enabled:

                flash_enabled = True

                lbl_status.config(
                    text="[SYSTEM] Flash loop RESUMED.",
                    fg="#00FF00"
                )

                if flash_timer_id:
                    shell.after_cancel(flash_timer_id)

                is_flashing = False
                set_colours(bg_normal, "#3498DB", "#A6ACAF")

                flash_timer_id = shell.after(
                    current_frequency,
                    snap_to_top_and_flash
                )

            else:

                lbl_status.config(
                    text="[SYSTEM] Flash loop already running.",
                    fg="#00FF00"
                )

        elif cmd_lower.startswith("flash add "):

            try:

                seconds_to_add = int(
                    cmd_lower.replace("flash add ", "").strip()
                )

                new_freq = current_frequency + (seconds_to_add * 1000)

                if new_freq < 1000:

                    lbl_status.config(
                        text="[ERROR] Min frequency is 1s.",
                        fg="#E74C3C"
                    )

                else:

                    current_frequency = new_freq

                    lbl_status.config(
                        text=f"[INTERVAL] Loop timing: {current_frequency // 1000}s",
                        fg="#3498DB"
                    )

                    if flash_enabled:

                        if flash_timer_id:
                            shell.after_cancel(flash_timer_id)

                        is_flashing = False
                        set_colours(bg_normal, "#3498DB", "#A6ACAF")

                        flash_timer_id = shell.after(
                            current_frequency,
                            snap_to_top_and_flash
                        )

            except ValueError:

                lbl_status.config(
                    text="[ERROR] Invalid format.",
                    fg="#E74C3C"
                )

        elif cmd_lower.startswith("kill "):

            app_key = cmd_lower.replace("kill ", "").strip()

            if app_key in custom_apps:

                target = custom_apps[app_key]

                if target.startswith("http"):

                    lbl_status.config(
                        text=f"[WARN] Cannot kill URL targets: '{app_key}'",
                        fg="#E67E22"
                    )

                else:

                    try:

                        result = subprocess.run(
                            ["killall", target],
                            capture_output=True,
                            text=True
                        )

                        if result.returncode == 0:

                            lbl_status.config(
                                text=f"[SYSTEM] Terminated '{target}'.",
                                fg="#00FF00"
                            )

                        else:

                            lbl_status.config(
                                text=f"[ERROR] Process '{target}' not running.",
                                fg="#E74C3C"
                            )

                    except Exception:

                        lbl_status.config(
                            text=f"[ERROR] Could not terminate '{target}'.",
                            fg="#E74C3C"
                        )

            else:

                lbl_status.config(
                    text=f"[ERROR] Key '{app_key}' missing from json.",
                    fg="#E74C3C"
                )

        elif cmd_lower == "time":

            lbl_status.config(
                text=f"[TIME] {get_current_time()}",
                fg="#3498DB"
            )

        elif cmd_lower in ("sentinel", "launch sentinel"):

            try:
                launched_name = launch_sentinel()
                lbl_status.config(
                    text=f"[EXEC] Sentinel launched: {launched_name}",
                    fg="#00FF00"
                )
            except Exception as error:
                lbl_status.config(
                    text=f"[ERROR] Sentinel launch failed: {error}",
                    fg="#E74C3C"
                )

        elif cmd_lower.startswith("calculate ") or cmd_lower.startswith("calc "):

            if cmd_lower.startswith("calculate "):
                raw_expr = cmd_text[10:]
            else:
                raw_expr = cmd_text[5:]

            math_output = evaluate_math(raw_expr.strip())

            lbl_status.config(
                text=f"[RESULT] {math_output}",
                fg="#3498DB"
            )

        elif cmd_lower in custom_apps or cmd_lower.startswith("launch "):

            if cmd_lower.startswith("launch "):
                app_key = cmd_lower[7:].strip()
            else:
                app_key = cmd_lower

            if app_key in custom_apps:

                target = custom_apps[app_key]

                try:

                    lbl_status.config(
                        text=f"[EXEC] Running target '{app_key}'...",
                        fg="#00FF00"
                    )

                    if target.startswith("http"):
                        subprocess.Popen(["open", target])
                    else:
                        subprocess.Popen(["open", "-a", target])

                except Exception:

                    lbl_status.config(
                        text=f"[ERROR] Launch failed for '{target}'",
                        fg="#E74C3C"
                    )

            else:

                lbl_status.config(
                    text=f"[ERROR] Key '{app_key}' missing from json.",
                    fg="#E74C3C"
                )

        else:

            lbl_status.config(
                text=f"[ERROR] Unknown command: {cmd_text}",
                fg="#E74C3C"
            )

    # ENTER KEY

    cmd_input.bind("<Return>", handle_command)

    # CLOSE WINDOW CLEANLY

    def close_window():

        if flash_timer_id:
            shell.after_cancel(flash_timer_id)

        root.destroy()

    shell.protocol("WM_DELETE_WINDOW", close_window)

    cmd_input.focus_set()

    root.mainloop()


if __name__ == "__main__":
    main()
