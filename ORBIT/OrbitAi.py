#!/usr/bin/env python3
"""Orbit AI - local AI assistant with an optional Pygame ch([docs.ollama.com](https://docs.ollama.com/api/chat?utm_source=chatgpt.com))es Ollama for local AI responses, so no OpenAI ([docs.ollama.com](https://docs.ollama.com/api/chat?utm_source=chatgpt.com))

Modes:
    python OrbitAI.py
    python OrbitAI.py --ui
    python OrbitAI.py --cli
    python OrbitAI.py --text "Hello"

First-time setup:
    1. Install Ollama.
    2. Start Ollama.
    3. Download a model, for example:
           ollama pull qwen3:4b
    4. Run this file.

Ollama normally listens on:
    http://localhost:11434
"""

from __future__ import annotations

import argparse
import json
import re
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

ProviderName = Literal["offline", "ollama"]


class AIProviderError(RuntimeError):
    """Raised when the configured local AI provider cannot answer."""


@dataclass
class ChatMessage:
    """One message in a conversation."""

    role: Literal["user", "assistant"]
    content: str
    timestamp: datetime = field(default_factory=datetime.now)


class AIEngine:
    """Reusable text-based assistant.

    The default provider is Ollama, which runs the model locally on your Mac.
    """

    def __init__(
        self,
        provider: ProviderName = "ollama",
        model: str = "qwen3:4b",
        base_url: str = "http://localhost:11434",
        system_prompt: str = (
            "You are Orbit AI, a helpful and friendly assistant inside the Orbit "
            "operating environment. Give useful answers, explain things clearly, "
            "and keep responses reasonably concise unless the user asks for detail."
        ),
        max_history_turns: int = 8,
    ) -> None:
        if provider not in ("offline", "ollama"):
            raise ValueError("provider must be either 'offline' or 'ollama'.")
        if max_history_turns < 0:
            raise ValueError("max_history_turns must be zero or greater.")

        self.provider = provider
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.system_prompt = system_prompt
        self.max_history_turns = max_history_turns
        self.history: list[ChatMessage] = []

    def clear_history(self) -> None:
        """Remove all remembered user and assistant messages."""
        self.history.clear()

    def respond(self, text: str) -> str:
        """Return an assistant response for a single input string."""
        if not isinstance(text, str):
            raise TypeError("text must be a string.")

        prompt = text.strip()
        if not prompt:
            return "Please enter a message so I can respond."

        self.history.append(ChatMessage("user", prompt))

        if self.provider == "ollama":
            answer = self._ollama_response()
        else:
            answer = self._offline_response(prompt)

        answer = answer.strip() or "I could not generate a response."
        self.history.append(ChatMessage("assistant", answer))
        self._trim_history()
        return answer

    def _trim_history(self) -> None:
        """Limit stored context to the configured number of complete turns."""
        limit = self.max_history_turns * 2
        if limit == 0:
            self.history.clear()
        elif len(self.history) > limit:
            self.history[:] = self.history[-limit:]

    def _ollama_response(self) -> str:
        """Call Ollama's local /api/chat endpoint."""
        endpoint = f"{self.base_url}/api/chat"

        messages: list[dict[str, str]] = [
            {"role": "system", "content": self.system_prompt}
        ]
        messages.extend(
            {"role": item.role, "content": item.content}
            for item in self.history
        )

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }

        request = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "User-Agent": "OrbitAI/1.0",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=300) as response:
                raw = response.read().decode("utf-8")
                data = json.loads(raw)
        except urllib.error.HTTPError as error:
            try:
                details = error.read().decode("utf-8", errors="replace")
                parsed = json.loads(details)
                message = parsed.get("error", details)
            except Exception:
                message = error.reason
            raise AIProviderError(
                f"Ollama returned HTTP {error.code}: {message}"
            ) from error
        except urllib.error.URLError as error:
            raise AIProviderError(
                "Could not connect to Ollama. Make sure Ollama is installed "
                "and running, then try again."
            ) from error
        except json.JSONDecodeError as error:
            raise AIProviderError(
                "Ollama returned invalid JSON."
            ) from error

        try:
            content = data["message"]["content"]
        except (KeyError, TypeError) as error:
            if "error" in data:
                raise AIProviderError(str(data["error"])) from error
            raise AIProviderError(
                "Ollama returned an unexpected response format."
            ) from error

        if not isinstance(content, str):
            raise AIProviderError("Ollama did not return text content.")

        return content

    def _offline_response(self, prompt: str) -> str:
        """Small dependency-free fallback."""
        lowered = prompt.casefold()

        if re.search(r"\b(hello|hi|hey|greetings)\b", lowered):
            return "Hello! Orbit AI is running in offline demo mode."

        if "what can you do" in lowered or lowered == "help":
            return (
                "I can chat, remember recent messages, answer questions, "
                "and run inside Orbit's Pygame interface."
            )

        if "time" in lowered and ("what" in lowered or "current" in lowered):
            return (
                "The local time is "
                f"{datetime.now().strftime('%H:%M on %A, %B %d, %Y')}."
            )

        if re.search(r"\b(bye|goodbye|exit|quit)\b", lowered):
            return "Goodbye."

        calculation = self._try_safe_arithmetic(prompt)
        if calculation is not None:
            return f"The result is {calculation}."

        concise = " ".join(prompt.split())
        return f'Offline Orbit AI received: "{concise[:280]}"'

    @staticmethod
    def _try_safe_arithmetic(text: str) -> str | None:
        """Evaluate a deliberately limited arithmetic expression."""
        candidate = text.strip().replace("×", "*").replace("÷", "/")
        candidate = re.sub(
            r"^(what\s+is|calculate|compute)\s+",
            "",
            candidate,
            flags=re.I,
        )
        candidate = candidate.rstrip("?. ")

        if not candidate or not re.fullmatch(
            r"[0-9\s+\-*/().%]+", candidate
        ):
            return None

        try:
            result = eval(candidate, {"__builtins__": {}}, {})  # noqa: S307
        except (ArithmeticError, SyntaxError, TypeError, ValueError):
            return None

        if isinstance(result, (int, float)) and not isinstance(result, bool):
            return str(result)
        return None


