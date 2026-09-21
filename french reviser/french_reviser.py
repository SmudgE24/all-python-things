run_pygame = True

if run_pygame:
    import pygame
    import json
    import random
    import os
    import unicodedata


    pygame.init()


    # --------------------------------------------------
    # SETTINGS
    # --------------------------------------------------

    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 700

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("French Reviser")

    clock = pygame.time.Clock()


    # --------------------------------------------------
    # FONTS
    # --------------------------------------------------

    title_font = pygame.font.Font(None, 60)
    question_font = pygame.font.Font(None, 45)
    answer_font = pygame.font.Font(None, 40)
    button_font = pygame.font.Font(None, 35)
    small_font = pygame.font.Font(None, 28)


    # --------------------------------------------------
    # LOAD JSON
    # --------------------------------------------------

    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(base_dir, "french_words.json")

    with open(json_file, "r", encoding="utf-8") as file:
        french_words = json.load(file)


    words = list(french_words.items())


    # --------------------------------------------------
    # FUNCTIONS
    # --------------------------------------------------

    def remove_accents(text):

        text = unicodedata.normalize("NFD", text)

        text = "".join(
            character
            for character in text
            if unicodedata.category(character) != "Mn"
        )

        return text


    def check_answer(answer, correct_answer):

        answer = answer.strip().lower()
        correct_answer = correct_answer.strip().lower()

        # Completely correct
        if answer == correct_answer:
            return "correct"

        # Correct apart from accents
        if remove_accents(answer) == remove_accents(correct_answer):
            return "accent"

        return "wrong"


    def draw_button(text, x, y, width, height):

        button_rectangle = pygame.Rect(x, y, width, height)

        pygame.draw.rect(screen, (70, 100, 180), button_rectangle)
        pygame.draw.rect(screen, (255, 255, 255), button_rectangle, 2)

        text_surface = button_font.render(text, True, (255, 255, 255))

        text_rectangle = text_surface.get_rect(center=button_rectangle.center)

        screen.blit(text_surface, text_rectangle)

        return button_rectangle


    def new_question():

        global french_word
        global english_word
        global direction
        global answer_box
        global result
        global hint_text
        global answer_checked

        french_word, english_word = random.choice(words)

        direction = random.choice(["fr-en", "en-fr"])

        answer_box = ""

        result = ""

        hint_text = ""

        answer_checked = False


    def get_hint():

        global hint_text

        if direction == "fr-en":

            # Hint for the English word
            hint_length = max(1, len(english_word) // 2)

            hint_text = english_word[:hint_length] + "..."

        else:

            # Hint for the French word
            hint_length = max(1, len(french_word) // 2)

            hint_text = french_word[:hint_length] + "..."


    # --------------------------------------------------
    # START
    # --------------------------------------------------

    score = 0
    questions = 0

    answer_box = ""
    result = ""
    hint_text = ""
    answer_checked = False

    new_question()


    running = True

    while running:

        # --------------------------------------------------
        # EVENTS
        # --------------------------------------------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False


            # Typing
            if event.type == pygame.TEXTINPUT:

                if not answer_checked:
                    answer_box += event.text


            # Keyboard
            if event.type == pygame.KEYDOWN:

                # Backspace
                if event.key == pygame.K_BACKSPACE:

                    if not answer_checked:
                        answer_box = answer_box[:-1]


                # Enter
                if event.key == pygame.K_RETURN:

                    if not answer_checked and answer_box != "":

                        questions += 1

                        if direction == "fr-en":
                            correct_answer = english_word
                        else:
                            correct_answer = french_word

                        answer_result = check_answer(
                            answer_box,
                            correct_answer
                        )

                        if answer_result == "correct":

                            score += 1
                            result = "CORRECT!"

                        elif answer_result == "accent":

                            score += 1

                            result = (
                                "Correct! But remember the accent: "
                                + correct_answer
                            )

                        else:

                            result = (
                                "Incorrect! Correct answer: "
                                + correct_answer
                            )

                        answer_checked = True


            # Mouse
            if event.type == pygame.MOUSEBUTTONDOWN:

                mouse_position = pygame.mouse.get_pos()


                # Hint button
                if hint_button.collidepoint(mouse_position):

                    if not answer_checked:
                        get_hint()


                # Next button
                if next_button.collidepoint(mouse_position):

                    if answer_checked:
                        new_question()


                # Answer box
                if answer_rectangle.collidepoint(mouse_position):

                    if not answer_checked:
                        pygame.key.start_text_input()


        # --------------------------------------------------
        # DRAW
        # --------------------------------------------------

        screen.fill((25, 30, 40))


        # Title
        title = title_font.render(
            "French Reviser",
            True,
            (255, 255, 255)
        )

        title_rectangle = title.get_rect(
            center=(SCREEN_WIDTH // 2, 60)
        )

        screen.blit(title, title_rectangle)


        # Score
        score_text = small_font.render(
            "Score: " + str(score) + " / " + str(questions),
            True,
            (220, 220, 220)
        )

        screen.blit(score_text, (30, 25))


        # --------------------------------------------------
        # QUESTION
        # --------------------------------------------------

        if direction == "fr-en":

            question_text = "Translate into English"

            word_to_show = french_word

        else:

            question_text = "Translate into French"

            word_to_show = english_word


        question_surface = question_font.render(
            question_text,
            True,
            (200, 200, 200)
        )

        question_rectangle = question_surface.get_rect(
            center=(SCREEN_WIDTH // 2, 150)
        )

        screen.blit(question_surface, question_rectangle)


        word_surface = title_font.render(
            word_to_show,
            True,
            (255, 255, 255)
        )

        word_rectangle = word_surface.get_rect(
            center=(SCREEN_WIDTH // 2, 220)
        )

        screen.blit(word_surface, word_rectangle)


        # --------------------------------------------------
        # ANSWER BOX
        # --------------------------------------------------

        answer_rectangle = pygame.Rect(
            250,
            290,
            500,
            60
        )

        pygame.draw.rect(
            screen,
            (45, 50, 65),
            answer_rectangle
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            answer_rectangle,
            2
        )


        answer_surface = answer_font.render(
            answer_box,
            True,
            (255, 255, 255)
        )

        screen.blit(
            answer_surface,
            (answer_rectangle.x + 15,
            answer_rectangle.y + 10)
        )


        # --------------------------------------------------
        # HINT
        # --------------------------------------------------

        hint_button = pygame.Rect(
            250,
            380,
            220,
            60
        )

        pygame.draw.rect(
            screen,
            (60, 120, 180),
            hint_button
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            hint_button,
            2
        )

        hint_surface = button_font.render(
            "HINT",
            True,
            (255, 255, 255)
        )

        hint_rectangle = hint_surface.get_rect(
            center=hint_button.center
        )

        screen.blit(hint_surface, hint_rectangle)


        # --------------------------------------------------
        # NEXT BUTTON
        # --------------------------------------------------

        next_button = pygame.Rect(
            530,
            380,
            220,
            60
        )

        pygame.draw.rect(
            screen,
            (60, 160, 90),
            next_button
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            next_button,
            2
        )

        next_surface = button_font.render(
            "NEXT",
            True,
            (255, 255, 255)
        )

        next_rectangle = next_surface.get_rect(
            center=next_button.center
        )

        screen.blit(next_surface, next_rectangle)


        # --------------------------------------------------
        # HINT TEXT
        # --------------------------------------------------

        if hint_text != "":

            hint_surface = small_font.render(
                "Hint: " + hint_text,
                True,
                (255, 220, 100)
            )

            hint_rectangle = hint_surface.get_rect(
                center=(SCREEN_WIDTH // 2, 480)
            )

            screen.blit(hint_surface, hint_rectangle)


        # --------------------------------------------------
        # RESULT
        # --------------------------------------------------

        if result != "":

            result_surface = small_font.render(
                result,
                True,
                (255, 255, 255)
            )

            result_rectangle = result_surface.get_rect(
                center=(SCREEN_WIDTH // 2, 550)
            )

            screen.blit(result_surface, result_rectangle)


        pygame.display.flip()

        clock.tick(60)


    pygame.quit()





try:
    pygame.quit()
except:
    pass





import json
import random
import os


# Find the folder this Python file is in
base_dir = os.path.dirname(os.path.abspath(__file__))

# Find the JSON file
json_file = os.path.join(base_dir, "french_words.json")


# Open the JSON file
with open(json_file, "r", encoding="utf-8") as file:
    french_words = json.load(file)


score = 0
questions = 0

# Turn the JSON dictionary into a list
words = list(french_words.items())


print("FRENCH VOCABULARY TEST")
print("----------------------")
print("Type 'quit' to stop.")
print()


while True:

    # Pick a random word
    french_word, english_word = random.choice(words)

    # Pick a random direction
    direction = random.choice(["fr-en", "en-fr"])


    # French -> English
    if direction == "fr-en":

        print()
        print("Translate into English:")
        print("French:", french_word)

        answer = input("Answer: ").strip().lower()

        if answer == "quit":
            break

        questions += 1

        if answer == english_word.lower():

            print("Correct!")
            score += 1

        else:

            print("Incorrect!")
            print("Correct answer:", english_word)


    # English -> French
    else:

        print()
        print("Translate into French:")
        print("English:", english_word)

        answer = input("Answer: ").strip().lower()

        if answer == "quit":
            break

        questions += 1

        if answer == french_word.lower():

            print("Correct!")
            score += 1

        else:

            print("Incorrect!")
            print("Correct answer:", french_word)


    print("Score:", score, "/", questions)


# Finished
print()
print("----------------------")
print("TEST FINISHED")

if questions > 0:

    percentage = (score / questions) * 100

    print("Final score:", score, "/", questions)
    print("Percentage:", round(percentage), "%")

else:

    print("No questions answered.")