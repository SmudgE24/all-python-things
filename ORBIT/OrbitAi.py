import ollama
import pygame
import threading
import sys
import os
import shutil
import subprocess
import time

# ============================================================
# ORBIT AI - MODEL CONFIGURATION
# ============================================================

FALLBACK_MODEL = "qwen3:0.6b"
BIG_MODEL = "qwen3-coder"

DRIVE_PATH = "/Volumes/ETHANS 1TB"
DRIVE_MODEL_PATH = "/Volumes/ETHANS 1TB/OllamaModels"


def drive_connected():
    return os.path.isdir(DRIVE_PATH)


def get_model():
    """
    Choose the best available model.

    If the removable drive is connected:
        qwen3-coder

    Otherwise:
        qwen3:0.6b
    """

    if drive_connected():
        return BIG_MODEL

    return FALLBACK_MODEL


CURRENT_MODEL = get_model()


# ============================================================
# AI
# ============================================================

def get_ai_response(messages):
    global CURRENT_MODEL

    try:
        CURRENT_MODEL = get_model()

        response = ollama.chat(
            model=CURRENT_MODEL,
            messages=messages
        )

        return response["message"]["content"]

    except Exception as e:
        return f"Error connecting to {CURRENT_MODEL}:\n{e}"


# ============================================================
# CLI MODE
# ============================================================

def shell_out():

    print("\n==============================")
    print("       ORBIT AI - CLI")
    print("==============================")

    print(f"Model: {get_model()}")
    print("Type 'exit' or 'quit' to stop.\n")

    messages = []

    while True:

        try:
            user_input = input("You: ")

        except KeyboardInterrupt:
            break

        if user_input.lower() in ["exit", "quit"]:
            break

        if not user_input.strip():
            continue

        messages.append({
            "role": "user",
            "content": user_input
        })

        print("\nOrbit AI: ", end="", flush=True)

        ai_message = get_ai_response(messages)

        print(ai_message)
        print()

        messages.append({
            "role": "assistant",
            "content": ai_message
        })


# ============================================================
# PYGAME CONFIG
# ============================================================

WIDTH = 1000
HEIGHT = 700

BG_COLOR = (18, 20, 25)
PANEL_COLOR = (25, 28, 35)
INPUT_BG = (35, 39, 48)

TEXT_COLOR = (235, 238, 245)

USER_COLOR = (100, 190, 255)
AI_COLOR = (130, 230, 150)

HEADER_COLOR = (30, 34, 42)

BORDER_COLOR = (60, 65, 75)

FONT_SIZE = 21
SMALL_FONT = 16

PADDING = 14


# ============================================================
# ORBIT GUI
# ============================================================

