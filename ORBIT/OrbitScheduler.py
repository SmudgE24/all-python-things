import json
import subprocess
import uuid
import webbrowser
from datetime import datetime
from pathlib import Path

import pygame

# ============================================================
# ORBIT SCHEDULER
# Built-in scheduler + Pygame UI in ONE file.
# ============================================================

BASE = Path(__file__).resolve().parent
TASK_FILE = BASE / "OrbitSchedulerTasks.json"


# ============================================================
# STORAGE
# ============================================================

def load_tasks():
    if not TASK_FILE.exists():
        return []
    try:
        data = json.loads(TASK_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def save_tasks(tasks):
    try:
        TASK_FILE.write_text(
            json.dumps(tasks, indent=4),
            encoding="utf-8"
        )
        return True
    except OSError:
        return False


# ============================================================
# ACTIONS
# ============================================================

def launch_app(app):
    try:
        subprocess.Popen(
            ["open", "-a", app],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True, f"Launching {app}"
    except OSError as e:
        return False, str(e)


def open_url(url):
    try:
        webbrowser.open(url)
        return True, f"Opening {url}"
    except Exception as e:
        return False, str(e)


def notify(title, message):
    title = str(title).replace('"', '\\"')
    message = str(message).replace('"', '\\"')
    script = f'display notification "{message}" with title "{title}"'
    try:
        subprocess.run(
            ["osascript", "-e", script],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )
        return True, "Notification sent."
    except OSError as e:
        return False, str(e)


# ============================================================
# SCHEDULER ENGINE
# ============================================================

class Scheduler:

    def __init__(self):
        self.tasks = load_tasks()
        self.last_second = ""

    def reload(self):
        self.tasks = load_tasks()

    def add(self, name, action, action_data, repeat, repeat_data):
        task = {
            "id": uuid.uuid4().hex,
            "name": name,
            "enabled": True,
            "action": action,
            "action_data": action_data,
            "repeat": repeat,
            "repeat_data": repeat_data,
            "last_run": None
        }
        self.tasks.append(task)
        save_tasks(self.tasks)

    def delete(self, task_id):
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        save_tasks(self.tasks)

    def toggle(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["enabled"] = not task["enabled"]
                save_tasks(self.tasks)
                return task["enabled"]
        return None

    def execute(self, task):
        a = task["action_data"]
        action = task["action"]

        if action == "app":
            ok, msg = launch_app(a.get("app", ""))
        elif action == "url":
            ok, msg = open_url(a.get("url", ""))
        elif action == "notification":
            ok, msg = notify(
                a.get("title", "Orbit"),
                a.get("message", "")
            )
        else:
            return False, "Unknown action."

        if ok:
            task["last_run"] = datetime.now().isoformat(timespec="seconds")
            save_tasks(self.tasks)

        return ok, msg

    def check(self):
        current = datetime.now()
        second = current.strftime("%Y-%m-%d %H:%M:%S")
        if second == self.last_second:
            return []
        self.last_second = second

        results = []

        for task in self.tasks:
            if not task.get("enabled", True):
                continue

            repeat = task["repeat"]
            data = task["repeat_data"]
            due = False

            if repeat == "daily":
                try:
                    due = (
                        current.hour == int(data["hour"])
                        and current.minute == int(data["minute"])
                        and (
                            not task.get("last_run")
                            or task["last_run"][:10] != current.strftime("%Y-%m-%d")
                        )
                    )
                except (KeyError, ValueError):
                    pass

            elif repeat == "once":
                try:
                    target = datetime.strptime(
                        data["datetime"],
                        "%Y-%m-%d %H:%M"
                    )
                    due = (
                        current >= target
                        and task.get("last_run") is None
                    )
                except (KeyError, ValueError):
                    pass

            elif repeat == "interval":
                try:
                    seconds = int(data["seconds"])
                    last = task.get("last_run")
                    if last:
                        old = datetime.fromisoformat(last)
                    else:
                        old = current
                    due = (current - old).total_seconds() >= seconds
                except (KeyError, ValueError):
                    pass

            if due:
                results.append(self.execute(task))

        return results


# ============================================================
# SIMPLE PYGAME UI
# ============================================================

class Box:

    def __init__(self, rect, hint):
        self.rect = pygame.Rect(rect)
        self.hint = hint
        self.text = ""
        self.active = False

    def event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            self.active = self.rect.collidepoint(e.pos)

        if e.type == pygame.KEYDOWN and self.active:
            if e.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif e.unicode.isprintable():
                self.text += e.unicode

    def draw(self, screen, font):
        pygame.draw.rect(screen, (255,255,255), self.rect, border_radius=8)
        pygame.draw.rect(
            screen,
            (60,120,245) if self.active else (215,215,220),
            self.rect,
            2,
            border_radius=8
        )
        text = self.text or self.hint
        colour = (30,30,35) if self.text else (110,110,115)
        screen.blit(font.render(text, True, colour),
                    (self.rect.x+10, self.rect.y+9))


class OrbitSchedulerUI:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 760), pygame.RESIZABLE)
        pygame.display.set_caption("OrbitScheduler")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("SF Pro Display", 19)
        self.small = pygame.font.SysFont("SF Pro Display", 15)
        self.title = pygame.font.SysFont("SF Pro Display", 34, bold=True)
        self.button_font = pygame.font.SysFont("SF Pro Display", 16, bold=True)

        self.scheduler = Scheduler()
        self.running = True
        self.selected = None
        self.scroll = 0
        self.action = "app"
        self.repeat = "daily"
        self.status = "Ready."

        self.name = Box((30, 145, 250, 42), "Task name")
        self.value = Box((295, 145, 310, 42), "App name / URL / message")
        self.when = Box((620, 145, 210, 42), "HH:MM")

        self.extra1 = Box((295, 195, 240, 42), "Notification title")
        self.extra2 = Box((550, 195, 280, 42), "Notification message")

    def button(self, rect, text, pos, colour=(60,120,245)):
        hover = rect.collidepoint(pos)
        c = tuple(min(255, x+12) for x in colour) if hover else colour
        pygame.draw.rect(self.screen, c, rect, border_radius=8)
        img = self.button_font.render(text, True, (255,255,255))
        self.screen.blit(img, img.get_rect(center=rect.center))

    def selected_task(self):
        for task in self.scheduler.tasks:
            if task["id"] == self.selected:
                return task
        return None

    def add_task(self):
        name = self.name.text.strip()
        value = self.value.text.strip()
        when = self.when.text.strip()

        if not name or not value:
            self.status = "Enter a task name and action."
            return

        if self.action == "app":
            action_data = {"app": value}
        elif self.action == "url":
            action_data = {"url": value}
        else:
            action_data = {
                "title": self.extra1.text.strip() or "Orbit",
                "message": self.extra2.text.strip() or value
            }

        if self.repeat == "daily":
            try:
                h, m = map(int, when.split(":"))
                if not (0 <= h <= 23 and 0 <= m <= 59):
                    raise ValueError
            except ValueError:
                self.status = "Daily time must be HH:MM."
                return
            repeat_data = {"hour": h, "minute": m}

        elif self.repeat == "once":
            try:
                datetime.strptime(when, "%Y-%m-%d %H:%M")
            except ValueError:
                self.status = "Once format: YYYY-MM-DD HH:MM."
                return
            repeat_data = {"datetime": when}

        else:
            try:
                seconds = max(1, int(when))
            except ValueError:
                self.status = "Interval must be seconds."
                return
            repeat_data = {"seconds": seconds}

        self.scheduler.add(
            name,
            self.action,
            action_data,
            self.repeat,
            repeat_data
        )

        for box in (self.name, self.value, self.when, self.extra1, self.extra2):
            box.text = ""

        self.status = f"Added: {name}"

    def action_name(self):
        return {
            "app": "Action: Launch App",
            "url": "Action: Open URL",
            "notification": "Action: Notification"
        }[self.action]

    def repeat_name(self):
        return {
            "daily": "Repeat: Daily",
            "once": "Schedule: Once",
            "interval": "Repeat: Interval"
        }[self.repeat]

    def cycle_action(self):
        vals = ["app", "url", "notification"]
        self.action = vals[(vals.index(self.action)+1) % len(vals)]

    def cycle_repeat(self):
        vals = ["daily", "once", "interval"]
        self.repeat = vals[(vals.index(self.repeat)+1) % len(vals)]

    def handle(self, e):
        for box in (self.name, self.value, self.when, self.extra1, self.extra2):
            box.event(e)

        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            self.running = False

        if e.type == pygame.MOUSEWHEEL:
            self.scroll = max(0, self.scroll - e.y * 45)

        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            self.click(e.pos)

    def click(self, pos):
        w, h = self.screen.get_size()

        action_button = pygame.Rect(30, 250, 260, 40)
        repeat_button = pygame.Rect(305, 250, 260, 40)
        add_button = pygame.Rect(w-210, 195, 180, 95)

        if action_button.collidepoint(pos):
            self.cycle_action()
            return

        if repeat_button.collidepoint(pos):
            self.cycle_repeat()
            return

        if add_button.collidepoint(pos):
            self.add_task()
            return

        # task controls
        toggle = pygame.Rect(w-390, h-58, 110, 40)
        run = pygame.Rect(w-270, h-58, 110, 40)
        delete = pygame.Rect(w-150, h-58, 120, 40)

        if toggle.collidepoint(pos) and self.selected:
            state = self.scheduler.toggle(self.selected)
            self.status = "Enabled." if state else "Disabled."
            return

        if run.collidepoint(pos) and self.selected:
            task = self.selected_task()
            if task:
                _, self.status = self.scheduler.execute(task)
            return

        if delete.collidepoint(pos) and self.selected:
            self.scheduler.delete(self.selected)
            self.selected = None
            self.status = "Task deleted."
            return

        # task list
        list_top = 355 - self.scroll
        for i, task in enumerate(self.scheduler.tasks):
            rect = pygame.Rect(30, list_top + i*68, w-60, 56)
            if rect.collidepoint(pos):
                self.selected = task["id"]
                return

    def draw(self):
        self.screen.fill((245,245,247))
        w, h = self.screen.get_size()

        self.screen.blit(self.title.render("OrbitScheduler", True, (30,30,35)), (30, 20))
        self.screen.blit(
            self.small.render(
                "Automate Orbit actions on your Mac",
                True,
                (105,105,112)
            ),
            (30, 60)
        )

        self.screen.blit(
            self.small.render(
                datetime.now().strftime("%A, %d %B %Y  %H:%M:%S"),
                True,
                (105,105,112)
            ),
            (w-285, 35)
        )

        # top panel
        panel = pygame.Rect(20, 100, w-40, 225)
        pygame.draw.rect(self.screen, (255,255,255), panel, border_radius=14)
        pygame.draw.rect(self.screen, (215,215,220), panel, 1, border_radius=14)

        self.name.rect.topleft = (30, 145)
        self.value.rect.topleft = (295, 145)
        self.when.rect.topleft = (620, 145)

        for box in (self.name, self.value, self.when):
            box.draw(self.screen, self.font)

        # Only show notification inputs for notification action.
        if self.action == "notification":
            self.extra1.rect.topleft = (295, 195)
            self.extra2.rect.topleft = (550, 195)
            self.extra1.draw(self.screen, self.small)
            self.extra2.draw(self.screen, self.small)

        self.button(
            pygame.Rect(30, 250, 260, 40),
            self.action_name(),
            pygame.mouse.get_pos()
        )
        self.button(
            pygame.Rect(305, 250, 260, 40),
            self.repeat_name(),
            pygame.mouse.get_pos()
        )
        self.button(
            pygame.Rect(w-210, 195, 180, 95),
            "ADD TASK",
            pygame.mouse.get_pos(),
            (48,170,95)
        )

        hint = {
            "daily": "HH:MM",
            "once": "YYYY-MM-DD HH:MM",
            "interval": "seconds"
        }[self.repeat]

        self.screen.blit(
            self.small.render(
                f"Schedule value: {hint}",
                True,
                (105,105,112)
            ),
            (620, 255)
        )

        # task list
        list_panel = pygame.Rect(20, 340, w-40, h-430)
        pygame.draw.rect(self.screen, (255,255,255), list_panel, border_radius=14)
        pygame.draw.rect(self.screen, (215,215,220), list_panel, 1, border_radius=14)

        self.screen.blit(
            self.font.render("Scheduled Tasks", True, (30,30,35)),
            (30, 355)
        )

        old_clip = self.screen.get_clip()
        self.screen.set_clip(list_panel)

        top = 395 - self.scroll

        for i, task in enumerate(self.scheduler.tasks):
            rect = pygame.Rect(30, top+i*68, w-60, 56)
            selected = task["id"] == self.selected

            colour = (60,120,245) if selected else (238,238,242)
            text_colour = (255,255,255) if selected else (30,30,35)
            secondary = (230,235,255) if selected else (105,105,112)

            pygame.draw.rect(self.screen, colour, rect, border_radius=9)

            self.screen.blit(
                self.font.render(task["name"], True, text_colour),
                (rect.x+12, rect.y+7)
            )

            if task["repeat"] == "daily":
                sched = f'Daily {task["repeat_data"]["hour"]:02d}:{task["repeat_data"]["minute"]:02d}'
            elif task["repeat"] == "once":
                sched = task["repeat_data"]["datetime"]
            else:
                sched = f'Every {task["repeat_data"]["seconds"]}s'

            action = {
                "app": "Launch " + task["action_data"].get("app", ""),
                "url": "Open " + task["action_data"].get("url", ""),
                "notification": "Notification"
            }.get(task["action"], "Unknown")

            line = f"{action}  •  {sched}"
            self.screen.blit(
                self.small.render(line[:120], True, secondary),
                (rect.x+12, rect.y+32)
            )

            state = "ON" if task.get("enabled", True) else "OFF"
            self.screen.blit(
                self.small.render(state, True, text_colour),
                (rect.right-35, rect.y+19)
            )

        self.screen.set_clip(old_clip)

        # bottom controls
        self.button(
            pygame.Rect(w-390, h-58, 110, 40),
            "ON / OFF",
            pygame.mouse.get_pos()
        )
        self.button(
            pygame.Rect(w-270, h-58, 110, 40),
            "RUN NOW",
            pygame.mouse.get_pos(),
            (48,170,95)
        )
        self.button(
            pygame.Rect(w-150, h-58, 120, 40),
            "DELETE",
            pygame.mouse.get_pos(),
            (220,70,70)
        )

        self.screen.blit(
            self.small.render(self.status[:130], True, (105,105,112)),
            (30, h-25)
        )

        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                else:
                    self.handle(event)

            for result in self.scheduler.check():
                if result:
                    self.status = result[1]

            self.draw()
            self.clock.tick(30)

        pygame.quit()


def open_ui():
    OrbitSchedulerUI().run()