def run_terminal_chat(ai: AIEngine) -> None:
    """Run an interactive terminal chat loop."""
    print("Orbit AI terminal chat started.")
    print("Type /clear to reset the conversation or /quit to exit.\n")

    while True:
        try:
            user_text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return

        if user_text.casefold() in {"/quit", "/exit"}:
            print("Goodbye.")
            return

        if user_text.casefold() == "/clear":
            ai.clear_history()
            print("Conversation cleared.")
            continue

        if not user_text:
            continue

        try:
            print(f"Orbit AI: {ai.respond(user_text)}\n")
        except AIProviderError as error:
            print(f"Orbit AI error: {error}\n")


def _wrapped_lines(font, text: str, max_width: int) -> list[str]:
    """Wrap text using actual Pygame font width."""
    lines: list[str] = []

    for paragraph in text.splitlines() or [""]:
        if not paragraph:
            lines.append("")
            continue

        current = ""
        for word in paragraph.split(" "):
            proposal = word if not current else f"{current} {word}"

            if font.size(proposal)[0] <= max_width:
                current = proposal
                continue

            if current:
                lines.append(current)

            while font.size(word)[0] > max_width and len(word) > 1:
                split_at = max(1, len(word) // 2)
                while (
                    split_at > 1
                    and font.size(word[:split_at])[0] > max_width
                ):
                    split_at -= 1
                lines.append(word[:split_at])
                word = word[split_at:]

            current = word

        lines.append(current)

    return lines


def run_pygame_chat(ai: AIEngine) -> None:
    """Open the Pygame chat interface."""
    try:
        import pygame
    except ImportError as error:
        raise RuntimeError(
            "Pygame is not installed. Install it with: "
            "python -m pip install pygame"
        ) from error

    pygame.init()
    pygame.display.set_caption("Orbit AI")

    width, height = 980, 700
    screen = pygame.display.set_mode(
        (width, height), pygame.RESIZABLE
    )
    clock = pygame.time.Clock()

    background = (18, 24, 38)
    panel = (28, 38, 57)
    input_panel = (38, 50, 74)
    user_bubble = (55, 95, 165)
    assistant_bubble = (46, 63, 87)
    accent = (111, 205, 255)
    text_color = (239, 244, 250)
    muted = (174, 190, 210)

    title_font = pygame.font.Font(None, 34)
    body_font = pygame.font.Font(None, 25)
    small_font = pygame.font.Font(None, 20)

    transcript: list[tuple[str, str, bool]] = [
        (
            "Orbit AI",
            "Hello! I am your local Orbit AI. Type a message and press Enter.",
            False,
        )
    ]

    typed = ""
    scroll_offset = 0
    running = True
    active = True

    def send_message() -> None:
        nonlocal typed, scroll_offset

        message = typed.strip()
        if not message:
            return

        typed = ""

        if message.casefold() == "/clear":
            ai.clear_history()
            transcript[:] = [
                ("Orbit AI", "Conversation cleared.", False)
            ]
            scroll_offset = 0
            return

        transcript.append(("You", message, True))

        try:
            answer = ai.respond(message)
            transcript.append(("Orbit AI", answer, False))
        except AIProviderError as error:
            transcript.append(("AI error", str(error), False))
        except Exception as error:
            transcript.append(("Application error", str(error), False))

        scroll_offset = 0

    while running:
        current_width, current_height = screen.get_size()
        current_width = max(520, current_width)
        current_height = max(420, current_height)

        header_rect = pygame.Rect(0, 0, current_width, 66)
        input_rect = pygame.Rect(
            18,
            current_height - 74,
            current_width - 150,
            52,
        )
        send_rect = pygame.Rect(
            current_width - 120,
            current_height - 74,
            102,
            52,
        )
        chat_rect = pygame.Rect(
            18,
            82,
            current_width - 36,
            current_height - 172,
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.VIDEORESIZE:
                new_w = max(520, event.size[0])
                new_h = max(420, event.size[1])
                screen = pygame.display.set_mode(
                    (new_w, new_h), pygame.RESIZABLE
                )

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    active = input_rect.collidepoint(event.pos)
                    if send_rect.collidepoint(event.pos):
                        send_message()
                        active = True

                elif event.button == 4:
                    scroll_offset = max(0, scroll_offset - 50)

                elif event.button == 5:
                    scroll_offset += 50

            elif event.type == pygame.MOUSEWHEEL:
                scroll_offset = max(0, scroll_offset - event.y * 50)

            elif event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    send_message()
                elif event.key == pygame.K_BACKSPACE:
                    typed = typed[:-1]
                elif event.key == pygame.K_ESCAPE:
                    active = False
                elif event.unicode and event.unicode.isprintable():
                    typed += event.unicode

        screen.fill(background)
        pygame.draw.rect(screen, panel, header_rect)

        screen.blit(
            title_font.render("Orbit AI", True, text_color),
            (20, 15),
        )

        status = (
            f"Local • {ai.model}"
            if ai.provider == "ollama"
            else "Offline demo"
        )
        status_surface = small_font.render(status, True, accent)
        screen.blit(
            status_surface,
            (
                current_width - status_surface.get_width() - 20,
                24,
            ),
        )

        pygame.draw.rect(
            screen,
            panel,
            chat_rect,
            border_radius=14,
        )

        clip_before = screen.get_clip()
        screen.set_clip(chat_rect)

        y = chat_rect.bottom - 16 + scroll_offset
        bubble_layout = []
        max_bubble_width = max(
            230,
            int(chat_rect.width * 0.74),
        )

        for speaker, message, is_user in reversed(transcript):
            lines = _wrapped_lines(
                body_font,
                message,
                max_bubble_width - 30,
            )

            bubble_height = 34 + len(lines) * 25
            bubble_width = min(
                max_bubble_width,
                max(
                    160,
                    max(
                        (body_font.size(line)[0] for line in lines),
                        default=0,
                    ) + 30,
                ),
            )

            y -= bubble_height
            x = (
                chat_rect.right - bubble_width - 14
                if is_user
                else chat_rect.left + 14
            )

            rect = pygame.Rect(
                x,
                y,
                bubble_width,
                bubble_height,
            )

            color = user_bubble if is_user else assistant_bubble
            bubble_layout.append(
                (rect, lines, color, speaker, is_user)
            )
            y -= 14

        min_y = min(
            (item[0].top for item in bubble_layout),
            default=chat_rect.top,
        )
        max_scroll = max(
            0,
            chat_rect.top - min_y + 14,
        )
        scroll_offset = min(scroll_offset, max_scroll)

        if scroll_offset and max_scroll:
            y = chat_rect.bottom - 16 + scroll_offset
            bubble_layout = []

            for speaker, message, is_user in reversed(transcript):
                lines = _wrapped_lines(
                    body_font,
                    message,
                    max_bubble_width - 30,
                )

                bubble_height = 34 + len(lines) * 25
                bubble_width = min(
                    max_bubble_width,
                    max(
                        160,
                        max(
                            (body_font.size(line)[0] for line in lines),
                            default=0,
                        ) + 30,
                    ),
                )

                y -= bubble_height
                x = (
                    chat_rect.right - bubble_width - 14
                    if is_user
                    else chat_rect.left + 14
                )

                rect = pygame.Rect(
                    x,
                    y,
                    bubble_width,
                    bubble_height,
                )

                color = user_bubble if is_user else assistant_bubble
                bubble_layout.append(
                    (rect, lines, color, speaker, is_user)
                )
                y -= 14

        for rect, lines, color, speaker, is_user in bubble_layout:
            pygame.draw.rect(
                screen,
                color,
                rect,
                border_radius=12,
            )

            label_color = accent if is_user else muted
            screen.blit(
                small_font.render(
                    speaker,
                    True,
                    label_color,
                ),
                (rect.x + 15, rect.y + 8),
            )

            text_y = rect.y + 28
            for line in lines:
                screen.blit(
                    body_font.render(
                        line,
                        True,
                        text_color,
                    ),
                    (rect.x + 15, text_y),
                )
                text_y += 25

        screen.set_clip(clip_before)

        pygame.draw.rect(
            screen,
            input_panel,
            input_rect,
            border_radius=10,
        )

        border_color = accent if active else muted
        pygame.draw.rect(
            screen,
            border_color,
            input_rect,
            2,
            border_radius=10,
        )

        display_text = typed or "Type a message…"
        display_color = text_color if typed else muted
        rendered_input = body_font.render(
            display_text,
            True,
            display_color,
        )

        input_clip = screen.get_clip()
        screen.set_clip(input_rect.inflate(-18, -8))
        screen.blit(
            rendered_input,
            (input_rect.x + 12, input_rect.y + 15),
        )
        screen.set_clip(input_clip)

        pygame.draw.rect(
            screen,
            accent,
            send_rect,
            border_radius=10,
        )

        send_label = body_font.render(
            "Send",
            True,
            background,
        )

        screen.blit(
            send_label,
            (
                send_rect.centerx - send_label.get_width() // 2,
                send_rect.centery - send_label.get_height() // 2,
            ),
        )

        hint = "Enter sends • Mouse wheel scrolls • Esc unfocuses"
        screen.blit(
            small_font.render(hint, True, muted),
            (22, current_height - 18),
        )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line parser."""
    parser = argparse.ArgumentParser(
        description="Orbit AI - local Ollama assistant with Pygame UI."
    )

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--text",
        metavar="PROMPT",
        help="Answer one prompt and exit.",
    )
    mode.add_argument(
        "--cli",
        action="store_true",
        help="Start terminal chat.",
    )
    mode.add_argument(
        "--ui",
        action="store_true",
        help="Start the Pygame chat window (default).",
    )

    parser.add_argument(
        "--provider",
        choices=("offline", "ollama"),
        default="ollama",
        help="Response source (default: ollama).",
    )

    parser.add_argument(
        "--model",
        default="qwen3:4b",
        help="Ollama model name (default: qwen3:4b).",
    )

    parser.add_argument(
        "--base-url",
        default="http://localhost:11434",
        help="Ollama server URL.",
    )

    return parser


def main() -> int:
    """Run the selected application mode."""
    args = build_parser().parse_args()

    ai = AIEngine(
        provider=args.provider,
        model=args.model,
        base_url=args.base_url,
    )

    try:
        if args.text is not None:
            print(ai.respond(args.text))
        elif args.cli:
            run_terminal_chat(ai)
        else:
            run_pygame_chat(ai)
    except (AIProviderError, RuntimeError) as error:
        print(f"Error: {error}")
        return 1
    except KeyboardInterrupt:
        print("\nStopped.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
