# Nook — Desktop Home

A first-version Mac-inspired desktop homepage built entirely in Python with Pygame.

## Run

```bash
python3 -m pip install pygame
python3 app.py
```

## Included plugins

- **Focus** — 25-minute focus timer with start/pause.
- **Quick note** — Click the note field, type, and press Enter to save.
- **Weather** — A lightweight local weather card mockup.
- **Calculator** — A visual calculator placeholder ready for the next iteration.

All plugins are self-contained in `app.py` and registered in `PLUGIN_CLASSES` near the middle of the file. This keeps the first version portable and makes the plugin system easy to extend.

## Controls

- Click **Overview** or **All plugins** in the sidebar.
- Click the Focus card to start/pause the timer.
- Click the Quick note field to edit it.
- Press `Esc` to return to Overview.
- Close the window to quit.
