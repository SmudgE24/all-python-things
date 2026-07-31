import pygame
import sys
import random
import time
import re
import OrbitCalc

def ALL_POWERFUL():
    # ============================================================
    # ORBIT COMMAND INTERPRETER + SCROLLABLE TERMINAL
    # ============================================================

    pygame.init()

    WIDTH = 1200
    HEIGHT = 700

    screen = pygame.display.set_mode(
        (WIDTH, HEIGHT),
        pygame.RESIZABLE
    )

    pygame.display.set_caption("Orbit Terminal")

    clock = pygame.time.Clock()

    # ============================================================
    # FONTS
    # ============================================================

    font = pygame.font.SysFont("couriernew", 20)
    title_font = pygame.font.SysFont("couriernew", 28, bold=True)

    # ============================================================
    # COLOURS
    # ============================================================

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (150, 150, 150)

    # ============================================================
    # ORBIT COMMAND DATABASE
    # ============================================================
    #
    # Normal questions go here.
    #
    # Example:
    #
    # "hello"
    #
    # can produce one of several random responses.
    #
    # ============================================================

    COMMANDS = {

        # ========================================================
        # GREETING
        # ========================================================

        "greeting": {

            "triggers": [
                "hello",
                "hi",
                "hey",
                "hello orbit",
                "hi orbit",
                "hey orbit"
            ],

            "responses": [
                "Hello.",
                "Hello. Orbit is ready.",
                "Greetings.",
                "Hello. All systems are operational."
            ]
        },


        # ========================================================
        # STATUS
        # ========================================================

        "status_question": {

            "triggers": [
                "how are you",
                "how are you doing",
                "are you okay",
                "are you alright",
                "how is orbit",
                "how are things"
            ],

            "responses": [
                "All systems are operating normally.",
                "Orbit is functioning correctly.",
                "Systems nominal.",
                "Everything is running smoothly."
            ]
        },


        # ========================================================
        # ABOUT ORBIT
        # ========================================================

        "about_orbit": {

            "triggers": [
                "what is orbit",
                "who are you",
                "what are you",
                "tell me about orbit",
                "explain orbit"
            ],

            "responses": [
                "I am Orbit, a modular Python system.",
                "Orbit is a modular software environment.",
                "I am Orbit. I manage modules, commands and system functions.",
                "Orbit is designed to coordinate multiple internal systems."
            ]
        },


        # ========================================================
        # HELP
        # ========================================================

        "help": {

            "triggers": [
                "help",
                "i need help",
                "can you help me",
                "what can you do",
                "what do you do"
            ],

            "responses": [
                "I can process commands, answer questions and control Orbit modules.",
                "I can interact with Orbit's internal systems.",
                "I can execute commands and communicate with Orbit's modules.",
                "Try typing /commands to see the available commands."
            ]
        },


        # ========================================================
        # CREATOR
        # ========================================================

        "creator": {

            "triggers": [
                "who created you",
                "who made you",
                "who built you",
                "who programmed you",
                "who is your creator"
            ],

            "responses": [
                "I was created by Ethan.",
                "Ethan built Orbit.",
                "My creator is Ethan.",
                "Orbit was developed by Ethan."
            ]
        },


        # ========================================================
        # TEST
        # ========================================================

        "test": {

            "triggers": [
                "test",
                "run test",
                "test orbit",
                "is this working",
                "are you working"
            ],

            "responses": [
                "Test successful.",
                "Orbit Terminal is functioning correctly.",
                "Command interpreter operational.",
                "All interpreter systems responding."
            ]
        },


        # ========================================================
        # PING
        # ========================================================

        "ping": {

            "triggers": [
                "ping",
                "ping orbit",
                "are you there"
            ],

            "responses": [
                "PONG",
                "PONG.",
                "Orbit responding.",
                "Signal received."
            ]
        },


        # ========================================================
        # CPU
        # ========================================================

        "cpu": {

            "triggers": [
                "cpu",
                "check cpu",
                "cpu usage",
                "what is my cpu usage",
                "how much cpu am i using",
                "processor usage"
            ],

            "responses": [
                "CPU monitoring is currently active.",
                "CPU usage is being monitored by OrbitProcess.",
                "CPU data has been requested.",
                "OrbitProcess is monitoring the processor."
            ]
        },


        # ========================================================
        # MEMORY
        # ========================================================

        "memory": {

            "triggers": [
                "memory",
                "ram",
                "check ram",
                "ram usage",
                "memory usage",
                "how much ram am i using"
            ],

            "responses": [
                "Memory monitoring is active.",
                "OrbitProcess is monitoring system memory.",
                "RAM information has been requested.",
                "Memory statistics are being collected."
            ]
        },


        # ========================================================
        # TIME
        # ========================================================

        "time_question": {

            "triggers": [
                "what time is it",
                "what is the time",
                "current time",
                "tell me the time"
            ],

            "responses": [
                "The current time is being retrieved.",
                "Checking system time...",
                "Retrieving current time..."
            ]
        }

    }


    # ============================================================
    # ORBIT BASE QUESTIONS
    # ============================================================
    #
    # Base questions are commands that send whatever comes AFTER
    # the trigger directly to another Orbit module.
    #
    # Example:
    #
    #     calc 44*99
    #
    # becomes:
    #
    #     OrbitCalc.calc("44*99")
    #
    # ============================================================

    BASE_QUESTIONS = {

        # ========================================================
        # CALCULATOR
        # ========================================================

        "calculator": {

            "triggers": [
                "calc",
                "calculate",
                "calculator"
            ],

            "function": OrbitCalc.calc
        }

    }


    # ============================================================
    # TERMINAL HISTORY
    # ============================================================

    terminal_lines = [
        "==============================================",
        "              ORBIT TERMINAL",
        "==============================================",
        "Orbit Command Interpreter initialized.",
        "Orbit Base Questions initialized.",
        "OrbitCalc connected.",
        "Type /help for help.",
        ""
    ]

    user_input = ""

    # ============================================================
    # SCROLL SETTINGS
    # ============================================================

    scroll_offset = 0

    SCROLL_AMOUNT = 60

    # ============================================================
    # TEXT NORMALISATION
    # ============================================================

    def normalize(text):

        text = text.lower().strip()

        text = re.sub(
            r"[^\w\s]",
            "",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text


    # ============================================================
    # FIND COMMAND
    # ============================================================

    def find_command(user_text):

        user_text = normalize(user_text)

        best_command = None
        best_score = 0

        for command_name, command_data in COMMANDS.items():

            for trigger in command_data["triggers"]:

                trigger = normalize(trigger)

                if user_text == trigger:

                    score = 1000 + len(trigger)

                elif trigger in user_text:

                    score = len(trigger)

                else:

                    continue

                if score > best_score:

                    best_score = score
                    best_command = command_name

        return best_command


    # ============================================================
    # FIND BASE QUESTION
    # ============================================================

    def find_base_question(user_text):

        text = user_text.strip()

        for question_name, question_data in BASE_QUESTIONS.items():

            for trigger in question_data["triggers"]:

                trigger_lower = trigger.lower()

                # --------------------------------
                # Trigger with argument
                # --------------------------------

                if text.lower().startswith(
                    trigger_lower + " "
                ):

                    argument = text[
                        len(trigger):
                    ].strip()

                    return question_data["function"], argument


                # --------------------------------
                # Trigger with nothing after it
                # --------------------------------

                elif text.lower() == trigger_lower:

                    return question_data["function"], ""


        return None, None


    # ============================================================
    # GET RANDOM RESPONSE
    # ============================================================

    def get_response(command_name):

        command = COMMANDS[command_name]

        return random.choice(
            command["responses"]
        )


    # ============================================================
    # PROCESS COMMAND
    # ============================================================

    def process_command(user_text):

        text = user_text.strip()
        lower = text.lower()

        if not text:
            return ""

        # ========================================================
        # BUILT-IN HELP
        # ========================================================

        if lower == "/help":

            return (
                "Built-in commands:\n"
                "/help       Show help\n"
                "/commands   Show Orbit commands\n"
                "/base       Show base questions\n"
                "/clear      Clear terminal\n"
                "/time       Show current time\n"
                "/status     Show interpreter status\n"
                "/top        Go to top\n"
                "/bottom     Go to bottom\n"
                "/exit       Exit Orbit"
            )


        # ========================================================
        # COMMAND LIST
        # ========================================================

        if lower == "/commands":

            names = list(COMMANDS.keys())

            return (
                "Loaded Orbit commands:\n"
                + "\n".join(
                    "  " + name
                    for name in names
                )
            )


        # ========================================================
        # BASE QUESTION LIST
        # ========================================================

        if lower == "/base":

            names = list(BASE_QUESTIONS.keys())

            return (
                "Loaded Orbit base questions:\n"
                + "\n".join(
                    "  " + name
                    for name in names
                )
            )


        # ========================================================
        # CLEAR
        # ========================================================

        if lower == "/clear":

            terminal_lines.clear()

            return ""


        # ========================================================
        # TIME
        # ========================================================

        if lower == "/time":

            return (
                "Current time: "
                + time.strftime("%H:%M:%S")
            )


        # ========================================================
        # STATUS
        # ========================================================

        if lower == "/status":

            return (
                "Orbit Command Interpreter: ONLINE\n"
                f"Commands loaded: {len(COMMANDS)}\n"
                f"Base questions loaded: {len(BASE_QUESTIONS)}"
            )


        # ========================================================
        # TOP
        # ========================================================

        if lower == "/top":

            return "__ORBIT_TOP__"


        # ========================================================
        # BOTTOM
        # ========================================================

        if lower == "/bottom":

            return "__ORBIT_BOTTOM__"


        # ========================================================
        # EXIT
        # ========================================================

        if lower == "/exit":

            pygame.quit()
            sys.exit()


        # ========================================================
        # BASE QUESTION
        # ========================================================
        #
        # This is checked BEFORE normal questions because we want
        # to preserve the argument exactly.
        #
        # Example:
        #
        # calc 44*99
        #
        # must NOT have the * removed by normalize().
        #
        # ========================================================

        base_function, argument = find_base_question(text)

        if base_function is not None:

            try:

                result = base_function(
                    argument
                )

                return str(result)

            except Exception as error:

                return (
                    "Module Error: "
                    + str(error)
                )


        # ========================================================
        # NORMAL QUESTION
        # ========================================================

        command_name = find_command(text)

        if command_name is not None:

            return get_response(
                command_name
            )


        # ========================================================
        # UNKNOWN COMMAND
        # ========================================================

        return (
            "I don't understand that command.\n"
            "Type /help for assistance."
        )


    # ============================================================
    # EXPAND TERMINAL LINES
    # ============================================================

    def get_display_lines():

        display_lines = []

        for line in terminal_lines:

            parts = line.split("\n")

            for part in parts:

                display_lines.append(
                    part
                )

        return display_lines


    # ============================================================
    # CALCULATE MAXIMUM SCROLL
    # ============================================================

    def get_max_scroll():

        width, height = screen.get_size()

        terminal_top = 75
        terminal_bottom = height - 65

        available_height = (
            terminal_bottom
            - terminal_top
        )

        visible_lines = max(
            1,
            available_height // 25
        )

        display_lines = get_display_lines()

        total_lines = len(display_lines)

        max_scroll = max(
            0,
            (
                total_lines
                - visible_lines
            ) * 25
        )

        return max_scroll


    # ============================================================
    # KEEP SCROLL IN RANGE
    # ============================================================

    def clamp_scroll():

        nonlocal scroll_offset

        maximum = get_max_scroll()

        scroll_offset = max(
            0,
            min(
                scroll_offset,
                maximum
            )
        )


    # ============================================================
    # DRAW TERMINAL
    # ============================================================

    def draw_terminal():

        nonlocal scroll_offset

        screen.fill(
            BLACK
        )

        width, height = screen.get_size()

        # ========================================================
        # TITLE
        # ========================================================

        title = title_font.render(
            "ORBIT TERMINAL",
            True,
            WHITE
        )

        screen.blit(
            title,
            (20, 15)
        )

        pygame.draw.line(
            screen,
            GREY,
            (20, 55),
            (width - 20, 55),
            1
        )

        # ========================================================
        # TERMINAL AREA
        # ========================================================

        terminal_top = 75
        terminal_bottom = height - 65

        display_lines = get_display_lines()

        line_height = 25

        first_line = int(
            scroll_offset
            / line_height
        )

        visible_count = (
            (
                terminal_bottom
                - terminal_top
            )
            // line_height
        ) + 2

        # ========================================================
        # TERMINAL SURFACE
        # ========================================================

        terminal_surface = pygame.Surface(
            (
                width,
                terminal_bottom - terminal_top
            )
        )

        terminal_surface.fill(
            BLACK
        )

        local_y = -(
            scroll_offset
            % line_height
        )

        for index in range(
            first_line,
            min(
                first_line + visible_count,
                len(display_lines)
            )
        ):

            line = display_lines[index]

            text = font.render(
                line,
                True,
                WHITE
            )

            terminal_surface.blit(
                text,
                (20, local_y)
            )

            local_y += line_height

        screen.blit(
            terminal_surface,
            (0, terminal_top)
        )

        # ========================================================
        # SCROLLBAR
        # ========================================================

        max_scroll = get_max_scroll()

        if max_scroll > 0:

            scrollbar_x = width - 12

            scrollbar_top = (
                terminal_top
            )

            scrollbar_height = (
                terminal_bottom
                - terminal_top
            )

            pygame.draw.rect(
                screen,
                (50, 50, 50),
                (
                    scrollbar_x,
                    scrollbar_top,
                    6,
                    scrollbar_height
                )
            )

            total_lines = len(
                display_lines
            )

            visible_lines_count = max(
                1,
                scrollbar_height
                // line_height
            )

            thumb_height = max(
                30,
                int(
                    scrollbar_height
                    * visible_lines_count
                    / max(
                        total_lines,
                        visible_lines_count
                    )
                )
            )

            thumb_range = (
                scrollbar_height
                - thumb_height
            )

            thumb_y = scrollbar_top

            if max_scroll > 0:

                thumb_y += int(
                    thumb_range
                    * (
                        scroll_offset
                        / max_scroll
                    )
                )

            pygame.draw.rect(
                screen,
                GREY,
                (
                    scrollbar_x,
                    thumb_y,
                    6,
                    thumb_height
                )
            )

        # ========================================================
        # INPUT LINE
        # ========================================================

        pygame.draw.line(
            screen,
            GREY,
            (20, height - 55),
            (width - 20, height - 55),
            1
        )

        prompt = font.render(
            "Orbit> "
            + user_input
            + "_",
            True,
            WHITE
        )

        screen.blit(
            prompt,
            (20, height - 38)
        )

        pygame.display.flip()


    # ============================================================
    # MAIN LOOP
    # ============================================================

    running = True

    while running:

        for event in pygame.event.get():

            # ====================================================
            # WINDOW CLOSED
            # ====================================================

            if event.type == pygame.QUIT:
                pygame.quit()
                running = False


            # ====================================================
            # MOUSE WHEEL
            # ====================================================

            elif event.type == pygame.MOUSEWHEEL:

                if event.y > 0:

                    scroll_offset -= (
                        SCROLL_AMOUNT
                        * event.y
                    )

                elif event.y < 0:

                    scroll_offset -= (
                        SCROLL_AMOUNT
                        * event.y
                    )

                clamp_scroll()


            # ====================================================
            # KEYBOARD
            # ====================================================

            elif event.type == pygame.KEYDOWN:

                # =================================================
                # UP
                # =================================================

                if event.key == pygame.K_UP:

                    scroll_offset -= (
                        SCROLL_AMOUNT
                    )

                    clamp_scroll()


                # =================================================
                # DOWN
                # =================================================

                elif event.key == pygame.K_DOWN:

                    scroll_offset += (
                        SCROLL_AMOUNT
                    )

                    clamp_scroll()


                # =================================================
                # HOME
                # =================================================

                elif event.key == pygame.K_HOME:

                    scroll_offset = 0


                # =================================================
                # END
                # =================================================

                elif event.key == pygame.K_END:

                    scroll_offset = (
                        get_max_scroll()
                    )

                elif event.key == pygame.K_ESCAPE:
                    running = False


                # =================================================
                # ENTER
                # =================================================

                elif event.key == pygame.K_RETURN:

                    if user_input.strip():

                        # -----------------------------------------
                        # SHOW USER INPUT
                        # -----------------------------------------

                        terminal_lines.append(
                            "Orbit> "
                            + user_input
                        )

                        # -----------------------------------------
                        # PROCESS INPUT
                        # -----------------------------------------

                        response = process_command(
                            user_input
                        )

                        # -----------------------------------------
                        # SPECIAL SCROLL COMMANDS
                        # -----------------------------------------

                        if response == "__ORBIT_TOP__":

                            scroll_offset = 0

                        elif response == "__ORBIT_BOTTOM__":

                            scroll_offset = (
                                get_max_scroll()
                            )

                        # -----------------------------------------
                        # NORMAL RESPONSE
                        # -----------------------------------------

                        elif response:

                            terminal_lines.append(
                                response
                            )

                        # -----------------------------------------
                        # CLEAR INPUT
                        # -----------------------------------------

                        user_input = ""

                        # -----------------------------------------
                        # RETURN TO BOTTOM
                        # -----------------------------------------

                        scroll_offset = (
                            get_max_scroll()
                        )


                # =================================================
                # BACKSPACE
                # =================================================

                elif event.key == pygame.K_BACKSPACE:

                    user_input = (
                        user_input[:-1]
                    )

                    scroll_offset = (
                        get_max_scroll()
                    )


                # =================================================
                # NORMAL CHARACTER
                # =================================================

                else:

                    if event.unicode.isprintable():

                        user_input += (
                            event.unicode
                        )

                        scroll_offset = (
                            get_max_scroll()
                        )


        # ========================================================
        # DRAW
        # ========================================================

        draw_terminal()

        clock.tick(60)