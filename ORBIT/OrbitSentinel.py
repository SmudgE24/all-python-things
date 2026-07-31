import pygame
import psutil
import cpuinfo
import platform
import subprocess
import plistlib
import threading
import time
import os
import socket
import shutil
from collections import deque
from datetime import datetime

# ============================================================
# ORBIT - FULL LIVE SYSTEM MONITOR
# ============================================================
# Controls
#   Mouse wheel / UP / DOWN : scroll
#   M                       : sort processes by RAM
#   C                       : sort processes by CPU
#   D                       : run diagnostics
#   R                       : refresh hardware / software info
#   ESC                     : quit
#
# This is deliberately written as one file so you can paste it
# directly into VS Code and run it.
# ============================================================


def ALL_POWERFULL():
    pygame.init()

    WIDTH, HEIGHT = 1120, 760
    FPS = 20
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("ORBIT - System Monitor")
    clock = pygame.time.Clock()

    # ------------------------------------------------------------
    # FONTS
    # ------------------------------------------------------------

    FONT = pygame.font.SysFont("Courier New", 16)
    SMALL = pygame.font.SysFont("Courier New", 13)
    TINY = pygame.font.SysFont("Courier New", 11)
    TITLE = pygame.font.SysFont("Courier New", 28, bold=True)
    BIG = pygame.font.SysFont("Courier New", 21, bold=True)

    # ------------------------------------------------------------
    # COLOURS
    # ------------------------------------------------------------

    BG = (9, 11, 15)
    PANEL = (16, 19, 25)
    PANEL2 = (20, 24, 31)
    WHITE = (235, 240, 245)
    MUTED = (130, 140, 153)
    GRID = (36, 43, 53)
    CYAN = (70, 215, 255)
    GREEN = (85, 225, 125)
    YELLOW = (245, 205, 75)
    ORANGE = (245, 145, 70)
    RED = (240, 85, 90)
    PURPLE = (175, 125, 245)

    # ------------------------------------------------------------
    # BASIC INFO
    # ------------------------------------------------------------

    CPU_NAME = cpuinfo.get_cpu_info().get("brand_raw", "Unknown CPU")
    OS_NAME = f"{platform.system()} {platform.release()}"
    ARCH = platform.machine()
    PYTHON_VERSION = platform.python_version()
    BOOT_TIME = psutil.boot_time()
    START_TIME = time.monotonic()

    # ------------------------------------------------------------
    # HISTORY
    # ------------------------------------------------------------

    cpu_history = deque(maxlen=600)
    ram_history = deque(maxlen=600)
    swap_history = deque(maxlen=600)
    power_history = deque(maxlen=600)
    download_history = deque(maxlen=600)
    upload_history = deque(maxlen=600)
    disk_read_history = deque(maxlen=600)
    disk_write_history = deque(maxlen=600)

    # ------------------------------------------------------------
    # EVENTS / ALERTS
    # ------------------------------------------------------------

    events = deque(maxlen=14)
    alerts = deque(maxlen=8)


    def add_event(message):
        timestamp = time.strftime("%H:%M:%S")
        if not events or events[-1][1] != message:
            events.append((timestamp, message))


    def add_alert(message):
        timestamp = time.strftime("%H:%M:%S")
        if not alerts or alerts[-1][1] != message:
            alerts.append((timestamp, message))
            add_event("ALERT: " + message)


    # ------------------------------------------------------------
    # POWER MONITOR
    # ------------------------------------------------------------

    power_lock = threading.Lock()
    power_watts = None
    power_source = "Unavailable"


    def read_battery_ioreg():
        try:
            result = subprocess.run(
                ["ioreg", "-r", "-n", "AppleSmartBattery", "-a"],
                capture_output=True,
                timeout=3,
            )
            if result.returncode != 0 or not result.stdout:
                return None
            data = plistlib.loads(result.stdout)
            if isinstance(data, list) and data:
                return data[0]
            if isinstance(data, dict):
                return data
        except Exception:
            pass
        return None


    def get_battery_power():
        data = read_battery_ioreg()
        if not data:
            return None

        current = data.get("Current")
        voltage = data.get("Voltage")

        if isinstance(current, (int, float)) and isinstance(voltage, (int, float)):
            watts = abs(float(current) * float(voltage)) / 1_000_000
            if 0 <= watts < 500:
                return watts
        return None


    def power_worker():
        nonlocal power_watts, power_source
        while True:
            value = get_battery_power()
            with power_lock:
                power_watts = value
                power_source = "Battery estimate" if value is not None else "Unavailable"
            time.sleep(2)


    threading.Thread(target=power_worker, daemon=True).start()

    # ------------------------------------------------------------
    # MAC HARDWARE HELPERS
    # ------------------------------------------------------------


    def run_command(command, timeout=4):
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return ""


    def get_temperature_text():
        # macOS does not expose a universal psutil temperature API on Apple Silicon.
        # Try powermetrics without sudo first; otherwise report unavailable.
        output = run_command(
            ["powermetrics", "--samplers", "thermal", "-n", "1"],
            timeout=5,
        )
        if output:
            lines = []
            for line in output.splitlines():
                lowered = line.lower()
                if "temperature" in lowered or "thermal" in lowered:
                    lines.append(line.strip())
            if lines:
                return " | ".join(lines[:2])[:100]
        return "Not exposed without additional macOS privileges"


    def get_fan_text():
        output = run_command(["powermetrics", "--samplers", "smc", "-n", "1"], timeout=5)
        if output:
            for line in output.splitlines():
                if "fan" in line.lower() or "rpm" in line.lower():
                    return line.strip()[:100]
        return "Not exposed"


    def get_battery_details():
        data = read_battery_ioreg() or {}
        battery = psutil.sensors_battery()

        percent = battery.percent if battery else None
        charging = battery.power_plugged if battery else False
        cycle = data.get("CycleCount")
        health = data.get("BatteryHealth") or data.get("HealthStatus")
        capacity = data.get("MaxCapacity")
        design = data.get("DesignCapacity")
        voltage = data.get("Voltage")

        return {
            "percent": percent,
            "charging": charging,
            "cycle": cycle,
            "health": health,
            "capacity": capacity,
            "design": design,
            "voltage": voltage,
        }


    def get_login_items():
        # Best-effort check of the user's LaunchAgents folder.
        folder = os.path.expanduser("~/Library/LaunchAgents")
        if not os.path.isdir(folder):
            return []
        try:
            return sorted(
                name for name in os.listdir(folder)
                if name.endswith(".plist")
            )[:30]
        except Exception:
            return []

    # ------------------------------------------------------------
    # GENERAL HELPERS
    # ------------------------------------------------------------


    def clamp(value, minimum, maximum):
        return max(minimum, min(maximum, value))


    def nice_bytes(value):
        value = float(value)
        for unit in ("B", "KB", "MB", "GB", "TB"):
            if value < 1024 or unit == "TB":
                return f"{value:.1f} {unit}"
            value /= 1024
        return f"{value:.1f} TB"


    def nice_speed(value):
        return nice_bytes(value) + "/s"


    def uptime_text():
        seconds = max(0, int(time.time() - BOOT_TIME))
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, _ = divmod(seconds, 60)
        if days:
            return f"{days}d {hours}h {minutes}m"
        return f"{hours}h {minutes}m"


    def text(surface, value, x, y, font=FONT, colour=WHITE):
        surface.blit(font.render(str(value), True, colour), (int(x), int(y)))


    def panel(surface, rect, title_text=None, colour=GRID):
        pygame.draw.rect(surface, PANEL, rect, border_radius=8)
        pygame.draw.rect(surface, colour, rect, width=1, border_radius=8)
        if title_text:
            text(surface, title_text, rect.x + 12, rect.y + 9, SMALL, CYAN)


    def bar(surface, x, y, width, height, value, maximum=100, colour=CYAN):
        value = clamp(value, 0, maximum)
        pygame.draw.rect(surface, GRID, (x, y, width, height), border_radius=4)
        fill = int(width * value / maximum) if maximum else 0
        if fill > 0:
            pygame.draw.rect(surface, colour, (x, y, fill, height), border_radius=4)


    def status_colour(value, warning=70, danger=90):
        if value >= danger:
            return RED
        if value >= warning:
            return YELLOW
        return GREEN


    def draw_graph(surface, rect, histories, labels, maxima, colours):
        pygame.draw.rect(surface, PANEL2, rect, border_radius=6)
        for i in range(5):
            yy = rect.y + int(rect.h * i / 4)
            pygame.draw.line(surface, GRID, (rect.x, yy), (rect.right, yy), 1)
        for i in range(7):
            xx = rect.x + int(rect.w * i / 6)
            pygame.draw.line(surface, GRID, (xx, rect.y), (xx, rect.bottom), 1)

        for history, maximum, colour in zip(histories, maxima, colours):
            if len(history) < 2:
                continue
            points = []
            for i, value in enumerate(history):
                xx = rect.x + int(i * (rect.w - 1) / max(1, len(history) - 1))
                yy = rect.bottom - int(clamp(value / maximum, 0, 1) * rect.h)
                points.append((xx, yy))
            pygame.draw.lines(surface, colour, False, points, 2)

        lx = rect.x + 6
        for label, colour in zip(labels, colours):
            text(surface, label, lx, rect.y + 6, TINY, colour)
            lx += 58

    # ------------------------------------------------------------
    # PROCESS DATA
    # ------------------------------------------------------------


    def get_processes():
        result = []
        for process in psutil.process_iter(
            ["pid", "name", "memory_percent", "cpu_percent", "status", "username", "num_threads"]
        ):
            try:
                info = process.info
                result.append({
                    "pid": info.get("pid", 0),
                    "name": info.get("name") or "Unknown",
                    "memory": info.get("memory_percent") or 0,
                    "cpu": info.get("cpu_percent") or 0,
                    "status": info.get("status") or "?",
                    "username": info.get("username") or "?",
                    "threads": info.get("num_threads") or 0,
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return result


    # ------------------------------------------------------------
    # STORAGE / NETWORK
    # ------------------------------------------------------------


    def get_drives():
        drives = []
        seen = set()
        for partition in psutil.disk_partitions(all=False):
            mount = partition.mountpoint
            if mount in seen:
                continue
            seen.add(mount)
            try:
                usage = psutil.disk_usage(mount)
                name = "Macintosh HD" if mount == "/" else mount.replace("/Volumes/", "")
                drives.append({
                    "name": name,
                    "mount": mount,
                    "percent": usage.percent,
                    "used": usage.used,
                    "free": usage.free,
                    "total": usage.total,
                    "fstype": partition.fstype,
                })
            except (PermissionError, OSError):
                pass
        return drives


    def get_ip():
        try:
            for address in psutil.net_if_addrs().values():
                for item in address:
                    if item.family == socket.AF_INET and not item.address.startswith("127."):
                        return item.address
        except Exception:
            pass
        return "Unavailable"


    def get_ping(host="1.1.1.1"):
        if shutil.which("ping") is None:
            return None
        try:
            result = subprocess.run(
                ["ping", "-c", "1", "-W", "1000", host],
                capture_output=True,
                text=True,
                timeout=2,
            )
            for line in result.stdout.splitlines():
                if "time=" in line:
                    part = line.split("time=")[-1].split()[0]
                    return float(part.replace("ms", ""))
        except Exception:
            pass
        return None


    def get_connections():
        try:
            return psutil.net_connections(kind="inet")
        except (psutil.AccessDenied, PermissionError):
            return []
        except Exception:
            return []

    # ------------------------------------------------------------
    # DIAGNOSTICS
    # ------------------------------------------------------------


    def run_diagnostics():
        checks = []

        checks.append(("CPU accessible", psutil.cpu_count() is not None))
        checks.append(("Memory accessible", psutil.virtual_memory().total > 0))
        checks.append(("Root disk accessible", os.path.exists("/")))
        checks.append(("Network interfaces found", len(psutil.net_if_addrs()) > 0))
        checks.append(("Process list accessible", len(psutil.pids()) > 0))
        checks.append(("Python executable", bool(sys_executable())))
        checks.append(("External storage scan", len(get_drives()) >= 1))

        ping = get_ping()
        checks.append(("Internet ping", ping is not None))

        return checks


    def sys_executable():
        return os.path.abspath(shutil.which("python") or "")

    # ------------------------------------------------------------
    # ORBIT PLUGIN STATUS
    # ------------------------------------------------------------


    def get_plugin_status():
        return [
            ("KERNEL", True),
            ("HARDWARE MONITOR", True),
            ("PROCESS MONITOR", True),
            ("NETWORK MONITOR", True),
            ("BATTERY MONITOR", True),
            ("STORAGE MONITOR", True),
            ("DIAGNOSTICS", True),
            ("HISTORY ENGINE", True),
            ("EVENT ENGINE", True),
        ]

    # ------------------------------------------------------------
    # STATE
    # ------------------------------------------------------------

    scroll = 0
    process_sort = "memory"
    processes_cache = []
    last_process_scan = 0
    last_ping = None
    last_ping_time = 0
    last_diagnostics = []
    last_diagnostic_time = 0
    last_warning_ram = 0
    last_warning_cpu = 0
    last_warning_disk = 0
    last_hardware_refresh = 0
    temperature_text = "Scanning..."
    fan_text = "Scanning..."
    login_items = []

    last_net = psutil.net_io_counters()
    last_net_time = time.monotonic()
    last_disk = psutil.disk_io_counters()
    last_disk_time = time.monotonic()

    # ------------------------------------------------------------
    # MAIN LOOP
    # ------------------------------------------------------------

    running = True

    while running:
        clock.tick(FPS)
        now = time.monotonic()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    scroll = max(0, scroll - 45)
                elif event.key == pygame.K_DOWN:
                    scroll += 45
                elif event.key == pygame.K_m:
                    process_sort = "memory"
                elif event.key == pygame.K_c:
                    process_sort = "cpu"
                elif event.key == pygame.K_d:
                    last_diagnostics = run_diagnostics()
                    last_diagnostic_time = now
                    add_event("Diagnostics completed")
                elif event.key == pygame.K_r:
                    last_hardware_refresh = 0
                    add_event("Hardware and software refresh requested")

            elif event.type == pygame.MOUSEWHEEL:
                scroll -= event.y * 45

        width, height = screen.get_size()

        # --------------------------------------------------------
        # LIVE DATA
        # --------------------------------------------------------

        cpu = psutil.cpu_percent()
        cpu_per_core = psutil.cpu_percent(percpu=True)
        ram = psutil.virtual_memory()
        swap = psutil.swap_memory()
        disk = psutil.disk_usage("/")
        battery_info = get_battery_details()
        battery_percent = battery_info["percent"]
        charging = battery_info["charging"]
        process_count = len(psutil.pids())

        net = psutil.net_io_counters()
        net_dt = max(now - last_net_time, 0.001)
        download_speed = max(0, (net.bytes_recv - last_net.bytes_recv) / net_dt)
        upload_speed = max(0, (net.bytes_sent - last_net.bytes_sent) / net_dt)
        last_net = net
        last_net_time = now

        disk_io = psutil.disk_io_counters()
        disk_dt = max(now - last_disk_time, 0.001)
        read_speed = 0
        write_speed = 0
        if disk_io and last_disk:
            read_speed = max(0, (disk_io.read_bytes - last_disk.read_bytes) / disk_dt)
            write_speed = max(0, (disk_io.write_bytes - last_disk.write_bytes) / disk_dt)
        last_disk = disk_io
        last_disk_time = now

        with power_lock:
            current_power = power_watts
            current_power_source = power_source

        cpu_history.append(cpu)
        ram_history.append(ram.percent)
        swap_history.append(swap.percent)
        power_history.append(current_power or 0)
        download_history.append(download_speed)
        upload_history.append(upload_speed)
        disk_read_history.append(read_speed)
        disk_write_history.append(write_speed)

        if now - last_process_scan > 2:
            processes_cache = get_processes()
            last_process_scan = now

        if now - last_ping_time > 10:
            last_ping = get_ping()
            last_ping_time = now

        if now - last_hardware_refresh > 20:
            temperature_text = get_temperature_text()
            fan_text = get_fan_text()
            login_items = get_login_items()
            last_hardware_refresh = now

        # --------------------------------------------------------
        # WARNINGS
        # --------------------------------------------------------

        if ram.percent >= 85 and now - last_warning_ram > 20:
            add_alert(f"RAM usage is {ram.percent:.1f}%")
            last_warning_ram = now

        if cpu >= 90 and now - last_warning_cpu > 20:
            add_alert(f"CPU usage is {cpu:.1f}%")
            last_warning_cpu = now

        if disk.percent >= 90 and now - last_warning_disk > 20:
            add_alert(f"Root disk is {disk.percent:.1f}% full")
            last_warning_disk = now

        if battery_percent is not None and battery_percent <= 15 and not charging:
            add_alert(f"Battery low: {battery_percent:.0f}%")

        # --------------------------------------------------------
        # HEALTH SCORE
        # --------------------------------------------------------

        score = 100
        score -= max(0, cpu - 60) * 0.55
        score -= max(0, ram.percent - 70) * 0.75
        score -= max(0, disk.percent - 85) * 0.65
        score -= max(0, swap.percent - 60) * 0.25
        if battery_percent is not None and battery_percent < 15 and not charging:
            score -= 8
        score = int(clamp(score, 0, 100))

        if score >= 80:
            health_text, health_colour = "GOOD", GREEN
        elif score >= 55:
            health_text, health_colour = "WATCH", YELLOW
        else:
            health_text, health_colour = "WARNING", RED

        # --------------------------------------------------------
        # SCREEN SURFACE
        # --------------------------------------------------------

        screen.fill(BG)

        # We draw the dashboard on a virtual tall canvas.
        content_width = width - 30
        content_height = 2240

        canvas = pygame.Surface((content_width, content_height))
        canvas.fill(BG)

        # --------------------------------------------------------
        # HEADER
        # --------------------------------------------------------

        text(canvas, "ORBIT", 15, 12, TITLE, CYAN)
        text(canvas, "FULL SYSTEM CONTROL CENTRE", 112, 17, BIG, WHITE)
        text(canvas, time.strftime("%H:%M:%S"), content_width - 95, 18, SMALL, MUTED)

        # --------------------------------------------------------
        # TOP CARDS
        # --------------------------------------------------------

        card_y = 60
        gap = 9
        card_w = (content_width - 4 * gap) // 5
        card_h = 105

        cards = [
            ("CPU", f"{cpu:.1f}%", cpu, CYAN),
            ("RAM", f"{ram.percent:.1f}%", ram.percent, GREEN),
            ("POWER", f"{current_power:.2f} W" if current_power is not None else "N/A", 0, PURPLE),
            ("BATTERY", f"{battery_percent:.0f}%" if battery_percent is not None else "N/A", battery_percent or 0, GREEN),
            ("DISK", f"{disk.percent:.1f}%", disk.percent, ORANGE),
        ]

        for i, (label, value, amount, colour) in enumerate(cards):
            x = i * (card_w + gap)
            rect = pygame.Rect(x, card_y, card_w, card_h)
            panel(canvas, rect)
            text(canvas, label, x + 11, card_y + 10, SMALL, colour)
            text(canvas, value, x + 11, card_y + 34, BIG, WHITE)
            if label == "POWER":
                text(canvas, current_power_source, x + 11, card_y + 76, TINY, MUTED)
            else:
                bar(canvas, x + 11, card_y + 77, card_w - 22, 10, amount, 100, status_colour(amount))

        # --------------------------------------------------------
        # QUICK SYSTEM INFO
        # --------------------------------------------------------

        qy = 185
        qh = 145
        left = pygame.Rect(0, qy, content_width // 2 - 5, qh)
        right = pygame.Rect(content_width // 2 + 5, qy, content_width // 2 - 5, qh)

        panel(canvas, left, "SYSTEM")
        text(canvas, f"CPU       {CPU_NAME}", left.x + 12, left.y + 36, SMALL)
        text(canvas, f"Architecture  {ARCH}", left.x + 12, left.y + 58, SMALL)
        text(canvas, f"OS        {OS_NAME}", left.x + 12, left.y + 80, SMALL)
        text(canvas, f"Python    {PYTHON_VERSION}", left.x + 12, left.y + 102, SMALL)
        text(canvas, f"Uptime    {uptime_text()}", left.x + 12, left.y + 124, SMALL)

        panel(canvas, right, "MEMORY / POWER")
        text(canvas, f"RAM       {ram.used / (1024**3):.1f} / {ram.total / (1024**3):.1f} GB", right.x + 12, right.y + 36, SMALL)
        text(canvas, f"Available {ram.available / (1024**3):.1f} GB", right.x + 12, right.y + 58, SMALL)
        text(canvas, f"Swap      {swap.percent:.1f}%  ({nice_bytes(swap.used)})", right.x + 12, right.y + 80, SMALL)
        text(canvas, f"Power     {current_power:.2f} W" if current_power is not None else "Power     N/A", right.x + 12, right.y + 102, SMALL)
        text(canvas, f"Battery   {'CHARGING' if charging else 'ON BATTERY' if battery_percent is not None else 'N/A'}", right.x + 12, right.y + 124, SMALL, GREEN if charging else WHITE)

        # --------------------------------------------------------
        # PERFORMANCE GRAPHS
        # --------------------------------------------------------

        graph_y = 345
        graph_h = 230
        graph_w = content_width // 2 - 7

        panel(canvas, pygame.Rect(0, graph_y, graph_w, graph_h), "CPU / RAM")
        draw_graph(
            canvas,
            pygame.Rect(10, graph_y + 35, graph_w - 20, graph_h - 47),
            [cpu_history, ram_history],
            ["CPU", "RAM"],
            [100, 100],
            [CYAN, GREEN],
        )

        panel(canvas, pygame.Rect(graph_w + 14, graph_y, graph_w, graph_h), "NETWORK")
        draw_graph(
            canvas,
            pygame.Rect(graph_w + 24, graph_y + 35, graph_w - 20, graph_h - 47),
            [download_history, upload_history],
            ["DOWN", "UP"],
            [max(1, max(download_history, default=1)), max(1, max(upload_history, default=1))],
            [CYAN, PURPLE],
        )

        # --------------------------------------------------------
        # CPU CORES
        # --------------------------------------------------------

        core_y = 590
        core_h = 115
        panel(canvas, pygame.Rect(0, core_y, content_width, core_h), "CPU CORES")
        core_count = max(1, len(cpu_per_core))
        core_w = max(55, (content_width - 24) // core_count)

        for i, value in enumerate(cpu_per_core):
            x = 12 + i * core_w
            text(canvas, f"C{i}", x, core_y + 34, TINY, MUTED)
            bar(canvas, x, core_y + 54, core_w - 10, 18, value, 100, status_colour(value))
            text(canvas, f"{value:.0f}%", x, core_y + 78, TINY, WHITE)

        # --------------------------------------------------------
        # STORAGE
        # --------------------------------------------------------

        storage_y = 725
        storage_h = 180
        storage_rect = pygame.Rect(0, storage_y, content_width, storage_h)
        panel(canvas, storage_rect, "STORAGE")

        drives = get_drives()
        for i, drive in enumerate(drives[:4]):
            yy = storage_y + 38 + i * 34
            name = drive["name"][:24]
            text(canvas, name, 12, yy, SMALL)
            text(canvas, f"{nice_bytes(drive['used'])} / {nice_bytes(drive['total'])}", 205, yy, TINY, MUTED)
            bar(canvas, 405, yy + 2, content_width - 485, 11, drive["percent"], 100, ORANGE)
            text(canvas, f"{drive['percent']:.1f}%", content_width - 68, yy, TINY, WHITE)

        text(canvas, f"Read  {nice_speed(read_speed)}", 12, storage_y + 151, TINY, CYAN)
        text(canvas, f"Write {nice_speed(write_speed)}", 170, storage_y + 151, TINY, PURPLE)

        # --------------------------------------------------------
        # PROCESSES
        # --------------------------------------------------------

        proc_y = 925
        proc_h = 320
        proc_rect = pygame.Rect(0, proc_y, content_width, proc_h)
        panel(canvas, proc_rect, f"PROCESS MANAGER  •  SORT: {process_sort.upper()}")
        text(canvas, "M = RAM   C = CPU", content_width - 180, proc_y + 10, TINY, MUTED)

        sorted_processes = sorted(
            processes_cache,
            key=lambda p: p[process_sort],
            reverse=True,
        )[:13]

        py = proc_y + 38
        for process in sorted_processes:
            name = process["name"]
            if len(name) > 37:
                name = name[:34] + "..."
            text(canvas, name, 12, py, TINY)
            text(canvas, f"PID {process['pid']}", 320, py, TINY, MUTED)
            text(canvas, f"CPU {process['cpu']:.1f}%", 410, py, TINY, GREEN)
            text(canvas, f"RAM {process['memory']:.2f}%", 510, py, TINY, CYAN)
            text(canvas, f"{process['status']}", 630, py, TINY, MUTED)
            text(canvas, f"T {process['threads']}", 720, py, TINY, MUTED)
            py += 20

        # --------------------------------------------------------
        # PROCESS DETAILS / COMMAND CENTRE
        # --------------------------------------------------------

        detail_y = 1260
        detail_h = 185
        detail_rect = pygame.Rect(0, detail_y, content_width, detail_h)
        panel(canvas, detail_rect, "PROCESS COMMAND CENTRE")

        if sorted_processes:
            selected = sorted_processes[0]
            text(canvas, f"Selected: {selected['name']}", 12, detail_y + 38, BIG, WHITE)
            text(canvas, f"PID        {selected['pid']}", 12, detail_y + 70, SMALL)
            text(canvas, f"CPU        {selected['cpu']:.2f}%", 12, detail_y + 92, SMALL)
            text(canvas, f"RAM        {selected['memory']:.2f}%", 12, detail_y + 114, SMALL)
            text(canvas, f"Status     {selected['status']}", 12, detail_y + 136, SMALL)
            text(canvas, "Use this section as the starting point for clickable process selection.", 330, detail_y + 48, SMALL, MUTED)
            text(canvas, "Safe management actions can be added here: Details • Locate • Terminate", 330, detail_y + 74, SMALL, MUTED)
        else:
            text(canvas, "No process data available.", 12, detail_y + 42, SMALL, MUTED)

        # --------------------------------------------------------
        # NETWORK / CONNECTIONS
        # --------------------------------------------------------

        network_y = 1460
        network_h = 175
        left_net = pygame.Rect(0, network_y, content_width // 2 - 5, network_h)
        right_net = pygame.Rect(content_width // 2 + 5, network_y, content_width // 2 - 5, network_h)
        panel(canvas, left_net, "NETWORK")
        text(canvas, f"IP address       {get_ip()}", 12, network_y + 40, SMALL)
        text(canvas, f"Download        {nice_speed(download_speed)}", 12, network_y + 64, SMALL, CYAN)
        text(canvas, f"Upload          {nice_speed(upload_speed)}", 12, network_y + 88, SMALL, PURPLE)
        text(canvas, f"Total received  {nice_bytes(net.bytes_recv)}", 12, network_y + 112, SMALL, MUTED)
        text(canvas, f"Total sent      {nice_bytes(net.bytes_sent)}", 12, network_y + 136, SMALL, MUTED)

        panel(canvas, right_net, "CONNECTIONS")
        connections = get_connections()
        listening = sum(1 for c in connections if c.status == psutil.CONN_LISTEN)
        established = sum(1 for c in connections if c.status == psutil.CONN_ESTABLISHED)
        text(canvas, f"Connections     {len(connections)}", right_net.x + 12, network_y + 40, SMALL)
        text(canvas, f"Established     {established}", right_net.x + 12, network_y + 64, SMALL)
        text(canvas, f"Listening ports {listening}", right_net.x + 12, network_y + 88, SMALL)
        text(canvas, f"Ping 1.1.1.1    {last_ping:.1f} ms" if last_ping is not None else "Ping 1.1.1.1    N/A", right_net.x + 12, network_y + 112, SMALL, CYAN)
        text(canvas, "Refreshes automatically.", right_net.x + 12, network_y + 136, TINY, MUTED)

        # --------------------------------------------------------
        # BATTERY / HARDWARE
        # --------------------------------------------------------

        hardware_y = 1650
        hardware_h = 180
        panel(canvas, pygame.Rect(0, hardware_y, content_width, hardware_h), "POWER / BATTERY / HARDWARE")
        text(canvas, f"Battery health      {battery_info['health'] or 'Not exposed'}", 12, hardware_y + 40, SMALL)
        text(canvas, f"Cycle count         {battery_info['cycle'] if battery_info['cycle'] is not None else 'Not exposed'}", 12, hardware_y + 64, SMALL)
        text(canvas, f"Max capacity        {battery_info['capacity'] if battery_info['capacity'] is not None else 'Not exposed'}", 12, hardware_y + 88, SMALL)
        text(canvas, f"Voltage             {battery_info['voltage'] if battery_info['voltage'] is not None else 'Not exposed'}", 12, hardware_y + 112, SMALL)
        text(canvas, f"Temperature         {temperature_text}", 380, hardware_y + 40, TINY, WHITE)
        text(canvas, f"Fan                 {fan_text}", 380, hardware_y + 66, TINY, WHITE)
        text(canvas, f"Power source        {current_power_source}", 380, hardware_y + 92, SMALL, PURPLE)
        text(canvas, "Note: some Apple Silicon hardware sensors require extra macOS privileges.", 380, hardware_y + 124, TINY, MUTED)

        # --------------------------------------------------------
        # DIAGNOSTICS
        # --------------------------------------------------------

        diag_y = 1840
        diag_h = 175
        diag_rect = pygame.Rect(0, diag_y, content_width, diag_h)
        panel(canvas, diag_rect, "ORBIT DIAGNOSTICS")
        text(canvas, "Press D to run a fresh diagnostic scan.", 12, diag_y + 36, SMALL, MUTED)

        if last_diagnostics:
            dy = diag_y + 62
            for label, passed in last_diagnostics[:7]:
                mark = "PASS" if passed else "FAIL"
                colour = GREEN if passed else RED
                text(canvas, mark, 12, dy, TINY, colour)
                text(canvas, label, 65, dy, TINY, WHITE)
                dy += 17
            if last_diagnostic_time:
                text(canvas, f"Last scan: {time.strftime('%H:%M:%S')}", 420, diag_y + 36, TINY, MUTED)
        else:
            text(canvas, "No diagnostic scan has been run yet.", 12, diag_y + 66, SMALL, MUTED)

        # --------------------------------------------------------
        # ALERTS / EVENTS
        # --------------------------------------------------------

        alert_y = 2030
        alert_h = 175
        left_alert = pygame.Rect(0, alert_y, content_width // 2 - 5, alert_h)
        right_alert = pygame.Rect(content_width // 2 + 5, alert_y, content_width // 2 - 5, alert_h)

        panel(canvas, left_alert, "ALERTS")
        ay = alert_y + 38
        if alerts:
            for timestamp, message in list(alerts)[-6:]:
                text(canvas, timestamp, 12, ay, TINY, MUTED)
                text(canvas, message, 72, ay, TINY, RED)
                ay += 19
        else:
            text(canvas, "No active alerts.", 12, ay, SMALL, GREEN)

        panel(canvas, right_alert, "ORBIT TIMELINE")
        ey = alert_y + 38
        if events:
            for timestamp, message in list(events)[-6:]:
                text(canvas, timestamp, right_alert.x + 12, ey, TINY, MUTED)
                text(canvas, message, right_alert.x + 72, ey, TINY, WHITE)
                ey += 19
        else:
            text(canvas, "No events yet.", right_alert.x + 12, ey, SMALL, MUTED)

        # --------------------------------------------------------
        # PLUGINS / LOGIN ITEMS / HISTORY NOTE
        # --------------------------------------------------------

        extra_y = 2220
        plugin_rect = pygame.Rect(0, extra_y, content_width, 170)
        panel(canvas, plugin_rect, "ORBIT MODULES • STARTUP • HISTORY")

        px = 12
        py = extra_y + 38
        for name, online in get_plugin_status():
            text(canvas, ("ONLINE" if online else "OFFLINE"), px, py, TINY, GREEN if online else RED)
            text(canvas, name, px + 60, py, TINY, WHITE)
            py += 17
            if py > extra_y + 118:
                break

        text(canvas, f"LaunchAgents found: {len(login_items)}", 390, extra_y + 40, SMALL, WHITE)
        text(canvas, "History: live rolling graphs are stored for the current ORBIT session.", 390, extra_y + 66, TINY, MUTED)
        text(canvas, "For 1h / 6h / 24h / 7d history, the next step is saving these samples to a log file/database.", 390, extra_y + 86, TINY, MUTED)
        text(canvas, f"Session runtime: {int(now - START_TIME)}s", 390, extra_y + 108, TINY, CYAN)

        # --------------------------------------------------------
        # DRAW SCROLLABLE CANVAS
        # --------------------------------------------------------

        max_scroll = max(0, content_height - height)
        scroll = int(clamp(scroll, 0, max_scroll))

        viewport = pygame.Rect(15, 0, width - 30, height)
        screen.set_clip(viewport)
        screen.blit(canvas, (15, -scroll))
        screen.set_clip(None)

        # Scroll bar
        if max_scroll > 0:
            track_x = width - 10
            track_h = height - 12
            thumb_h = max(50, int(track_h * height / content_height))
            thumb_y = 6 + int((track_h - thumb_h) * scroll / max_scroll)
            pygame.draw.rect(screen, GRID, (track_x, 6, 5, track_h), border_radius=3)
            pygame.draw.rect(screen, CYAN, (track_x, thumb_y, 5, thumb_h), border_radius=3)

        # Fixed footer
        footer = pygame.Rect(0, height - 24, width, 24)
        pygame.draw.rect(screen, (12, 15, 20), footer)
        pygame.draw.line(screen, GRID, (0, height - 24), (width, height - 24), 1)
        text(screen, f"SYSTEM HEALTH  {score}/100  {health_text}", 10, height - 18, TINY, health_colour)
        text(screen, "SCROLL: wheel / ↑↓    M: RAM sort    C: CPU sort    D: diagnostics    R: refresh    ESC: quit", width - 625, height - 18, TINY, MUTED)

        pygame.display.flip()