class OrbitGUI:

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT),
            pygame.RESIZABLE
        )

        pygame.display.set_caption(
            "Orbit AI"
        )

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(
            "Arial",
            FONT_SIZE
        )

        self.small_font = pygame.font.SysFont(
            "Arial",
            SMALL_FONT
        )

        self.title_font = pygame.font.SysFont(
            "Arial",
            25,
            bold=True
        )

        self.messages = []

        self.user_text = ""

        self.scroll_y = 0

        self.is_loading = False

        self.running = True

        self.input_rect = pygame.Rect(
            PADDING,
            HEIGHT - 60,
            WIDTH - 2 * PADDING,
            45
        )

        self.history_rect = pygame.Rect(
            0,
            55,
            WIDTH,
            HEIGHT - 125
        )


    # ========================================================
    # TEXT WRAPPING
    # ========================================================

    def wrap_text(self, text, width, color):

        lines = []

        paragraphs = text.split("\n")

        for paragraph in paragraphs:

            if not paragraph:
                lines.append("")
                continue

            words = paragraph.split()

            current_line = ""

            for word in words:

                test_line = (
                    word
                    if not current_line
                    else current_line + " " + word
                )

                if self.font.size(test_line)[0] <= width:

                    current_line = test_line

                else:

                    if current_line:
                        lines.append(current_line)

                    current_line = word

            if current_line:
                lines.append(current_line)

        return [
            self.font.render(
                line,
                True,
                color
            )
            for line in lines
        ]


    # ========================================================
    # TOTAL CHAT HEIGHT
    # ========================================================

    def get_chat_height(self):

        total_height = PADDING

        for msg in self.messages:

            wrapped = self.wrap_text(
                msg["text"],
                WIDTH - 80,
                TEXT_COLOR
            )

            total_height += (
                FONT_SIZE + 6
            )

            total_height += (
                len(wrapped)
                * (FONT_SIZE + 5)
            )

            total_height += 18

        return total_height


    # ========================================================
    # SCROLL TO BOTTOM
    # ========================================================

    def scroll_to_bottom(self):

        total_height = self.get_chat_height()

        available = self.history_rect.height

        if total_height > available:

            self.scroll_y = (
                available
                - total_height
                - PADDING
            )

        else:

            self.scroll_y = 0


    # ========================================================
    # AI THREAD
    # ========================================================

    def get_response_gui(self, prompt):

        self.is_loading = True

        try:

            chat_history = []

            for m in self.messages:

                if m["type"] == "user":

                    chat_history.append({
                        "role": "user",
                        "content": m["text"]
                    })

                elif m["type"] == "ai":

                    chat_history.append({
                        "role": "assistant",
                        "content": m["text"]
                    })

            ai_text = get_ai_response(
                chat_history
            )

            self.messages.append({
                "type": "ai",
                "text": ai_text
            })

        except Exception as e:

            self.messages.append({
                "type": "ai",
                "text": f"Error:\n{e}"
            })

        finally:

            self.is_loading = False

            self.scroll_to_bottom()


    # ========================================================
    # HEADER
    # ========================================================

    def draw_header(self):

        pygame.draw.rect(
            self.screen,
            HEADER_COLOR,
            (0, 0, WIDTH, 55)
        )

        title = self.title_font.render(
            "ORBIT AI",
            True,
            TEXT_COLOR
        )

        self.screen.blit(
            title,
            (PADDING, 14)
        )

        model = get_model()

        if model == BIG_MODEL:

            status = "● QWEN3-CODER  •  USB"

            status_color = (100, 230, 150)

        else:

            status = "● QWEN3 0.6B  •  LOCAL"

            status_color = (100, 180, 255)

        status_surface = self.small_font.render(
            status,
            True,
            status_color
        )

        self.screen.blit(
            status_surface,
            (
                WIDTH - status_surface.get_width() - PADDING,
                20
            )
        )


    # ========================================================
    # MESSAGE BUBBLES
    # ========================================================

    def draw_message(self, msg, y):

        is_user = msg["type"] == "user"

        if is_user:

            color = USER_COLOR
            prefix = "You"

        else:

            color = AI_COLOR
            prefix = "Orbit AI"

        prefix_surface = self.small_font.render(
            prefix,
            True,
            color
        )

        self.screen.blit(
            prefix_surface,
            (PADDING + 10, y)
        )

        y += 23

        wrapped = self.wrap_text(
            msg["text"],
            WIDTH - 80,
            TEXT_COLOR
        )

        for surface in wrapped:

            if (
                y > self.history_rect.y - 30
                and y < self.history_rect.bottom
            ):

                self.screen.blit(
                    surface,
                    (PADDING + 25, y)
                )

            y += FONT_SIZE + 5

        return y + 18


    # ========================================================
    # INPUT
    # ========================================================

    def draw_input(self):

        pygame.draw.rect(
            self.screen,
            INPUT_BG,
            self.input_rect,
            border_radius=10
        )

        pygame.draw.rect(
            self.screen,
            BORDER_COLOR,
            self.input_rect,
            width=1,
            border_radius=10
        )

        display_text = self.user_text

        if self.is_loading:

            display_text += "  Thinking..."

        else:

            display_text += "|"

        text_surface = self.font.render(
            display_text,
            True,
            TEXT_COLOR
        )

        self.screen.blit(
            text_surface,
            (
                self.input_rect.x + 12,
                self.input_rect.y + 10
            )
        )


    # ========================================================
    # SCROLLBAR
    # ========================================================

    def draw_scrollbar(self):

        total_height = self.get_chat_height()

        available = self.history_rect.height

        if total_height <= available:

            return

        bar_height = max(
            40,
            int(
                available
                * available
                / total_height
            )
        )

        max_scroll = total_height - available

        progress = (
            -self.scroll_y
            / max_scroll
            if max_scroll > 0
            else 0
        )

        bar_y = (
            self.history_rect.y
            +
            progress
            * (
                available
                - bar_height
            )
        )

        pygame.draw.rect(
            self.screen,
            BORDER_COLOR,
            (
                WIDTH - 7,
                bar_y,
                5,
                bar_height
            ),
            border_radius=3
        )


    # ========================================================
    # MAIN LOOP
    # ========================================================

    def run(self):

        while self.running:

            self.screen.fill(
                BG_COLOR
            )

            # -----------------------------------------------
            # EVENTS
            # -----------------------------------------------

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    self.running = False

                # -------------------------------------------
                # RESIZE
                # -------------------------------------------

                elif event.type == pygame.VIDEORESIZE:

                    global WIDTH, HEIGHT

                    WIDTH = max(
                        600,
                        event.w
                    )

                    HEIGHT = max(
                        400,
                        event.h
                    )

                    self.input_rect = pygame.Rect(
                        PADDING,
                        HEIGHT - 60,
                        WIDTH - 2 * PADDING,
                        45
                    )

                    self.history_rect = pygame.Rect(
                        0,
                        55,
                        WIDTH,
                        HEIGHT - 125
                    )

                # -------------------------------------------
                # MOUSE WHEEL
                # -------------------------------------------

                elif event.type == pygame.MOUSEWHEEL:

                    if self.history_rect.collidepoint(
                        pygame.mouse.get_pos()
                    ):

                        self.scroll_y += (
                            event.y * 25
                        )

                        if self.scroll_y > 0:

                            self.scroll_y = 0

                        total_height = (
                            self.get_chat_height()
                        )

                        max_scroll = (
                            self.history_rect.height
                            - total_height
                            - PADDING
                        )

                        if (
                            total_height
                            > self.history_rect.height
                        ):

                            if (
                                self.scroll_y
                                < max_scroll
                            ):

                                self.scroll_y = (
                                    max_scroll
                                )

                        else:

                            self.scroll_y = 0

                # -------------------------------------------
                # KEYBOARD
                # -------------------------------------------

                elif event.type == pygame.KEYDOWN:

                    if (
                        event.key
                        == pygame.K_RETURN
                        and not self.is_loading
                    ):

                        if self.user_text.strip():

                            prompt = (
                                self.user_text
                            )

                            self.messages.append({
                                "type": "user",
                                "text": prompt
                            })

                            self.user_text = ""

                            threading.Thread(
                                target=self.get_response_gui,
                                args=(prompt,),
                                daemon=True
                            ).start()

                            self.scroll_to_bottom()

                    elif (
                        event.key
                        == pygame.K_BACKSPACE
                    ):

                        self.user_text = (
                            self.user_text[:-1]
                        )

                    elif event.unicode:

                        self.user_text += (
                            event.unicode
                        )


            # =================================================
            # DRAW HEADER
            # =================================================

            self.draw_header()


            # =================================================
            # CHAT AREA
            # =================================================

            self.screen.set_clip(
                self.history_rect
            )

            current_y = (
                self.history_rect.y
                + self.scroll_y
                + PADDING
            )

            for msg in self.messages:

                current_y = self.draw_message(
                    msg,
                    current_y
                )

            self.screen.set_clip(None)


            # =================================================
            # LOADING INDICATOR
            # =================================================

            if self.is_loading:

                loading = self.small_font.render(
                    "Orbit AI is thinking...",
                    True,
                    AI_COLOR
                )

                self.screen.blit(
                    loading,
                    (
                        PADDING,
                        HEIGHT - 87
                    )
                )


            # =================================================
            # INPUT
            # =================================================

            self.draw_input()

            self.draw_scrollbar()


            # =================================================
            # DISPLAY
            # =================================================

            pygame.display.flip()

            self.clock.tick(60)


        pygame.quit()

        sys.exit()


# ============================================================
# PYGAME MODE
# ============================================================

def pygame_out():

    gui = OrbitGUI()

    gui.run()


# ============================================================
# ONE-LINE QUESTION
# ============================================================

def function_out(text):

    messages = [
        {
            "role": "user",
            "content": text
        }
    ]

    response = get_ai_response(
        messages
    )

    return f"Orbit AI: {response}"


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("==============================")
    print("         ORBIT AI")
    print("==============================")
    print()
    print("Detected model:")
    print(f"  {get_model()}")
    print()

    print("Choose your interface:")
    print("1. Text-operated (CLI)")
    print("2. UI-operated (Pygame)")
    print("3. One-line question")

    choice = input(
        "\nEnter choice (1, 2 or 3): "
    )

    if choice == "1":

        shell_out()

    elif choice == "2":

        pygame_out()

    elif choice == "3":

        question = input(
            "Enter your question: "
        )

        print(
            function_out(question)
        )

    else:

        print(
            "Invalid choice. Exiting."
        )


if __name__ == "__main__":

    main()