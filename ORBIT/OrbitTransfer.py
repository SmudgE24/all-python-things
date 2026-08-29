# ============================================================
# ORBIT TRANSFER
# ============================================================
#
# Backend for OrbitTransfer.
#
# Provides:
#   • Find real macOS .app applications
#   • Launch applications using the real macOS `open` command
#   • Create/delete saved app groups
#   • Add/remove applications from groups
#   • Open an entire app group
#   • Dispatch text commands for OrbitCommand
#
# Saved groups:
#   OrbitTransferGroups.json
#
# ============================================================

import json
import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
GROUP_FILE = BASE_DIR / "OrbitTransferGroups.json"

APPLICATION_FOLDERS = [
    Path("/Applications"),
    Path.home() / "Applications",
]


# ============================================================
# GROUP STORAGE
# ============================================================

def load_groups():
    if not GROUP_FILE.exists():
        return {}

    try:
        with open(GROUP_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data if isinstance(data, dict) else {}

    except (json.JSONDecodeError, OSError):
        return {}


def save_groups(groups):
    try:
        with open(GROUP_FILE, "w", encoding="utf-8") as file:
            json.dump(groups, file, indent=4)

        return True

    except OSError:
        return False


# ============================================================
# APPLICATION DISCOVERY
# ============================================================

def find_apps():
    apps = []
    seen = set()

    for folder in APPLICATION_FOLDERS:
        if not folder.exists():
            continue

        try:
            for item in folder.iterdir():
                if item.is_dir() and item.suffix.lower() == ".app":
                    path = str(item.resolve())

                    if path not in seen:
                        apps.append({
                            "name": item.stem,
                            "path": path
                        })
                        seen.add(path)

        except (PermissionError, OSError):
            continue

    apps.sort(key=lambda app: app["name"].lower())
    return apps


def find_app(name):
    if not name:
        return None

    name = name.strip().strip('"').strip("'")

    if name.lower().endswith(".app"):
        name = name[:-4]

    apps = find_apps()

    # Exact match first.
    for app in apps:
        if app["name"].lower() == name.lower():
            return app

    # Then partial matches.
    matches = [
        app for app in apps
        if name.lower() in app["name"].lower()
    ]

    if len(matches) == 1:
        return matches[0]

    if len(matches) > 1:
        return matches

    return None


# ============================================================
# APP ACTIONS
# ============================================================

def list_apps():
    apps = find_apps()

    if not apps:
        return "No applications were found."

    output = "Installed Applications:\n\n"

    for app in apps:
        output += f"- {app['name']}\n"

    output += f"\n{len(apps)} applications found."
    return output


def open_app(name):
    result = find_app(name)

    if result is None:
        return f"Application not found: {name}"

    if isinstance(result, list):
        output = "Multiple applications matched:\n\n"
        for app in result:
            output += f"- {app['name']}\n"
        output += "\nPlease be more specific."
        return output

    try:
        subprocess.Popen(
            ["open", result["path"]],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return f"Launching {result['name']}..."

    except OSError as error:
        return f"Failed to launch {result['name']}: {error}"


# ============================================================
# GROUP ACTIONS
# ============================================================

def list_groups():
    groups = load_groups()

    if not groups:
        return "No app groups exist."

    output = "OrbitTransfer App Groups:\n\n"

    for group_name, apps in groups.items():
        output += f"[{group_name}]\n"

        for app in apps:
            output += f"  - {app}\n"

        output += "\n"

    return output.rstrip()


def create_group(name):
    name = name.strip()

    if not name:
        return "Group name cannot be empty."

    groups = load_groups()

    if name in groups:
        return f"Group already exists: {name}"

    groups[name] = []

    if save_groups(groups):
        return f"Created app group: {name}"

    return "Failed to save app group."


def delete_group(name):
    name = name.strip()
    groups = load_groups()

    if name not in groups:
        return f"Group not found: {name}"

    del groups[name]

    if save_groups(groups):
        return f"Deleted app group: {name}"

    return "Failed to save changes."


def add_to_group(group_name, app_name):
    group_name = group_name.strip()
    app_name = app_name.strip().strip('"').strip("'")

    groups = load_groups()

    if group_name not in groups:
        return f"Group not found: {group_name}"

    app = find_app(app_name)

    if app is None:
        return f"Application not found: {app_name}"

    if isinstance(app, list):
        output = "Multiple applications matched:\n\n"
        for match in app:
            output += f"- {match['name']}\n"
        return output

    real_name = app["name"]

    if real_name in groups[group_name]:
        return f"{real_name} is already in {group_name}."

    groups[group_name].append(real_name)

    if save_groups(groups):
        return f"Added {real_name} to {group_name}."

    return "Failed to save changes."


def remove_from_group(group_name, app_name):
    group_name = group_name.strip()
    app_name = app_name.strip().strip('"').strip("'")

    groups = load_groups()

    if group_name not in groups:
        return f"Group not found: {group_name}"

    match = next(
        (
            app for app in groups[group_name]
            if app.lower() == app_name.lower()
        ),
        None
    )

    if match is None:
        return f"{app_name} is not in {group_name}."

    groups[group_name].remove(match)

    if save_groups(groups):
        return f"Removed {match} from {group_name}."

    return "Failed to save changes."


def show_group(name):
    name = name.strip()
    groups = load_groups()

    if name not in groups:
        return f"Group not found: {name}"

    apps = groups[name]

    output = f"App Group: {name}\n\n"

    if not apps:
        output += "  (empty)"
        return output

    for app in apps:
        output += f"- {app}\n"

    return output.rstrip()


def open_group(name):
    name = name.strip()
    groups = load_groups()

    if name not in groups:
        return f"Group not found: {name}"

    apps = groups[name]

    if not apps:
        return f"Group '{name}' is empty."

    launched = []
    failed = []

    for app_name in apps:
        result = find_app(app_name)

        if result and not isinstance(result, list):
            try:
                subprocess.Popen(
                    ["open", result["path"]],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                launched.append(result["name"])

            except OSError:
                failed.append(app_name)

        else:
            failed.append(app_name)

    output = f"Opening group: {name}\n\n"

    for app in launched:
        output += f"[OK] {app}\n"

    for app in failed:
        output += f"[FAILED] {app}\n"

    return output.rstrip()


# ============================================================
# COMMAND DISPATCH
# ============================================================

def command(text):
    if text is None:
        return "No OrbitTransfer command supplied."

    text = text.strip()

    if not text:
        return "No OrbitTransfer command supplied."

    parts = text.split()
    action = parts[0].lower()

    if action in ["apps", "list"]:
        return list_apps()

    if action in ["open", "launch"]:
        if len(parts) < 2:
            return "Usage: launch <application>"

        return open_app(" ".join(parts[1:]))

    if action == "groups":
        return list_groups()

    if action != "group":
        return f"Unknown OrbitTransfer command: {action}"

    if len(parts) < 2:
        return (
            "Usage:\n"
            "group create <name>\n"
            "group delete <name>\n"
            "group add <group> <app>\n"
            "group remove <group> <app>\n"
            "group show <name>\n"
            "group open <name>"
        )

    group_action = parts[1].lower()

    if group_action == "create":
        if len(parts) < 3:
            return "Usage: group create <name>"
        return create_group(" ".join(parts[2:]))

    if group_action == "delete":
        if len(parts) < 3:
            return "Usage: group delete <name>"
        return delete_group(" ".join(parts[2:]))

    if group_action == "add":
        if len(parts) < 4:
            return "Usage: group add <group> <app>"
        return add_to_group(parts[2], " ".join(parts[3:]))

    if group_action == "remove":
        if len(parts) < 4:
            return "Usage: group remove <group> <app>"
        return remove_from_group(parts[2], " ".join(parts[3:]))

    if group_action == "show":
        if len(parts) < 3:
            return "Usage: group show <name>"
        return show_group(" ".join(parts[2:]))

    if group_action == "open":
        if len(parts) < 3:
            return "Usage: group open <name>"
        return open_group(" ".join(parts[2:]))

    return f"Unknown group command: {group_action}"


if __name__ == "__main__":
    print("OrbitTransfer backend loaded.")
    print(f"Found {len(find_apps())} applications.")
