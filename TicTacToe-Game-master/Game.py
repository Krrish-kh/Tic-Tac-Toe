"""
    TicTacToe Game is a board game of placing crosses and circles and is played as a multiplayer or as a computer vs player.
    Copyright (C) 2018  Rahul Gautham Putcha

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    For more details on contact, please visit https://rahulgputcha.com or email to rahulgautham95@gmail.com

"""

from __future__ import annotations

import random
import time
import tkinter as tk
from typing import Optional, Sequence


APP_TITLE = "Tic Tac Toe"
BOT_THINK_DELAY_MS = 900
BOT_MOVE_ANIM_MS = 70
BACKEND_TRACE_START_DELAY_MS = 650
BACKEND_TRACE_STEP_MS = 950
RESTART_SHORTCUT_WINDOW_SEC = 0.7
WIN_LENGTH = 3

WIN_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)

THEMES = {
    "Neural": {
        "bg": "#0d1117",
        "panel": "#141a22",
        "panel_alt": "#18202a",
        "card": "#1a222d",
        "card_hover": "#202a36",
        "tile": "#171f28",
        "tile_hover": "#1d2732",
        "tile_win": "#142a31",
        "border": "#2a3441",
        "shadow": "#070a0d",
        "text": "#eef2f6",
        "muted": "#93a0b1",
        "accent_cyan": "#82c9d6",
        "accent_green": "#7ac3a3",
        "accent_coral": "#c09a82",
        "accent_gold": "#b6ab7a",
        "accent_white": "#fbfcfd",
    },
    "Classic": {
        "bg": "#111418",
        "panel": "#171c22",
        "panel_alt": "#1c2129",
        "card": "#20262e",
        "card_hover": "#252c35",
        "tile": "#1d232b",
        "tile_hover": "#232a33",
        "tile_win": "#1c2a29",
        "border": "#2f3742",
        "shadow": "#080a0d",
        "text": "#f2f5f8",
        "muted": "#a6b0bb",
        "accent_cyan": "#88aeda",
        "accent_green": "#73c39a",
        "accent_coral": "#c39a7e",
        "accent_gold": "#b9ab6f",
        "accent_white": "#fcfcfd",
    },
    "Bank": {
        "bg": "#0d141d",
        "panel": "#151d29",
        "panel_alt": "#182231",
        "card": "#1a2431",
        "card_hover": "#202b3a",
        "tile": "#172130",
        "tile_hover": "#1d2737",
        "tile_win": "#143130",
        "border": "#304054",
        "shadow": "#060b11",
        "text": "#f2f6fb",
        "muted": "#9baab9",
        "accent_cyan": "#89add3",
        "accent_green": "#7fbea0",
        "accent_coral": "#c0a07c",
        "accent_gold": "#c9ba86",
        "accent_white": "#ffffff",
    },
    "Grocery": {
        "bg": "#101612",
        "panel": "#171f1a",
        "panel_alt": "#1c251f",
        "card": "#202a23",
        "card_hover": "#263029",
        "tile": "#1b241f",
        "tile_hover": "#212c26",
        "tile_win": "#18342d",
        "border": "#324237",
        "shadow": "#08100c",
        "text": "#f1f5f2",
        "muted": "#9fb0a4",
        "accent_cyan": "#89c7a9",
        "accent_green": "#a0ca7a",
        "accent_coral": "#c3a27c",
        "accent_gold": "#c4c883",
        "accent_white": "#fcfdfb",
    },
    "Cafe": {
        "bg": "#19120f",
        "panel": "#221913",
        "panel_alt": "#2a2019",
        "card": "#2c221a",
        "card_hover": "#352921",
        "tile": "#241b16",
        "tile_hover": "#2c221c",
        "tile_win": "#2a2318",
        "border": "#433326",
        "shadow": "#0c0907",
        "text": "#fcf7f1",
        "muted": "#c0ab9c",
        "accent_cyan": "#c2a38f",
        "accent_green": "#8fc2a0",
        "accent_coral": "#c89068",
        "accent_gold": "#d1bf79",
        "accent_white": "#fffdfb",
    },
    "Studio": {
        "bg": "#10131a",
        "panel": "#181d27",
        "panel_alt": "#1d2330",
        "card": "#202735",
        "card_hover": "#262d3d",
        "tile": "#1a2130",
        "tile_hover": "#222939",
        "tile_win": "#1b2d2c",
        "border": "#31394b",
        "shadow": "#090b11",
        "text": "#f4f7fb",
        "muted": "#a3adbf",
        "accent_cyan": "#8ca4d8",
        "accent_green": "#75c5a8",
        "accent_coral": "#c69a7b",
        "accent_gold": "#c4b07a",
        "accent_white": "#ffffff",
    },
}

THEME_ORDER = ("Neural", "Classic", "Bank", "Grocery", "Cafe", "Studio")

THEME_MARKERS = {
    "Neural": {"X": "network", "O": "core"},
    "Classic": {"X": "cross", "O": "ring"},
    "Bank": {"X": "bank", "O": "coin"},
    "Grocery": {"X": "cart", "O": "bag"},
    "Cafe": {"X": "cup", "O": "machine"},
    "Studio": {"X": "palette", "O": "mic"},
}

COLORS = {
    **THEMES["Neural"],
}

def other_symbol(symbol: str) -> str:
    return "O" if symbol == "X" else "X"


def build_app_icon(master: tk.Misc) -> tk.PhotoImage:
    """Build a small in-memory icon so the app feels finished without extra assets."""
    size = 64
    icon = tk.PhotoImage(master=master, width=size, height=size)

    rows = []
    for y in range(size):
        row = []
        for x in range(size):
            color = COLORS["bg"]

            if 6 <= x <= 57 and 6 <= y <= 57:
                color = COLORS["panel"]

            if 12 <= x <= 51 and 12 <= y <= 51:
                color = COLORS["card"]

            if 20 <= x <= 23 or 40 <= x <= 43:
                if 12 <= y <= 51:
                    color = COLORS["accent_cyan"]

            if 20 <= y <= 23 or 40 <= y <= 43:
                if 12 <= x <= 51:
                    color = COLORS["accent_cyan"]

            # X mark in the top-left cell.
            if 15 <= x <= 28 and 15 <= y <= 28:
                if abs((x - 15) - (y - 15)) <= 1 or abs((x - 28) - (y - 15)) <= 1:
                    color = COLORS["accent_coral"]

            # O mark in the bottom-right cell.
            dx = x - 48
            dy = y - 48
            dist_sq = dx * dx + dy * dy
            if 40 <= dist_sq <= 92:
                color = COLORS["accent_green"]

            row.append(color)
        rows.append(row)

    for y, row in enumerate(rows):
        icon.put("{" + " ".join(row) + "}", to=(0, y, size, y + 1))

    return icon


class TicTacToeApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(APP_TITLE)
        self.root.configure(bg=COLORS["bg"])
        self.root.resizable(True, True)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.minsize(980, 680)

        self.root.option_add("*Font", ("Segoe UI", 10))
        self.root.bind_all("<Escape>", self.on_close)
        self.root.bind_all("<KeyPress-r>", self._on_restart_key)
        self.root.bind_all("<KeyPress-R>", self._on_restart_key)
        self.root.bind_all("<KeyPress-n>", self._on_restart_button_key)
        self.root.bind_all("<KeyPress-N>", self._on_restart_button_key)
        self.root.bind_all("<space>", self._on_space_key)

        self.app_icon = build_app_icon(self.root)
        self.root.iconphoto(True, self.app_icon)

        self.theme_name = "Neural"
        self.theme_buttons: dict[str, tk.Button] = {}
        self.board_dim = 3
        self.win_length = WIN_LENGTH
        self.board = [""] * 9
        self.current_player = "X"
        self.ai_symbol: Optional[str] = None
        self.cpu_vs_cpu = False
        self.game_over = False
        self.last_move_index: Optional[int] = None
        self.hover_index: Optional[int] = None
        self.winning_cells: list[int] = []
        self.pending_ai_job: Optional[str] = None
        self.turn_banner_job: Optional[str] = None
        self.bot_move_job: Optional[str] = None
        self.bot_move_anim_step = 0
        self.bot_move_anim_index: Optional[int] = None
        self.bot_move_anim_total = 0
        self.backend_window: Optional[tk.Toplevel] = None
        self.backend_cells: list[tk.Label] = []
        self.backend_candidate_cells: list[tk.Label] = []
        self.backend_pipeline_labels: list[tk.Label] = []
        self.backend_log_lines: list[str] = []
        self.backend_last_analysis: Optional[dict[str, object]] = None
        self.backend_trace_data: Optional[dict[str, object]] = None
        self.backend_trace_steps: list[dict[str, object]] = []
        self.backend_trace_index = -1
        self.backend_trace_job: Optional[str] = None
        self.backend_trace_pending_move: Optional[int] = None
        self.backend_status_var = tk.StringVar(value="Idle")
        self.backend_detail_var = tk.StringVar(value="Waiting for the next AI turn.")
        self.backend_move_var = tk.StringVar(value="No move selected yet.")
        self.backend_phase_var = tk.StringVar(value="Board synchronized.")
        self.backend_board_var = tk.StringVar(value="1 2 3 / 4 5 6 / 7 8 9")
        self.backend_board_state_var = tk.StringVar(value='["", "", "", "", "", "", "", "", ""]')
        self.backend_structure_var = tk.StringVar(value="board = []\navailable = []\nsearch_stats = {}")
        self.backend_candidates_var = tk.StringVar(value="current_candidates = []")
        self.backend_available_var = tk.StringVar(value="available_moves = []")
        self.backend_trace_steps_var = tk.StringVar(value="trace_steps = 0")
        self.backend_mode_state_var = tk.StringVar(value="Human vs Human")
        self.backend_turn_state_var = tk.StringVar(value="X")
        self.backend_alpha_var = tk.StringVar(value="alpha = -")
        self.backend_beta_var = tk.StringVar(value="beta = -")
        self.backend_nodes_var = tk.StringVar(value="nodes = 0")
        self.backend_prunes_var = tk.StringVar(value="prunes = 0")
        self.backend_best_var = tk.StringVar(value="best = -")
        self.backend_choice_var = tk.StringVar(value="choice = pending")
        self.backend_eval_var = tk.StringVar(value="evaluating: none")
        self.backend_progress_var = tk.StringVar(value="0 / 0")
        self.scores = {"X": 0, "O": 0, "Draw": 0}
        self._restart_shortcut_deadline = 0.0

        self.status_var = tk.StringVar()
        self.mode_var = tk.StringVar()
        self.control_var = tk.StringVar()
        self.turn_banner_var = tk.StringVar()
        self.player1_state_var = tk.StringVar()
        self.player2_state_var = tk.StringVar()
        self.bot_state_var = tk.StringVar()
        self.score_x_var = tk.StringVar()
        self.score_o_var = tk.StringVar()
        self.score_draw_var = tk.StringVar()

        self.root.update_idletasks()
        self._configure_board_metrics()
        self.win_lines = WIN_LINES

        self._build_ui()
        self.maximize_window()
        self.new_game()
        self.open_backend_window()

    def _build_tile_positions(self) -> list[tuple[int, int, int, int]]:
        positions = []
        start_x = self.grid_origin
        start_y = self.grid_origin
        for row in range(self.board_dim):
            for col in range(self.board_dim):
                x1 = start_x + col * (self.tile_size + self.tile_gap)
                y1 = start_y + row * (self.tile_size + self.tile_gap)
                x2 = x1 + self.tile_size
                y2 = y1 + self.tile_size
                positions.append((x1, y1, x2, y2))
        return positions

    def _configure_board_metrics(self) -> None:
        self.board_size = self._compute_board_size()
        self.tile_gap = 12
        self.board_padding = 14
        self.tile_size = (self.board_size - (2 * self.board_padding) - (2 * self.tile_gap)) // self.board_dim
        self.grid_size = self.tile_size * self.board_dim + self.tile_gap * (self.board_dim - 1)
        self.grid_origin = (self.board_size - self.grid_size) // 2
        self.tile_positions = self._build_tile_positions()

    def _build_ui(self) -> None:
        outer = tk.Frame(self.root, bg=COLORS["bg"])
        outer.pack(fill="both", expand=True, padx=24, pady=20)

        header = tk.Frame(outer, bg=COLORS["bg"])
        header.pack(fill="x", pady=(0, 18))

        badge = tk.Frame(header, bg=COLORS["panel"], highlightthickness=1, highlightbackground=COLORS["border"])
        badge.pack(side="left", padx=(0, 16))
        icon_label = tk.Label(
            badge,
            image=self.app_icon,
            bg=COLORS["panel"],
            bd=0,
        )
        icon_label.pack(padx=12, pady=12)

        title_wrap = tk.Frame(header, bg=COLORS["bg"])
        title_wrap.pack(side="left", fill="x", expand=True)

        tk.Label(
            title_wrap,
            text="Tic Tac Toe",
            bg=COLORS["bg"],
            fg=COLORS["text"],
            font=("Segoe UI Semibold", 28, "bold"),
        ).pack(anchor="w")

        tk.Label(
            title_wrap,
            text="A refined desktop edition with local play and a computer opponent.",
            bg=COLORS["bg"],
            fg=COLORS["muted"],
            font=("Segoe UI", 11),
        ).pack(anchor="w", pady=(4, 0))

        self.mode_badge = tk.Label(
            header,
            textvariable=self.mode_var,
            bg=COLORS["panel"],
            fg=COLORS["accent_cyan"],
            font=("Segoe UI Semibold", 10),
            padx=14,
            pady=8,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
        )
        self.mode_badge.pack(side="right")

        body = tk.Frame(outer, bg=COLORS["bg"])
        body.pack(fill="both", expand=True)

        left = tk.Frame(body, bg=COLORS["bg"])
        left.pack(side="left", fill="both", expand=True, padx=(0, 18))

        board_header = tk.Frame(left, bg=COLORS["bg"])
        board_header.pack(fill="x", pady=(0, 10))
        tk.Label(
            board_header,
            text="Playfield",
            bg=COLORS["bg"],
            fg=COLORS["text"],
            font=("Segoe UI Semibold", 17, "bold"),
        ).pack(anchor="w")
        tk.Label(
            board_header,
            text="Click a tile, press R for a new game, or Space to switch the computer on or off.",
            bg=COLORS["bg"],
            fg=COLORS["muted"],
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(2, 0))

        self.theme_card, self.theme_card_content = self._make_card(left, "Themes")
        self.theme_card.pack(fill="x", pady=(0, 14))
        theme_row = tk.Frame(self.theme_card_content, bg=COLORS["panel"])
        theme_row.pack(fill="x")
        self.theme_buttons = {}
        for theme_name in THEME_ORDER:
            button = self._make_theme_chip(theme_row, theme_name)
            button.pack(side="left", padx=(0, 8))
            self.theme_buttons[theme_name] = button

        self.turn_banner_frame = tk.Frame(
            left,
            bg=COLORS["panel"],
            highlightthickness=1,
            highlightbackground=COLORS["border"],
        )
        self.turn_banner_frame.pack(fill="x", pady=(0, 14))
        self.turn_banner_label = tk.Label(
            self.turn_banner_frame,
            textvariable=self.turn_banner_var,
            bg=COLORS["panel"],
            fg=COLORS["accent_cyan"],
            font=("Segoe UI Semibold", 16, "bold"),
            pady=10,
        )
        self.turn_banner_label.pack(fill="x")

        self.board_shell = tk.Frame(
            left,
            bg=COLORS["panel"],
            highlightthickness=1,
            highlightbackground=COLORS["border"],
        )
        self.board_shell.pack(fill="both", expand=True)

        self.board_canvas = tk.Canvas(
            self.board_shell,
            width=self.board_size,
            height=self.board_size,
            bg=COLORS["panel"],
            highlightthickness=0,
            bd=0,
            cursor="hand2",
        )
        self.board_canvas.pack(expand=True, padx=18, pady=18)
        self.board_canvas.bind("<Motion>", self.on_board_motion)
        self.board_canvas.bind("<Leave>", self.on_board_leave)
        self.board_canvas.bind("<Button-1>", self.on_board_click)

        right = tk.Frame(body, bg=COLORS["bg"], width=280)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        self.status_card, self.status_card_content = self._make_card(right, "Match Status")
        self.status_card.pack(fill="x", pady=(0, 14))
        self.status_label = tk.Label(
            self.status_card_content,
            textvariable=self.status_var,
            bg=COLORS["panel"],
            fg=COLORS["text"],
            wraplength=228,
            justify="left",
            font=("Segoe UI Semibold", 15, "bold"),
            pady=2,
        )
        self.status_label.pack(anchor="w")

        self.status_detail = tk.Label(
            self.status_card_content,
            textvariable=self.control_var,
            bg=COLORS["panel"],
            fg=COLORS["muted"],
            wraplength=228,
            justify="left",
            font=("Segoe UI", 10),
        )
        self.status_detail.pack(anchor="w", pady=(8, 0))

        self.score_card, self.score_card_content = self._make_card(right, "Scoreboard")
        self.score_card.pack(fill="x", pady=(0, 14))
        scores = tk.Frame(self.score_card_content, bg=COLORS["panel"])
        scores.pack(fill="x")
        self._make_score_chip(scores, "X", self.score_x_var, COLORS["accent_coral"]).pack(side="left", expand=True, fill="x", padx=(0, 8))
        self._make_score_chip(scores, "O", self.score_o_var, COLORS["accent_cyan"]).pack(side="left", expand=True, fill="x")
        self._make_score_chip(scores, "Draw", self.score_draw_var, COLORS["accent_green"]).pack(side="left", expand=True, fill="x", padx=(8, 0))

        self.players_card, self.players_card_content = self._make_card(right, "Players")
        self.players_card.pack(fill="x", pady=(0, 14))
        self._make_player_row(self.players_card_content, "Player 1", self.player1_state_var, COLORS["accent_coral"]).pack(fill="x", pady=(0, 8))
        self._make_player_row(self.players_card_content, "Player 2", self.player2_state_var, COLORS["accent_cyan"]).pack(fill="x", pady=(0, 8))
        self._make_player_row(self.players_card_content, "Computer", self.bot_state_var, COLORS["accent_green"]).pack(fill="x")

        self.controls_card, self.controls_card_content = self._make_card(right, "Controls")
        self.controls_card.pack(fill="x", pady=(0, 14))
        controls = self.controls_card_content

        self.new_game_button = self._make_button(controls, "New Game", self.trigger_new_game, COLORS["accent_green"], COLORS["card_hover"])
        self.new_game_button.pack(fill="x", pady=(0, 10))

        self.ai_button = self._make_button(controls, "Computer: Off", self.toggle_ai_mode, COLORS["accent_cyan"], COLORS["card_hover"])
        self.ai_button.pack(fill="x", pady=(0, 10))

        self.cpu_button = self._make_button(controls, "Computer vs Computer: Off", self.toggle_cpu_vs_cpu_mode, COLORS["accent_gold"], COLORS["card_hover"])
        self.cpu_button.pack(fill="x", pady=(0, 10))

        self.backend_button = self._make_button(controls, "Backend Window", self.toggle_backend_window, COLORS["accent_gold"], COLORS["card_hover"])
        self.backend_button.pack(fill="x", pady=(0, 10))

        self.exit_button = self._make_button(controls, "Exit", self.on_close, COLORS["accent_coral"], COLORS["card_hover"])
        self.exit_button.pack(fill="x")

        self.hint_card, self.hint_card_content = self._make_card(right, "Shortcuts")
        self.hint_card.pack(fill="x")
        hint_text = (
            "R or N  -  restart the board\n"
            "Space   -  toggle computer control\n"
            "R + Space - computer vs computer\n"
            "Esc     -  close the app"
        )
        tk.Label(
            self.hint_card_content,
            text=hint_text,
            bg=COLORS["panel"],
            fg=COLORS["muted"],
            justify="left",
            font=("Consolas", 10),
        ).pack(anchor="w")

        self.footer = tk.Label(
            outer,
            text="Built with Tkinter for a polished desktop feel.",
            bg=COLORS["bg"],
            fg=COLORS["muted"],
            font=("Segoe UI", 9),
        )
        self.footer.pack(anchor="e", pady=(14, 0))

    def _make_card(self, parent: tk.Widget, title: str) -> tuple[tk.Frame, tk.Frame]:
        card = tk.Frame(
            parent,
            bg=COLORS["panel"],
            highlightthickness=1,
            highlightbackground=COLORS["border"],
        )
        tk.Label(
            card,
            text=title.upper(),
            bg=COLORS["panel"],
            fg=COLORS["muted"],
            font=("Segoe UI Semibold", 9),
            anchor="w",
        ).pack(fill="x", padx=16, pady=(14, 6))

        content = tk.Frame(card, bg=COLORS["panel"])
        content.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        return card, content

    def _make_score_chip(self, parent: tk.Widget, label: str, value_var: tk.StringVar, accent: str) -> tk.Frame:
        chip = tk.Frame(
            parent,
            bg=COLORS["card"],
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            padx=0,
            pady=0,
        )
        tk.Label(
            chip,
            text=label,
            bg=COLORS["card"],
            fg=accent,
            font=("Segoe UI Semibold", 11, "bold"),
        ).pack(anchor="center", pady=(12, 0))
        tk.Label(
            chip,
            textvariable=value_var,
            bg=COLORS["card"],
            fg=COLORS["text"],
            font=("Segoe UI Semibold", 20, "bold"),
        ).pack(anchor="center", pady=(2, 12))
        return chip

    def _make_player_row(self, parent: tk.Widget, label: str, value_var: tk.StringVar, accent: str) -> tk.Frame:
        row = tk.Frame(
            parent,
            bg=COLORS["card"],
            highlightthickness=1,
            highlightbackground=COLORS["border"],
        )
        dot = tk.Canvas(row, width=16, height=16, bg=COLORS["card"], highlightthickness=0, bd=0)
        dot.create_oval(3, 3, 13, 13, fill=accent, outline="")
        dot.pack(side="left", padx=(12, 8), pady=12)

        text_wrap = tk.Frame(row, bg=COLORS["card"])
        text_wrap.pack(side="left", fill="x", expand=True, pady=10)
        tk.Label(
            text_wrap,
            text=label,
            bg=COLORS["card"],
            fg=COLORS["text"],
            font=("Segoe UI Semibold", 11, "bold"),
            anchor="w",
        ).pack(anchor="w")
        tk.Label(
            text_wrap,
            textvariable=value_var,
            bg=COLORS["card"],
            fg=COLORS["muted"],
            font=("Segoe UI", 9),
            anchor="w",
        ).pack(anchor="w", pady=(2, 0))
        return row

    def _make_theme_chip(self, parent: tk.Widget, theme_name: str) -> tk.Button:
        palette = THEMES[theme_name]
        selected = theme_name == self.theme_name
        border = palette["accent_gold"] if selected else palette["border"]
        button = tk.Button(
            parent,
            text=theme_name,
            command=lambda name=theme_name: self.set_theme(name),
            bg=palette["card"],
            fg=palette["text"],
            activebackground=palette["card_hover"],
            activeforeground=palette["text"],
            relief="flat",
            bd=0,
            highlightthickness=2 if selected else 1,
            highlightbackground=border,
            highlightcolor=border,
            cursor="hand2",
            font=("Segoe UI Semibold", 10, "bold"),
            padx=12,
            pady=8,
        )
        return button

    def _make_button(
        self,
        parent: tk.Widget,
        text: str,
        command,
        accent: str,
        hover: str,
    ) -> tk.Button:
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=accent,
            fg=COLORS["bg"],
            activebackground=hover,
            activeforeground=COLORS["bg"],
            relief="flat",
            bd=0,
            highlightthickness=0,
            font=("Segoe UI Semibold", 11, "bold"),
            cursor="hand2",
            pady=10,
        )

        def on_enter(_event: tk.Event) -> None:
            button.configure(bg=hover)

        def on_leave(_event: tk.Event) -> None:
            button.configure(bg=accent)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        return button

    def _compute_board_size(self) -> int:
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        usable_width = screen_width - 560
        usable_height = screen_height - 380
        return max(360, min(420, usable_width, usable_height))

    def maximize_window(self) -> None:
        try:
            self.root.state("zoomed")
        except tk.TclError:
            self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")

    def toggle_backend_window(self, event: Optional[tk.Event] = None) -> None:
        del event
        if self.backend_window is not None and self.backend_window.winfo_exists():
            self.close_backend_window()
        else:
            self.open_backend_window()

    def open_backend_window(self) -> None:
        if self.backend_window is not None and self.backend_window.winfo_exists():
            self.refresh_backend_window()
            return

        win = tk.Toplevel(self.root)
        win.title("Backend Simulation")
        win.configure(bg=COLORS["bg"])
        win.geometry("520x780+40+40")
        win.minsize(480, 700)
        win.protocol("WM_DELETE_WINDOW", self.close_backend_window)
        win.transient(self.root)
        self.backend_window = win
        self.backend_cells = []
        self.backend_candidate_cells = []
        self.backend_pipeline_labels = []

        header = tk.Frame(win, bg=COLORS["bg"])
        header.pack(fill="x", padx=16, pady=(16, 10))
        tk.Label(header, text="Backend Simulation", bg=COLORS["bg"], fg=COLORS["text"], font=("Segoe UI Semibold", 20, "bold")).pack(anchor="w")
        tk.Label(header, text="Live search debugger for board storage, candidate scoring, and move selection.", bg=COLORS["bg"], fg=COLORS["muted"], font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 0))

        body_shell = tk.Frame(win, bg=COLORS["bg"])
        body_shell.pack(fill="both", expand=True, padx=0, pady=0)
        body_canvas = tk.Canvas(body_shell, bg=COLORS["bg"], highlightthickness=0, bd=0)
        body_scroll = tk.Scrollbar(body_shell, orient="vertical", command=body_canvas.yview)
        body_canvas.configure(yscrollcommand=body_scroll.set)
        body_scroll.pack(side="right", fill="y")
        body_canvas.pack(side="left", fill="both", expand=True)
        body_frame = tk.Frame(body_canvas, bg=COLORS["bg"])
        body_window = body_canvas.create_window((0, 0), window=body_frame, anchor="nw")

        def _sync_scroll_region(event: tk.Event) -> None:
            body_canvas.configure(scrollregion=body_canvas.bbox("all"))
            body_canvas.itemconfigure(body_window, width=event.width)

        body_frame.bind("<Configure>", lambda event: body_canvas.configure(scrollregion=body_canvas.bbox("all")))
        body_canvas.bind("<Configure>", _sync_scroll_region)

        meta = tk.Frame(body_frame, bg=COLORS["panel"], highlightthickness=1, highlightbackground=COLORS["border"])
        meta.pack(fill="x", padx=16, pady=(0, 12))
        tk.Label(meta, textvariable=self.backend_phase_var, bg=COLORS["panel"], fg=COLORS["accent_cyan"], font=("Segoe UI Semibold", 10), padx=14, pady=10).pack(anchor="w")
        tk.Label(meta, textvariable=self.backend_status_var, bg=COLORS["panel"], fg=COLORS["text"], font=("Segoe UI Semibold", 14, "bold"), padx=14).pack(anchor="w")
        tk.Label(meta, textvariable=self.backend_detail_var, bg=COLORS["panel"], fg=COLORS["muted"], font=("Segoe UI", 10), wraplength=500, justify="left", padx=14, pady=4).pack(anchor="w")
        tk.Label(meta, textvariable=self.backend_progress_var, bg=COLORS["panel"], fg=COLORS["accent_gold"], font=("Consolas", 10), padx=14).pack(anchor="w", pady=(2, 10))

        pipeline_card = tk.Frame(body_frame, bg=COLORS["panel"], highlightthickness=1, highlightbackground=COLORS["border"])
        pipeline_card.pack(fill="x", padx=16, pady=(0, 12))
        tk.Label(pipeline_card, text="DECISION PIPELINE", bg=COLORS["panel"], fg=COLORS["muted"], font=("Segoe UI Semibold", 9), anchor="w").pack(fill="x", padx=14, pady=(12, 8))
        pipeline_wrap = tk.Frame(pipeline_card, bg=COLORS["panel"])
        pipeline_wrap.pack(fill="x", padx=14, pady=(0, 14))
        for step in ("Capture board", "Predict candidates", "Score branches", "Prune tree", "Choose move", "Apply move"):
            row = tk.Frame(pipeline_wrap, bg=COLORS["panel"])
            row.pack(fill="x", pady=2)
            lamp = tk.Label(row, text="●", bg=COLORS["panel"], fg=COLORS["muted"], font=("Segoe UI", 10, "bold"), width=2)
            lamp.pack(side="left")
            label = tk.Label(row, text=step, bg=COLORS["panel"], fg=COLORS["muted"], font=("Segoe UI Semibold", 10))
            label.pack(side="left")
            self.backend_pipeline_labels.append(label)

        board_card = tk.Frame(body_frame, bg=COLORS["panel"], highlightthickness=1, highlightbackground=COLORS["border"])
        board_card.pack(fill="x", padx=16, pady=(0, 12))
        tk.Label(board_card, text="LIVE STRUCTURES", bg=COLORS["panel"], fg=COLORS["muted"], font=("Segoe UI Semibold", 9), anchor="w").pack(fill="x", padx=14, pady=(12, 6))
        tk.Label(board_card, textvariable=self.backend_structure_var, bg=COLORS["panel"], fg=COLORS["accent_cyan"], font=("Consolas", 9), anchor="w", justify="left", wraplength=470).pack(fill="x", padx=14)
        tk.Label(board_card, textvariable=self.backend_available_var, bg=COLORS["panel"], fg=COLORS["accent_gold"], font=("Consolas", 9), anchor="w", justify="left", wraplength=470).pack(fill="x", padx=14, pady=(4, 0))
        tk.Label(board_card, textvariable=self.backend_trace_steps_var, bg=COLORS["panel"], fg=COLORS["muted"], font=("Consolas", 9), anchor="w", justify="left", wraplength=470).pack(fill="x", padx=14, pady=(4, 0))
        board_grid = tk.Frame(board_card, bg=COLORS["panel"])
        board_grid.pack(padx=14, pady=(10, 14))
        for r in range(3):
            for c in range(3):
                cell = tk.Label(board_grid, text="", width=8, height=3, bg=COLORS["card"], fg=COLORS["text"], font=("Segoe UI Semibold", 12, "bold"), relief="flat", bd=0, highlightthickness=1, highlightbackground=COLORS["border"], justify="center")
                cell.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")
                board_grid.grid_columnconfigure(c, weight=1)
                board_grid.grid_rowconfigure(r, weight=1)
                self.backend_cells.append(cell)

        stats_card = tk.Frame(body_frame, bg=COLORS["panel"], highlightthickness=1, highlightbackground=COLORS["border"])
        stats_card.pack(fill="x", padx=16, pady=(0, 12))
        tk.Label(stats_card, text="SEARCH STATE", bg=COLORS["panel"], fg=COLORS["muted"], font=("Segoe UI Semibold", 9), anchor="w").pack(fill="x", padx=14, pady=(12, 8))
        stats_grid = tk.Frame(stats_card, bg=COLORS["panel"])
        stats_grid.pack(fill="x", padx=14, pady=(0, 14))
        stat_items = [
            ("Mode", self.backend_mode_state_var, COLORS["accent_coral"]),
            ("Turn", self.backend_turn_state_var, COLORS["accent_cyan"]),
            ("Alpha", self.backend_alpha_var, COLORS["accent_green"]),
            ("Beta", self.backend_beta_var, COLORS["accent_gold"]),
            ("Nodes", self.backend_nodes_var, COLORS["accent_white"]),
            ("Prunes", self.backend_prunes_var, COLORS["accent_white"]),
            ("Best", self.backend_best_var, COLORS["accent_white"]),
            ("Choice", self.backend_choice_var, COLORS["accent_white"]),
        ]
        for index, (label_text, var, accent) in enumerate(stat_items):
            cell = tk.Frame(stats_grid, bg=COLORS["card"], highlightthickness=1, highlightbackground=COLORS["border"])
            cell.grid(row=index // 2, column=index % 2, sticky="nsew", padx=(0, 8) if index % 2 == 0 else (8, 0), pady=6)
            tk.Label(cell, text=label_text.upper(), bg=COLORS["card"], fg=COLORS["muted"], font=("Segoe UI Semibold", 8), anchor="w").pack(fill="x", padx=12, pady=(10, 2))
            tk.Label(cell, textvariable=var, bg=COLORS["card"], fg=accent, font=("Segoe UI Semibold", 12, "bold"), anchor="w").pack(fill="x", padx=12, pady=(0, 10))
        stats_grid.grid_columnconfigure(0, weight=1)
        stats_grid.grid_columnconfigure(1, weight=1)

        candidate_card = tk.Frame(body_frame, bg=COLORS["panel"], highlightthickness=1, highlightbackground=COLORS["border"])
        candidate_card.pack(fill="x", padx=16, pady=(0, 12))
        tk.Label(candidate_card, text="CANDIDATE WEIGHTS", bg=COLORS["panel"], fg=COLORS["muted"], font=("Segoe UI Semibold", 9), anchor="w").pack(fill="x", padx=14, pady=(12, 8))
        tk.Label(candidate_card, textvariable=self.backend_eval_var, bg=COLORS["panel"], fg=COLORS["text"], font=("Segoe UI Semibold", 11), anchor="w", justify="left", wraplength=470).pack(fill="x", padx=14, pady=(0, 10))
        candidate_grid = tk.Frame(candidate_card, bg=COLORS["panel"])
        candidate_grid.pack(padx=14, pady=(0, 14))
        for r in range(3):
            for c in range(3):
                cell = tk.Label(candidate_grid, text="", width=8, height=3, bg=COLORS["card"], fg=COLORS["text"], font=("Consolas", 10, "bold"), relief="flat", bd=0, highlightthickness=1, highlightbackground=COLORS["border"], justify="center")
                cell.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")
                candidate_grid.grid_columnconfigure(c, weight=1)
                candidate_grid.grid_rowconfigure(r, weight=1)
                self.backend_candidate_cells.append(cell)

        move_card = tk.Frame(body_frame, bg=COLORS["panel"], highlightthickness=1, highlightbackground=COLORS["border"])
        move_card.pack(fill="both", expand=True, padx=16, pady=(0, 12))
        tk.Label(move_card, text="TRACE LOG", bg=COLORS["panel"], fg=COLORS["muted"], font=("Segoe UI Semibold", 9), anchor="w").pack(fill="x", padx=14, pady=(12, 8))
        tk.Label(move_card, textvariable=self.backend_move_var, bg=COLORS["panel"], fg=COLORS["text"], font=("Segoe UI Semibold", 11, "bold"), wraplength=470, justify="left", padx=14).pack(anchor="w")
        tk.Label(move_card, textvariable=self.backend_board_var, bg=COLORS["panel"], fg=COLORS["accent_cyan"], font=("Consolas", 9), anchor="w", justify="left", wraplength=470, padx=14).pack(anchor="w", pady=(8, 0))
        self.backend_log_text = tk.Text(move_card, height=8, bg=COLORS["panel"], fg=COLORS["muted"], insertbackground=COLORS["muted"], relief="flat", bd=0, highlightthickness=0, wrap="word", font=("Consolas", 9))
        self.backend_log_text.pack(fill="both", expand=True, padx=14, pady=(10, 14))
        self.backend_log_text.configure(state="disabled")

        footer = tk.Frame(body_frame, bg=COLORS["bg"])
        footer.pack(fill="x", padx=16, pady=(0, 16))
        tk.Label(footer, text="This window exposes the backend as a live, visual debugger.", bg=COLORS["bg"], fg=COLORS["muted"], font=("Segoe UI", 9)).pack(anchor="w")

        self._append_backend_log("Backend monitor opened.")
        self.refresh_backend_window()

    def close_backend_window(self) -> None:
        self._clear_backend_trace()
        if self.backend_window is not None:
            try:
                self.backend_window.destroy()
            finally:
                self.backend_window = None
                self.backend_cells = []
                self.backend_candidate_cells = []
                self.backend_pipeline_labels = []

    def _on_restart_key(self, event: Optional[tk.Event] = None) -> str:
        del event
        self._restart_shortcut_deadline = time.monotonic() + RESTART_SHORTCUT_WINDOW_SEC
        self.new_game()
        return "break"

    def _on_restart_button_key(self, event: Optional[tk.Event] = None) -> str:
        del event
        self._restart_shortcut_deadline = 0.0
        self.trigger_new_game()
        return "break"

    def _on_space_key(self, event: Optional[tk.Event] = None) -> str:
        del event
        now = time.monotonic()
        if now <= self._restart_shortcut_deadline:
            self._restart_shortcut_deadline = 0.0
            self.toggle_cpu_vs_cpu_mode()
        else:
            self.toggle_ai_mode()
        return "break"

    def trigger_new_game(self, event: Optional[tk.Event] = None) -> None:
        del event
        self._restart_shortcut_deadline = 0.0
        self.new_game()

    def _clear_backend_trace(self) -> None:
        if self.backend_trace_job is not None:
            self.root.after_cancel(self.backend_trace_job)
            self.backend_trace_job = None
        self.backend_trace_data = None
        self.backend_trace_steps = []
        self.backend_trace_index = -1
        self.backend_trace_pending_move = None

    def _update_backend_pipeline(self, active_index: int, done_index: Optional[int] = None) -> None:
        labels = self.backend_pipeline_labels
        if not labels:
            return
        active_color = COLORS["accent_cyan"]
        done_color = COLORS["accent_green"]
        idle_color = COLORS["muted"]
        for index, label in enumerate(labels):
            if done_index is not None and index <= done_index:
                label.configure(fg=done_color)
            elif index == active_index:
                label.configure(fg=active_color)
            else:
                label.configure(fg=idle_color)

    def _format_board_state(self, board: Sequence[str]) -> str:
        rows = []
        for row in range(3):
            cells = []
            for col in range(3):
                index = row * 3 + col
                value = board[index] if board[index] else str(index + 1)
                cells.append(f"{index + 1}:{value}")
            rows.append("  ".join(cells))
        return " | ".join(rows)

    def _format_board_vector(self, board: Sequence[str]) -> str:
        return "[" + ", ".join(repr(cell) if cell else '""' for cell in board) + "]"

    def _format_available_moves(self, moves: Sequence[int]) -> str:
        if not moves:
            return "available_moves = []"
        return "available_moves = [" + ", ".join(str(move + 1) for move in moves) + "]"

    def _format_candidate_snapshot(self, candidates: Sequence[dict[str, object]]) -> str:
        if not candidates:
            return "current_candidates = []"
        parts = []
        for item in candidates:
            move = int(item.get("move", -1)) + 1
            score = item.get("score", "-")
            nodes = item.get("nodes", 0)
            prunes = item.get("prunes", 0)
            parts.append(f"{move}:{score} n{nodes} p{prunes}")
        return "current_candidates = [" + "; ".join(parts) + "]"

    def _update_backend_structure_vars(
        self,
        *,
        board: Sequence[str],
        available: Sequence[int],
        candidates: Sequence[dict[str, object]],
        nodes: int,
        prunes: int,
        steps: int,
        choice: str,
        best: str,
    ) -> None:
        self.backend_board_state_var.set(self._format_board_vector(board))
        self.backend_board_var.set(self._format_board_vector(board))
        self.backend_available_var.set(self._format_available_moves(available))
        self.backend_candidates_var.set(self._format_candidate_snapshot(candidates))
        self.backend_trace_steps_var.set(f"trace_steps = {steps}")
        self.backend_structure_var.set(
            "board = "
            + self._format_board_vector(board)
            + "\n"
            + self._format_available_moves(available)
            + "\n"
            + self._format_candidate_snapshot(candidates)
            + f"\nsearch_stats = {{nodes: {nodes}, prunes: {prunes}}}"
            + f"\ntrace_steps = {steps}"
            + f"\ncurrent_choice = {choice}"
            + f"\ncurrent_best = {best}"
        )

    def _set_backend_trace(self, trace: dict[str, object], chosen_move: int) -> None:
        self.backend_trace_data = trace
        self.backend_trace_pending_move = chosen_move
        self.backend_trace_steps = list(trace.get("steps", []))
        self.backend_trace_index = -1
        self.backend_mode_state_var.set(str(trace.get("mode", self.backend_mode_state_var.get())))
        self.backend_turn_state_var.set(str(trace.get("turn", self.current_player)))
        available = list(trace.get("available", []))
        candidates = list(trace.get("current_candidates", []))
        if "board" in trace:
            self.backend_board_state_var.set(self._format_board_state(trace["board"]))
            self.backend_board_var.set(self._format_board_vector(trace["board"]))
        self.backend_available_var.set(self._format_available_moves(available))
        self.backend_candidates_var.set(self._format_candidate_snapshot(candidates))
        self.backend_trace_steps_var.set(f"trace_steps = {len(self.backend_trace_steps)}")
        self.backend_structure_var.set(
            "board = "
            + self._format_board_vector(trace.get("board", self.board))
            + "\n"
            + self._format_available_moves(available)
            + "\n"
            + self._format_candidate_snapshot(candidates)
            + f"\nsearch_stats = {{nodes: {trace.get('nodes', 0)}, prunes: {trace.get('prunes', 0)}}}"
            + f"\ntrace_steps = {len(self.backend_trace_steps)}"
            + f"\ncurrent_choice = pending"
            + f"\ncurrent_best = pending"
        )
        self.backend_alpha_var.set("alpha = -1000")
        self.backend_beta_var.set("beta = 1000")
        self.backend_nodes_var.set("nodes = 0")
        self.backend_prunes_var.set("prunes = 0")
        self.backend_best_var.set("best = pending")
        self.backend_choice_var.set("choice = pending")
        self.backend_eval_var.set("evaluating: search tree")
        self.backend_progress_var.set(f"0 / {len(self.backend_trace_steps)}")
        self.backend_trace_job = self.root.after(BACKEND_TRACE_START_DELAY_MS, self._advance_backend_trace)

    def _advance_backend_trace(self) -> None:
        if self.backend_trace_data is None:
            self.backend_trace_job = None
            return

        self.backend_trace_index += 1
        steps = self.backend_trace_steps
        if self.backend_trace_index >= len(steps):
            self.backend_trace_job = None
            chosen = self.backend_trace_pending_move
            if chosen is not None:
                self.backend_phase_var.set("Apply move")
                self.backend_status_var.set(f"Committing move {chosen + 1}")
                self.backend_detail_var.set("The selected branch is now applied to the live board.")
                self.backend_move_var.set(f"Selected move {chosen + 1} has been committed.")
                self.backend_choice_var.set(f"choice = {chosen + 1}")
                self.backend_progress_var.set(f"{len(steps)} / {len(steps)}")
                self._update_backend_pipeline(5, 5)
                self.refresh_backend_window()
                self.backend_trace_data = None
                self.backend_trace_steps = []
                self.backend_trace_index = -1
                self.backend_trace_pending_move = None
                self.make_move(chosen, by_ai=True)
                self._start_bot_move_animation(chosen)
            return

        step = steps[self.backend_trace_index]
        stage = str(step.get("stage", "scan"))
        stage_index_map = {
            "capture": 0,
            "predict": 1,
            "score": 2,
            "prune": 3,
            "choose": 4,
            "commit": 5,
        }
        stage_index = stage_index_map.get(stage, 1)
        self._update_backend_pipeline(stage_index, stage_index - 1 if stage_index > 0 else None)

        self.backend_phase_var.set(str(step.get("phase", "Search")))
        self.backend_status_var.set(str(step.get("status", "Running search...")))
        self.backend_detail_var.set(str(step.get("detail", "")))
        self.backend_move_var.set(str(step.get("move_text", self.backend_move_var.get())))
        self.backend_progress_var.set(f"{self.backend_trace_index + 1} / {len(steps)}")

        if "alpha" in step:
            self.backend_alpha_var.set(f"alpha = {step['alpha']}")
        if "beta" in step:
            self.backend_beta_var.set(f"beta = {step['beta']}")
        if "nodes" in step:
            self.backend_nodes_var.set(f"nodes = {step['nodes']}")
        if "prunes" in step:
            self.backend_prunes_var.set(f"prunes = {step['prunes']}")
        if "best" in step:
            self.backend_best_var.set(f"best = {step['best']}")
        if "choice" in step:
            self.backend_choice_var.set(f"choice = {step['choice']}")
        if "eval" in step:
            self.backend_eval_var.set(str(step["eval"]))
        if "board" in step:
            self.backend_board_state_var.set(self._format_board_state(step["board"]))
            self.backend_board_var.set(self._format_board_vector(step["board"]))
        if "candidates" in step:
            self._render_backend_candidates(step["candidates"], step.get("focus"))
        if "trace_line" in step:
            self._append_backend_log(str(step["trace_line"]))

        self.refresh_backend_window()
        self.backend_trace_job = self.root.after(BACKEND_TRACE_STEP_MS, self._advance_backend_trace)

    def _render_backend_candidates(self, candidates: Sequence[dict[str, object]], focus: Optional[int] = None) -> None:
        candidate_map = {int(item["move"]): item for item in candidates}
        for index, cell in enumerate(self.backend_candidate_cells):
            item = candidate_map.get(index)
            symbol = self.board[index]
            if symbol:
                text = f"{index + 1}\nLOCKED\n{symbol}"
                fg = COLORS["muted"]
                bg = COLORS["card"]
            elif item is not None:
                score = item.get("score", "?")
                nodes = item.get("nodes", 0)
                prunes = item.get("prunes", 0)
                if isinstance(score, (int, float)):
                    score_text = f"{score:+d}"
                    fg = COLORS["accent_green"] if score > 0 else COLORS["accent_coral"] if score < 0 else COLORS["accent_cyan"]
                else:
                    score_text = str(score)
                    fg = COLORS["accent_cyan"]
                text = f"{index + 1}\nscore {score_text}\nN{nodes} P{prunes}"
                bg = COLORS["tile_hover"] if focus == index else COLORS["card"]
            else:
                text = f"{index + 1}\nwaiting\n-"
                fg = COLORS["muted"]
                bg = COLORS["card"]

            cell.configure(
                text=text,
                bg=bg,
                fg=fg,
                highlightbackground=COLORS["accent_gold"] if focus == index else COLORS["border"],
            )

    def _append_backend_log(self, text: str) -> None:
        self.backend_log_lines.append(text)
        self.backend_log_lines = self.backend_log_lines[-8:]
        if hasattr(self, "backend_log_text") and self.backend_log_text.winfo_exists():
            self.backend_log_text.configure(state="normal")
            self.backend_log_text.delete("1.0", tk.END)
            self.backend_log_text.insert("end", "\n".join(self.backend_log_lines))
            self.backend_log_text.configure(state="disabled")

    def refresh_backend_window(self) -> None:
        if self.backend_window is None or not self.backend_window.winfo_exists():
            return

        trace_active = self.backend_trace_data is not None and 0 <= self.backend_trace_index < len(self.backend_trace_steps)
        if not trace_active:
            available = [index for index, cell in enumerate(self.board) if not cell]
            candidates: list[dict[str, object]] = []
            if self.game_over:
                phase = "Round complete"
                status = "Search halted"
                detail = "The round finished, so the backend is holding the final state."
                move = "Waiting for a new round."
            elif self.cpu_vs_cpu:
                phase = "Auto simulation"
                status = f"Computer vs Computer ({self.current_player} to move)"
                detail = "Both sides are controlled by the backend. Alpha-beta keeps selecting the next move."
                move = self.backend_move_var.get() if self.backend_move_var.get() != "No move selected yet." else "Evaluating the next automated move..."
            elif self.ai_symbol is None:
                phase = "Manual play"
                status = "Human vs Human"
                detail = "Backend is idle because the computer is turned off."
                move = "No AI move is being evaluated."
            elif self.current_player == self.ai_symbol:
                phase = "Alpha-beta search"
                status = f"Computer thinking as {self.ai_symbol}"
                detail = "Scanning available moves, scoring each branch, and pruning weak paths."
                move = self.backend_move_var.get() if self.backend_move_var.get() != "No move selected yet." else "Evaluating candidate moves..."
            else:
                phase = "Board sync"
                status = f"Waiting for player {self.current_player}"
                detail = "The AI is idle until the turn switches back to the computer."
                move = "Player turn in progress."

            self.backend_phase_var.set(phase)
            self.backend_status_var.set(status)
            self.backend_detail_var.set(detail)
            self.backend_move_var.set(move)
            self.backend_mode_state_var.set("Computer vs Computer" if self.cpu_vs_cpu else "Human vs Computer" if self.ai_symbol is not None else "Human vs Human")
            self.backend_turn_state_var.set(self.current_player)
            self.backend_board_state_var.set(self._format_board_state(self.board))
            self.backend_board_var.set(self._format_board_vector(self.board))
            self.backend_progress_var.set("idle")
            self.backend_alpha_var.set("alpha = -")
            self.backend_beta_var.set("beta = -")
            self.backend_nodes_var.set("nodes = 0")
            self.backend_prunes_var.set("prunes = 0")
            self.backend_best_var.set("best = -")
            self.backend_choice_var.set("choice = pending")
            self.backend_eval_var.set("evaluating: none")
            self._update_backend_structure_vars(
                board=self.board,
                available=available,
                candidates=candidates,
                nodes=0,
                prunes=0,
                steps=0,
                choice="pending",
                best="-",
            )
            self._update_backend_pipeline(0)

            for i, cell in enumerate(self.backend_cells):
                symbol = self.board[i]
                display = f"{i + 1}" if not symbol else f"{i + 1}\n{symbol}"
                cell.configure(
                    text=display,
                    bg=COLORS["tile_win"] if i in self.winning_cells else COLORS["card"] if not symbol else COLORS["tile_hover"],
                    fg=COLORS["accent_white"] if i in self.winning_cells else (COLORS["accent_coral"] if symbol == "X" else COLORS["accent_cyan"] if symbol == "O" else COLORS["muted"]),
                    highlightbackground=COLORS["accent_green"] if i == self.last_move_index and symbol else COLORS["border"],
                )

            if self.backend_last_analysis:
                entries = self.backend_last_analysis.get("entries", [])
                chosen = self.backend_last_analysis.get("chosen")
                best_score = self.backend_last_analysis.get("best_score")
                lines = ["AI evaluation:"]
                for move_index, move_score in entries:
                    lines.append(f"  move {move_index + 1}: score {move_score}")
                if chosen is not None:
                    lines.append(f"Selected move: {chosen + 1} (score {best_score})")
                self._append_backend_log("\n".join(lines))
                self.backend_last_analysis = None
        else:
            step = self.backend_trace_steps[self.backend_trace_index]
            trace = self.backend_trace_data or {}
            available = list(trace.get("available", [index for index, cell in enumerate(self.board) if not cell]))
            if "board" in step:
                self.backend_board_state_var.set(self._format_board_state(step["board"]))
                self.backend_board_var.set(self._format_board_vector(step["board"]))
            if "candidates" in step:
                self._render_backend_candidates(step["candidates"], step.get("focus"))
                self.backend_candidates_var.set(self._format_candidate_snapshot(step["candidates"]))
            self.backend_available_var.set(self._format_available_moves(available))
            self.backend_trace_steps_var.set(f"trace_steps = {len(self.backend_trace_steps)}")
            self.backend_structure_var.set(
                "board = "
                + self._format_board_vector(step.get("board", self.board))
                + "\n"
                + self._format_available_moves(available)
                + "\n"
                + self._format_candidate_snapshot(step.get("candidates", []))
                + f"\nsearch_stats = {{nodes: {trace.get('nodes', 0)}, prunes: {trace.get('prunes', 0)}}}"
                + f"\ntrace_steps = {len(self.backend_trace_steps)}"
                + f"\ncurrent_choice = {trace.get('chosen', 'pending') if self.backend_trace_index >= 4 else 'pending'}"
                + f"\ncurrent_best = {trace.get('best_score', 'pending')}"
            )
            self._update_backend_pipeline(
                {"capture": 0, "predict": 1, "score": 2, "prune": 3, "choose": 4, "commit": 5}.get(str(step.get("stage", "predict")), 1),
                None,
            )

        for i, cell in enumerate(self.backend_cells):
            symbol = self.board[i]
            display = f"{i + 1}" if not symbol else f"{i + 1}\n{symbol}"
            cell.configure(
                text=display,
                bg=COLORS["tile_win"] if i in self.winning_cells else COLORS["card"] if not symbol else COLORS["tile_hover"],
                fg=COLORS["accent_white"] if i in self.winning_cells else (COLORS["accent_coral"] if symbol == "X" else COLORS["accent_cyan"] if symbol == "O" else COLORS["muted"]),
                highlightbackground=COLORS["accent_green"] if i == self.last_move_index and symbol else COLORS["border"],
            )

        self.backend_window.update_idletasks()

    def set_theme(self, theme_name: str) -> None:
        if theme_name not in THEMES or theme_name == self.theme_name:
            return

        backend_open = self.backend_window is not None and self.backend_window.winfo_exists()
        if backend_open:
            self.close_backend_window()

        self._cancel_timers()
        self.theme_name = theme_name
        COLORS.clear()
        COLORS.update(THEMES[theme_name])
        self.root.configure(bg=COLORS["bg"])
        self._rebuild_ui()
        if backend_open:
            self.open_backend_window()

    def _cancel_timers(self) -> None:
        if self.pending_ai_job is not None:
            self.root.after_cancel(self.pending_ai_job)
            self.pending_ai_job = None
        if self.turn_banner_job is not None:
            self.root.after_cancel(self.turn_banner_job)
            self.turn_banner_job = None
        if self.bot_move_job is not None:
            self.root.after_cancel(self.bot_move_job)
            self.bot_move_job = None

    def _rebuild_ui(self) -> None:
        for child in self.root.winfo_children():
            child.destroy()
        self._configure_board_metrics()
        self._build_ui()
        self.maximize_window()
        self._refresh_labels()
        self.render()
        if self._auto_play_enabled():
            self._schedule_ai_move()

    def new_game(self, event: Optional[tk.Event] = None) -> None:
        del event
        self._cancel_timers()
        self._clear_backend_trace()
        self.bot_move_anim_step = 0
        self.bot_move_anim_index = None
        self.bot_move_anim_total = 0
        self.backend_last_analysis = None

        self.board = [""] * 9
        self.current_player = "X"
        self.game_over = False
        self.last_move_index = None
        self.hover_index = None
        self.winning_cells = []
        self._append_backend_log("New game started.")
        self._refresh_labels()
        self.render()

        if self._auto_play_enabled():
            self._schedule_ai_move()

    def toggle_ai_mode(self, event: Optional[tk.Event] = None) -> None:
        del event
        self._clear_backend_trace()
        self._cancel_timers()
        self.bot_move_anim_step = 0
        self.bot_move_anim_index = None
        self.bot_move_anim_total = 0
        log_message: Optional[str] = None
        if self.cpu_vs_cpu:
            self.cpu_vs_cpu = False
            self.ai_symbol = None
            log_message = "Computer vs computer disabled."
        elif self.game_over:
            # Keep the mode toggle available, but do not force a move into a finished game.
            self.ai_symbol = self.current_player if self.ai_symbol is None else None
        elif self.ai_symbol is None:
            self.ai_symbol = self.current_player
        else:
            self.ai_symbol = None

        self._refresh_labels()
        self.render()
        if log_message is not None:
            self._append_backend_log(log_message)
        elif not self.cpu_vs_cpu:
            self._append_backend_log(f"Computer toggled {'on' if self.ai_symbol else 'off'}.")

        if self._auto_play_enabled():
            self._schedule_ai_move()

    def toggle_cpu_vs_cpu_mode(self, event: Optional[tk.Event] = None) -> None:
        del event
        self._clear_backend_trace()
        self._cancel_timers()
        self.bot_move_anim_step = 0
        self.bot_move_anim_index = None
        self.bot_move_anim_total = 0
        self.cpu_vs_cpu = not self.cpu_vs_cpu
        if self.cpu_vs_cpu:
            self.ai_symbol = None
            self._append_backend_log("Computer vs computer enabled.")
        else:
            self.ai_symbol = None
            self._append_backend_log("Computer vs computer disabled.")

        self._cancel_timers()
        self._refresh_labels()
        self.render()

        if self._auto_play_enabled():
            self._schedule_ai_move()

    def _auto_play_enabled(self) -> bool:
        return not self.game_over and (self.cpu_vs_cpu or (self.ai_symbol is not None and self.current_player == self.ai_symbol))

    def _active_computer_symbol(self) -> Optional[str]:
        if self.cpu_vs_cpu:
            return self.current_player
        return self.ai_symbol

    def _game_mode_text(self) -> tuple[str, str, str]:
        if self.cpu_vs_cpu:
            return (
                "Computer vs Computer",
                "Both sides are controlled by the backend. Press Space to stop.",
                "Auto Play: On",
            )
        if self.ai_symbol is None:
            return (
                "Human vs Human",
                "Computer control is off. Two people can take turns locally.",
                "Computer: Off",
            )
        return (
            "Human vs Computer",
            f"Computer is controlling {self.ai_symbol} and will move on that side.",
            f"Computer: {self.ai_symbol}",
        )

    def _refresh_labels(self) -> None:
        mode_text, control_text, button_text = self._game_mode_text()

        self.mode_var.set(mode_text)
        self.control_var.set(control_text)
        self.ai_button.configure(text=button_text)
        if hasattr(self, "cpu_button"):
            cpu_button_text = "Computer vs Computer: On" if self.cpu_vs_cpu else "Computer vs Computer: Off"
            self.cpu_button.configure(text=cpu_button_text)
        if hasattr(self, "backend_button"):
            backend_button_text = "Backend: On" if self.backend_window is not None and self.backend_window.winfo_exists() else "Backend: Off"
            self.backend_button.configure(text=backend_button_text)

        self.score_x_var.set(str(self.scores["X"]))
        self.score_o_var.set(str(self.scores["O"]))
        self.score_draw_var.set(str(self.scores["Draw"]))
        self._refresh_player_states()

        if self.game_over:
            winner = self._winner_symbol(self.board)
            if winner:
                self.status_var.set(f"{winner} wins the round")
                self.control_var.set("Press New Game to start a fresh board.")
                self._set_turn_banner(f"{winner} WINS", COLORS["accent_green"], animated=False)
            else:
                self.status_var.set("Draw game")
                self.control_var.set("Every square is filled. Start a new round to keep playing.")
                self._set_turn_banner("DRAW GAME", COLORS["accent_gold"], animated=False)
        else:
            self.status_var.set(self._turn_status_text())
            if self._auto_play_enabled():
                self._set_turn_banner(f"Computer to move ({self.current_player})", COLORS["accent_cyan"], animated=False)
            else:
                accent = COLORS["accent_coral"] if self.current_player == "X" else COLORS["accent_cyan"]
                self._set_turn_banner(self._turn_status_text(), accent, animated=False)

    def _refresh_player_states(self) -> None:
        if self.cpu_vs_cpu:
            self.player1_state_var.set("Computer turn" if self.current_player == "X" else "Waiting")
            self.player2_state_var.set("Computer turn" if self.current_player == "O" else "Waiting")
            self.bot_state_var.set("Auto play enabled")
        elif self.ai_symbol is None:
            self.player1_state_var.set("Active" if self.current_player == "X" else "Waiting")
            self.player2_state_var.set("Active" if self.current_player == "O" else "Waiting")
            self.bot_state_var.set("Off")
        else:
            if self.ai_symbol == "X":
                self.player1_state_var.set("Computer turn" if self.current_player == "X" else "Waiting")
                self.player2_state_var.set("Human turn" if self.current_player == "X" else "Computer turn")
            else:
                self.player1_state_var.set("Human turn" if self.current_player == "X" else "Waiting")
                self.player2_state_var.set("Computer turn" if self.current_player == "O" else "Waiting")
            self.bot_state_var.set(f"Computer playing as {self.ai_symbol}")

    def _set_turn_banner(self, text: str, accent: str, animated: bool) -> None:
        self.turn_banner_var.set(text)
        del animated
        if self.turn_banner_job is not None:
            self.root.after_cancel(self.turn_banner_job)
            self.turn_banner_job = None
        self.turn_banner_frame.configure(bg=COLORS["panel"], highlightbackground=accent)
        self.turn_banner_label.configure(bg=COLORS["panel"], fg=accent)

    def _turn_status_text(self) -> str:
        if self.cpu_vs_cpu:
            return f"Computer vs Computer ({self.current_player} turn)"
        if self.ai_symbol is None:
            return "Player 1 turn" if self.current_player == "X" else "Player 2 turn"
        if self.current_player == self.ai_symbol:
            return f"Computer to move ({self.current_player})"
        return f"Player turn ({self.current_player})"

    def render(self) -> None:
        self._draw_board()
        self._refresh_labels()
        self.refresh_backend_window()

    def _draw_board(self) -> None:
        canvas = self.board_canvas
        canvas.delete("all")

        # Board shell and subtle depth.
        canvas.create_rectangle(16, 16, self.board_size - 10, self.board_size - 10, fill=COLORS["shadow"], outline="")
        canvas.create_rectangle(10, 10, self.board_size - 18, self.board_size - 18, fill=COLORS["panel"], outline=COLORS["border"], width=2)

        for index, (x1, y1, x2, y2) in enumerate(self.tile_positions):
            symbol = self.board[index]
            is_hover = index == self.hover_index and symbol == "" and not self.game_over
            is_winning = index in self.winning_cells
            is_last_move = index == self.last_move_index and symbol != ""
            if index == self.bot_move_anim_index and self.bot_move_anim_total > 0:
                progress = min(1.0, self.bot_move_anim_step / max(1, self.bot_move_anim_total))
                anim_scale = 0.88 + (0.12 * progress)
            else:
                anim_scale = 1.0

            tile_fill = COLORS["tile_win"] if is_winning else COLORS["tile_hover"] if is_hover else COLORS["tile"]
            tile_outline = COLORS["accent_green"] if is_winning else COLORS["accent_cyan"] if is_hover else COLORS["border"]

            canvas.create_rectangle(x1 + 5, y1 + 6, x2 + 5, y2 + 6, fill=COLORS["shadow"], outline="")
            canvas.create_rectangle(x1, y1, x2, y2, fill=tile_fill, outline=tile_outline, width=2)

            if is_last_move:
                glow_color = COLORS["accent_coral"] if symbol == "X" else COLORS["accent_cyan"]
                canvas.create_rectangle(x1 + 2, y1 + 2, x2 - 2, y2 - 2, outline=glow_color, width=3)

            if symbol:
                self._draw_piece(canvas, symbol, x1, y1, x2, y2, is_winning, anim_scale)

        if self.winning_cells:
            self._draw_winning_line(canvas)

    def _draw_x(self, canvas: tk.Canvas, x1: int, y1: int, x2: int, y2: int, winning: bool, scale: float = 1.0) -> None:
        color = COLORS["accent_white"] if winning else COLORS["accent_coral"]
        shadow = COLORS["accent_coral"] if winning else COLORS["shadow"]
        pad = int(34 * scale)
        canvas.create_line(x1 + pad + 2, y1 + pad + 2, x2 - pad + 2, y2 - pad + 2, fill=shadow, width=14, capstyle=tk.ROUND)
        canvas.create_line(x1 + pad + 2, y2 - pad + 2, x2 - pad + 2, y1 + pad + 2, fill=shadow, width=14, capstyle=tk.ROUND)
        canvas.create_line(x1 + pad, y1 + pad, x2 - pad, y2 - pad, fill=color, width=10, capstyle=tk.ROUND)
        canvas.create_line(x1 + pad, y2 - pad, x2 - pad, y1 + pad, fill=color, width=10, capstyle=tk.ROUND)

    def _draw_o(self, canvas: tk.Canvas, x1: int, y1: int, x2: int, y2: int, winning: bool, scale: float = 1.0) -> None:
        color = COLORS["accent_white"] if winning else COLORS["accent_cyan"]
        shadow = COLORS["accent_green"] if winning else COLORS["shadow"]
        pad = int(36 * scale)
        canvas.create_oval(x1 + pad + 2, y1 + pad + 2, x2 - pad + 2, y2 - pad + 2, outline=shadow, width=16)
        canvas.create_oval(x1 + pad, y1 + pad, x2 - pad, y2 - pad, outline=color, width=11)

    def _draw_piece(self, canvas: tk.Canvas, symbol: str, x1: int, y1: int, x2: int, y2: int, winning: bool, scale: float = 1.0) -> None:
        kind = THEME_MARKERS.get(self.theme_name, THEME_MARKERS["Classic"]).get(symbol, "cross")
        if kind == "cross":
            self._draw_x(canvas, x1, y1, x2, y2, winning, scale)
        elif kind == "ring":
            self._draw_o(canvas, x1, y1, x2, y2, winning, scale)
        elif kind == "bank":
            self._draw_bank(canvas, x1, y1, x2, y2, winning, scale)
        elif kind == "coin":
            self._draw_coin(canvas, x1, y1, x2, y2, winning, scale)
        elif kind == "cart":
            self._draw_cart(canvas, x1, y1, x2, y2, winning, scale)
        elif kind == "bag":
            self._draw_bag(canvas, x1, y1, x2, y2, winning, scale)
        elif kind == "cup":
            self._draw_cup(canvas, x1, y1, x2, y2, winning, scale)
        elif kind == "machine":
            self._draw_machine(canvas, x1, y1, x2, y2, winning, scale)
        elif kind == "palette":
            self._draw_palette(canvas, x1, y1, x2, y2, winning, scale)
        elif kind == "mic":
            self._draw_mic(canvas, x1, y1, x2, y2, winning, scale)
        elif kind == "network":
            self._draw_network(canvas, x1, y1, x2, y2, winning, scale)
        elif kind == "core":
            self._draw_core(canvas, x1, y1, x2, y2, winning, scale)
        else:
            self._draw_x(canvas, x1, y1, x2, y2, winning, scale)

    def _draw_bank(self, canvas: tk.Canvas, x1: int, y1: int, x2: int, y2: int, winning: bool, scale: float = 1.0) -> None:
        width = x2 - x1
        height = y2 - y1
        margin_x = int(width * 0.16)
        margin_y = int(height * 0.18)
        left = x1 + margin_x
        right = x2 - margin_x
        bottom = y2 - margin_y
        top = y1 + margin_y + int(6 * scale)
        roof = y1 + int(height * 0.18)
        center = (x1 + x2) // 2
        accent = COLORS["accent_white"] if winning else COLORS["accent_cyan"]
        detail = COLORS["accent_green"] if winning else COLORS["accent_gold"]
        shadow = COLORS["shadow"]

        canvas.create_polygon(
            left,
            top,
            center,
            roof,
            right,
            top,
            fill=accent,
            outline=shadow,
            width=3,
        )
        canvas.create_rectangle(left, top, right, bottom, fill=COLORS["panel"], outline=accent, width=3)
        column_w = max(8, int(width * 0.08))
        column_gap = (right - left - (3 * column_w)) // 4
        column_top = top + int(height * 0.10)
        column_bottom = bottom - int(height * 0.14)
        x = left + column_gap
        for _ in range(3):
            canvas.create_rectangle(x, column_top, x + column_w, column_bottom, fill=detail, outline="")
            x += column_w + column_gap
        canvas.create_rectangle(left + int(width * 0.06), bottom - int(height * 0.10), right - int(width * 0.06), bottom, fill=detail, outline="")
        canvas.create_text(center, bottom - int(height * 0.06), text="BANK", fill=COLORS["text"], font=("Segoe UI Semibold", max(8, int(9 * scale)), "bold"))

    def _draw_coin(self, canvas: tk.Canvas, x1: int, y1: int, x2: int, y2: int, winning: bool, scale: float = 1.0) -> None:
        width = x2 - x1
        height = y2 - y1
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        radius = int(min(width, height) * 0.22)
        accent = COLORS["accent_white"] if winning else COLORS["accent_gold"]
        shadow = COLORS["accent_green"] if winning else COLORS["shadow"]
        ring = COLORS["accent_cyan"]
        for offset in (int(10 * scale), int(4 * scale), 0):
            canvas.create_oval(
                cx - radius + offset,
                cy - radius + offset,
                cx + radius + offset,
                cy + radius + offset,
                fill=COLORS["panel"] if offset else accent,
                outline=shadow if offset else ring,
                width=3,
            )
        canvas.create_text(cx + int(4 * scale), cy + int(1 * scale), text="$", fill=COLORS["text"], font=("Segoe UI Semibold", max(14, int(18 * scale)), "bold"))

    def _draw_cart(self, canvas: tk.Canvas, x1: int, y1: int, x2: int, y2: int, winning: bool, scale: float = 1.0) -> None:
        width = x2 - x1
        height = y2 - y1
        left = x1 + int(width * 0.18)
        right = x2 - int(width * 0.18)
        top = y1 + int(height * 0.25)
        mid = y1 + int(height * 0.52)
        bottom = y2 - int(height * 0.22)
        accent = COLORS["accent_white"] if winning else COLORS["accent_green"]
        shadow = COLORS["shadow"]
        detail = COLORS["accent_coral"]
        canvas.create_polygon(
            left,
            top,
            right - int(width * 0.08),
            top,
            right,
            mid,
            left + int(width * 0.06),
            mid,
            fill=COLORS["panel"],
            outline=accent,
            width=3,
        )
        canvas.create_line(left + int(width * 0.08), mid, right - int(width * 0.06), mid, fill=accent, width=4)
        canvas.create_line(left + int(width * 0.03), top - int(height * 0.06), left + int(width * 0.14), top, fill=accent, width=4)
        canvas.create_line(left + int(width * 0.05), top - int(height * 0.12), left + int(width * 0.14), top - int(height * 0.02), fill=accent, width=4)
        wheel_r = max(6, int(width * 0.07))
        wheel_y = bottom
        wheel_x1 = left + int(width * 0.14)
        wheel_x2 = right - int(width * 0.10)
        for wheel_x in (wheel_x1, wheel_x2):
            canvas.create_oval(wheel_x - wheel_r, wheel_y - wheel_r, wheel_x + wheel_r, wheel_y + wheel_r, fill=detail, outline=shadow, width=2)

    def _draw_bag(self, canvas: tk.Canvas, x1: int, y1: int, x2: int, y2: int, winning: bool, scale: float = 1.0) -> None:
        width = x2 - x1
        height = y2 - y1
        left = x1 + int(width * 0.26)
        right = x2 - int(width * 0.26)
        top = y1 + int(height * 0.22)
        bottom = y2 - int(height * 0.18)
        accent = COLORS["accent_white"] if winning else COLORS["accent_coral"]
        shadow = COLORS["shadow"]
        detail = COLORS["accent_green"]
        canvas.create_rectangle(left, top + int(height * 0.06), right, bottom, fill=COLORS["panel"], outline=accent, width=3)
        canvas.create_arc(left, top - int(height * 0.02), right, top + int(height * 0.26), start=0, extent=180, style=tk.ARC, outline=accent, width=4)
        canvas.create_line(left + int(width * 0.08), top + int(height * 0.04), right - int(width * 0.08), top + int(height * 0.04), fill=detail, width=4)
        canvas.create_line((x1 + x2) // 2, top, (x1 + x2) // 2, bottom, fill=detail, width=3)
        canvas.create_line(left, bottom, right, bottom, fill=shadow, width=3)

    def _draw_cup(self, canvas: tk.Canvas, x1: int, y1: int, x2: int, y2: int, winning: bool, scale: float = 1.0) -> None:
        width = x2 - x1
        height = y2 - y1
        left = x1 + int(width * 0.24)
        right = x2 - int(width * 0.24)
        top = y1 + int(height * 0.28)
        bottom = y2 - int(height * 0.24)
        accent = COLORS["accent_white"] if winning else COLORS["accent_coral"]
        steam = COLORS["accent_gold"]
        shadow = COLORS["shadow"]
        cup_right = right - int(width * 0.10)
        canvas.create_polygon(left + int(width * 0.08), top, cup_right, top, right, bottom - int(height * 0.02), left, bottom - int(height * 0.02), fill=COLORS["panel"], outline=accent, width=3)
        canvas.create_oval(right - int(width * 0.10), top + int(height * 0.10), right + int(width * 0.04), top + int(height * 0.36), outline=accent, width=3)
        canvas.create_rectangle(left + int(width * 0.08), bottom, cup_right - int(width * 0.02), bottom + int(height * 0.05), fill=steam, outline=shadow, width=2)
        for offset in (-0.11, 0.0, 0.11):
            sx = (x1 + x2) // 2 + int(width * offset)
            canvas.create_line(sx, y1 + int(height * 0.12), sx - int(width * 0.03), y1 + int(height * 0.02), fill=steam, width=3, capstyle=tk.ROUND)

    def _draw_machine(self, canvas: tk.Canvas, x1: int, y1: int, x2: int, y2: int, winning: bool, scale: float = 1.0) -> None:
        width = x2 - x1
        height = y2 - y1
        left = x1 + int(width * 0.20)
        right = x2 - int(width * 0.20)
        top = y1 + int(height * 0.24)
        bottom = y2 - int(height * 0.20)
        accent = COLORS["accent_white"] if winning else COLORS["accent_gold"]
        shadow = COLORS["shadow"]
        detail = COLORS["accent_cyan"]
        canvas.create_rectangle(left, top, right, bottom, fill=COLORS["panel"], outline=accent, width=3)
        canvas.create_rectangle(left + int(width * 0.06), top + int(height * 0.08), right - int(width * 0.06), top + int(height * 0.22), fill=detail, outline="")
        canvas.create_rectangle(left + int(width * 0.08), top + int(height * 0.28), right - int(width * 0.08), top + int(height * 0.58), fill=COLORS["bg"], outline=detail, width=2)
        canvas.create_oval(right - int(width * 0.12), top + int(height * 0.32), right + int(width * 0.02), top + int(height * 0.46), outline=accent, width=3)
        canvas.create_rectangle((x1 + x2) // 2 - int(width * 0.10), bottom, (x1 + x2) // 2 + int(width * 0.10), bottom + int(height * 0.10), fill=accent, outline=shadow, width=2)
        for offset in (-0.08, 0.0, 0.08):
            cx = (x1 + x2) // 2 + int(width * offset)
            canvas.create_oval(cx - 3, top + int(height * 0.10) - 3, cx + 3, top + int(height * 0.10) + 3, fill=accent, outline="")

    def _draw_palette(self, canvas: tk.Canvas, x1: int, y1: int, x2: int, y2: int, winning: bool, scale: float = 1.0) -> None:
        width = x2 - x1
        height = y2 - y1
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        accent = COLORS["accent_white"] if winning else COLORS["accent_cyan"]
        shadow = COLORS["shadow"]
        detail = COLORS["accent_coral"]
        canvas.create_oval(x1 + int(width * 0.20), y1 + int(height * 0.16), x2 - int(width * 0.18), y2 - int(height * 0.14), fill=COLORS["panel"], outline=accent, width=3)
        canvas.create_oval(cx - int(width * 0.08), cy - int(height * 0.06), cx + int(width * 0.02), cy + int(height * 0.04), fill=COLORS["bg"], outline="")
        for dx, dy, color_key in (
            (-0.18, -0.02, "accent_green"),
            (-0.05, -0.18, "accent_gold"),
            (0.11, -0.02, "accent_coral"),
            (-0.02, 0.12, "accent_white"),
        ):
            px = cx + int(width * dx)
            py = cy + int(height * dy)
            canvas.create_oval(px - 5, py - 5, px + 5, py + 5, fill=COLORS[color_key], outline=shadow, width=1)
        canvas.create_line(cx - int(width * 0.11), cy + int(height * 0.12), cx + int(width * 0.14), cy - int(height * 0.08), fill=detail, width=4, capstyle=tk.ROUND)

    def _draw_mic(self, canvas: tk.Canvas, x1: int, y1: int, x2: int, y2: int, winning: bool, scale: float = 1.0) -> None:
        width = x2 - x1
        height = y2 - y1
        cx = (x1 + x2) // 2
        accent = COLORS["accent_white"] if winning else COLORS["accent_green"]
        shadow = COLORS["shadow"]
        detail = COLORS["accent_cyan"]
        capsule_top = y1 + int(height * 0.24)
        capsule_bottom = y1 + int(height * 0.60)
        capsule_left = cx - int(width * 0.10)
        capsule_right = cx + int(width * 0.10)
        canvas.create_oval(capsule_left, capsule_top, capsule_right, capsule_bottom, fill=COLORS["panel"], outline=accent, width=3)
        canvas.create_rectangle(cx - int(width * 0.03), capsule_bottom - int(height * 0.02), cx + int(width * 0.03), y2 - int(height * 0.22), fill=accent, outline=shadow, width=2)
        canvas.create_line(cx, y2 - int(height * 0.22), cx - int(width * 0.14), y2 - int(height * 0.12), fill=accent, width=4)
        canvas.create_line(cx, y2 - int(height * 0.22), cx + int(width * 0.14), y2 - int(height * 0.12), fill=accent, width=4)
        canvas.create_oval(cx - int(width * 0.13), capsule_top - int(height * 0.04), cx + int(width * 0.13), capsule_bottom + int(height * 0.04), outline=detail, width=2)

    def _draw_network(self, canvas: tk.Canvas, x1: int, y1: int, x2: int, y2: int, winning: bool, scale: float = 1.0) -> None:
        width = x2 - x1
        height = y2 - y1
        accent = COLORS["accent_white"] if winning else COLORS["accent_cyan"]
        node = COLORS["accent_green"] if winning else COLORS["accent_coral"]
        glow = COLORS["shadow"]
        points = [
            (x1 + int(width * 0.30), y1 + int(height * 0.32)),
            ((x1 + x2) // 2, y1 + int(height * 0.20)),
            (x2 - int(width * 0.28), y1 + int(height * 0.34)),
            (x1 + int(width * 0.36), y2 - int(height * 0.26)),
            (x2 - int(width * 0.30), y2 - int(height * 0.22)),
        ]
        for start, end in ((0, 1), (1, 2), (1, 3), (1, 4), (3, 4)):
            x_start, y_start = points[start]
            x_end, y_end = points[end]
            canvas.create_line(x_start, y_start, x_end, y_end, fill=accent, width=4, capstyle=tk.ROUND)
            canvas.create_line(x_start + 2, y_start + 2, x_end + 2, y_end + 2, fill=glow, width=8, capstyle=tk.ROUND)
        for x, y in points:
            canvas.create_oval(x - 8, y - 8, x + 8, y + 8, fill=node, outline=accent, width=2)
        canvas.create_oval(
            x1 + int(width * 0.24),
            y1 + int(height * 0.14),
            x2 - int(width * 0.24),
            y2 - int(height * 0.14),
            outline=COLORS["accent_gold"] if winning else COLORS["accent_green"],
            width=2,
        )

    def _draw_core(self, canvas: tk.Canvas, x1: int, y1: int, x2: int, y2: int, winning: bool, scale: float = 1.0) -> None:
        width = x2 - x1
        height = y2 - y1
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        outer = COLORS["accent_white"] if winning else COLORS["accent_green"]
        inner = COLORS["accent_cyan"]
        glow = COLORS["shadow"]
        canvas.create_oval(
            cx - int(width * 0.18) + 2,
            cy - int(height * 0.18) + 2,
            cx + int(width * 0.18) + 2,
            cy + int(height * 0.18) + 2,
            outline=glow,
            width=12,
        )
        canvas.create_oval(
            cx - int(width * 0.18),
            cy - int(height * 0.18),
            cx + int(width * 0.18),
            cy + int(height * 0.18),
            outline=outer,
            width=8,
        )
        canvas.create_oval(
            cx - int(width * 0.08),
            cy - int(height * 0.08),
            cx + int(width * 0.08),
            cy + int(height * 0.08),
            fill=inner,
            outline=COLORS["accent_white"],
            width=2,
        )
        canvas.create_line(
            cx - int(width * 0.24),
            cy,
            cx + int(width * 0.24),
            cy,
            fill=COLORS["accent_gold"],
            width=2,
            dash=(4, 4),
        )

    def _draw_winning_line(self, canvas: tk.Canvas) -> None:
        start = self.tile_center(self.winning_cells[0])
        end = self.tile_center(self.winning_cells[-1])
        canvas.create_line(
            start[0],
            start[1],
            end[0],
            end[1],
            fill=COLORS["accent_green"],
            width=16,
            capstyle=tk.ROUND,
        )
        canvas.create_line(
            start[0],
            start[1],
            end[0],
            end[1],
            fill=COLORS["accent_white"],
            width=4,
            capstyle=tk.ROUND,
        )

    def tile_center(self, index: int) -> tuple[int, int]:
        x1, y1, x2, y2 = self.tile_positions[index]
        return ((x1 + x2) // 2, (y1 + y2) // 2)

    def on_board_motion(self, event: tk.Event) -> None:
        index = self.index_from_xy(event.x, event.y)
        if index != self.hover_index:
            self.hover_index = index
            self._draw_board()

    def on_board_leave(self, event: tk.Event) -> None:
        del event
        if self.hover_index is not None:
            self.hover_index = None
            self._draw_board()

    def on_board_click(self, event: tk.Event) -> None:
        index = self.index_from_xy(event.x, event.y)
        if index is None:
            return
        self.make_move(index)

    def index_from_xy(self, x: int, y: int) -> Optional[int]:
        for index, (x1, y1, x2, y2) in enumerate(self.tile_positions):
            if x1 <= x <= x2 and y1 <= y <= y2:
                return index
        return None

    def make_move(self, index: int, by_ai: bool = False) -> bool:
        if self.game_over or self.board[index]:
            return False
        if self._auto_play_enabled() and not by_ai:
            return False

        self.board[index] = self.current_player
        self.last_move_index = index
        winner = self._winner_symbol(self.board)

        if winner:
            self.game_over = True
            self.winning_cells = list(self._winning_line(self.board) or [])
            self.scores[winner] += 1
            self._refresh_labels()
            self.render()
            return True

        if "" not in self.board:
            self.game_over = True
            self.scores["Draw"] += 1
            self.winning_cells = []
            self._refresh_labels()
            self.render()
            return True

        self.current_player = other_symbol(self.current_player)
        self._refresh_labels()
        self.render()

        if self._auto_play_enabled():
            self._schedule_ai_move()

        return True

    def _winner_symbol(self, board: Sequence[str]) -> Optional[str]:
        for line in self.win_lines:
            value = board[line[0]]
            if value and all(board[index] == value for index in line[1:]):
                return value
        return None

    def _winning_line(self, board: Sequence[str]) -> Optional[Sequence[int]]:
        for line in self.win_lines:
            value = board[line[0]]
            if value and all(board[index] == value for index in line[1:]):
                return line
        return None

    def _schedule_ai_move(self) -> None:
        if self.pending_ai_job is not None:
            self.root.after_cancel(self.pending_ai_job)
        if self.game_over or not self._auto_play_enabled():
            self.pending_ai_job = None
            return
        self.pending_ai_job = self.root.after(BOT_THINK_DELAY_MS, self._ai_move)

    def _ai_move(self) -> None:
        self.pending_ai_job = None
        if self.game_over or self._active_computer_symbol() != self.current_player:
            return

        move = self.best_ai_move()
        if move is not None:
            trace = None
            if self.backend_last_analysis:
                trace = self.backend_last_analysis.get("trace")
                self.backend_last_analysis = None
            use_trace = (
                trace is not None
                and not self.cpu_vs_cpu
                and self.backend_window is not None
                and self.backend_window.winfo_exists()
            )
            if use_trace:
                self._set_backend_trace(trace, move)
            else:
                self._clear_backend_trace()
                self.make_move(move, by_ai=True)
                self._start_bot_move_animation(move)

    def _start_bot_move_animation(self, index: int) -> None:
        if self.bot_move_job is not None:
            self.root.after_cancel(self.bot_move_job)
            self.bot_move_job = None
        self.bot_move_anim_index = index
        self.bot_move_anim_step = 0
        self.bot_move_anim_total = 5
        self._animate_bot_move()

    def _animate_bot_move(self) -> None:
        if self.bot_move_anim_index is None:
            self.bot_move_job = None
            return

        if self.bot_move_anim_step >= self.bot_move_anim_total:
            self.bot_move_job = None
            self.bot_move_anim_index = None
            self.render()
            return

        self.render()
        self.bot_move_anim_step += 1
        self.bot_move_job = self.root.after(BOT_MOVE_ANIM_MS, self._animate_bot_move)

    def best_ai_move(self) -> Optional[int]:
        ai = self._active_computer_symbol()
        if ai is None:
            return None

        human = other_symbol(ai)
        board = tuple(self.board)
        available = [index for index, cell in enumerate(board) if not cell]
        if not available:
            return None

        preferred_order = (4, 0, 2, 6, 8, 1, 3, 5, 7)

        def ordered_moves(state: Sequence[str]) -> list[int]:
            return [idx for idx in preferred_order if not state[idx]]

        search_stats = {"nodes": 0, "prunes": 0}

        def score(state: tuple[str, ...], turn: str, alpha: int, beta: int, depth: int) -> int:
            search_stats["nodes"] += 1
            winner = self._winner_symbol(state)
            if winner == ai:
                return 100 - depth
            if winner == human:
                return depth - 100
            if "" not in state:
                return 0

            moves = ordered_moves(state)
            if turn == ai:
                best = -1000
                for idx in moves:
                    next_state = list(state)
                    next_state[idx] = turn
                    best = max(best, score(tuple(next_state), human, alpha, beta, depth + 1))
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        search_stats["prunes"] += 1
                        break
                return best

            best = 1000
            for idx in moves:
                next_state = list(state)
                next_state[idx] = turn
                best = min(best, score(tuple(next_state), ai, alpha, beta, depth + 1))
                beta = min(beta, best)
                if beta <= alpha:
                    search_stats["prunes"] += 1
                    break
            return best

        best_score = -1000
        best_moves: list[int] = []
        evaluated_moves: list[tuple[int, int]] = []
        trace_steps: list[dict[str, object]] = [
            {
                "stage": "capture",
                "phase": "Capture board",
                "status": "Board stored in search buffer",
                "detail": "The backend copies the visible board into a plain array before any prediction starts.",
                "board": list(board),
                "move_text": "Board copied into memory.",
                "alpha": "-1000",
                "beta": "1000",
                "nodes": 0,
                "prunes": 0,
                "best": "-",
                "choice": "pending",
                "eval": "State vector prepared.",
            },
            {
                "stage": "predict",
                "phase": "Predict candidates",
                "status": "Enumerating open squares",
                "detail": f"Open squares: {', '.join(str(index + 1) for index in available)}",
                "board": list(board),
                "move_text": "Possible moves are being prepared.",
                "alpha": "-1000",
                "beta": "1000",
                "nodes": 0,
                "prunes": 0,
                "best": "-",
                "choice": "pending",
                "eval": f"{len(available)} legal moves found.",
                "candidates": [
                    {"move": index, "score": "-", "nodes": 0, "prunes": 0}
                    for index in available
                ],
                "focus": None,
            },
        ]
        current_candidates: list[dict[str, object]] = [
            {"move": index, "score": "-", "nodes": 0, "prunes": 0}
            for index in available
        ]

        for move in ordered_moves(board):
            next_state = list(board)
            next_state[move] = ai
            before_nodes = search_stats["nodes"]
            before_prunes = search_stats["prunes"]
            move_score = score(tuple(next_state), human, -1000, 1000, 1)
            nodes_delta = search_stats["nodes"] - before_nodes
            prunes_delta = search_stats["prunes"] - before_prunes
            evaluated_moves.append((move, move_score))
            for candidate in current_candidates:
                if int(candidate["move"]) == move:
                    candidate["score"] = move_score
                    candidate["nodes"] = nodes_delta
                    candidate["prunes"] = prunes_delta
                    break
            current_best = best_score
            trace_steps.append(
                {
                    "stage": "score",
                    "phase": "Score branches",
                    "status": f"Evaluating square {move + 1}",
                    "detail": f"Candidate {move + 1} returns score {move_score} after {nodes_delta} nodes and {prunes_delta} prunes.",
                    "board": list(board),
                    "move_text": f"Square {move + 1} scored {move_score}.",
                    "alpha": str(current_best),
                    "beta": "1000",
                    "nodes": search_stats["nodes"],
                    "prunes": search_stats["prunes"],
                    "best": current_best if current_best != -1000 else move_score,
                    "choice": "pending",
                    "eval": f"Move {move + 1} -> score {move_score}",
                    "candidates": [dict(item) for item in current_candidates],
                    "focus": move,
                }
            )
            if move_score > best_score:
                best_score = move_score
                best_moves = [move]
            elif move_score == best_score:
                best_moves.append(move)

        if not best_moves:
            return None

        chosen = random.choice(best_moves)
        trace_steps.append(
            {
                "stage": "choose",
                "phase": "Choose move",
                "status": f"Selected square {chosen + 1}",
                "detail": f"The best score is {best_score}, so the backend chooses square {chosen + 1}.",
                "board": list(board),
                "move_text": f"Chosen move: {chosen + 1}.",
                "alpha": str(best_score),
                "beta": "1000",
                "nodes": search_stats["nodes"],
                "prunes": search_stats["prunes"],
                "best": best_score,
                "choice": chosen + 1,
                "eval": f"Final choice: {chosen + 1}",
                "candidates": [dict(item) for item in current_candidates],
                "focus": chosen,
            }
        )
        trace_steps.append(
            {
                "stage": "commit",
                "phase": "Apply move",
                "status": f"Applying move {chosen + 1}",
                "detail": "The selected move leaves search and becomes the live board move.",
                "board": list(board),
                "move_text": f"Applying chosen move {chosen + 1}.",
                "alpha": str(best_score),
                "beta": "1000",
                "nodes": search_stats["nodes"],
                "prunes": search_stats["prunes"],
                "best": best_score,
                "choice": chosen + 1,
                "eval": "Committing the selected branch.",
                "candidates": [dict(item) for item in current_candidates],
                "focus": chosen,
            }
        )
        self.backend_last_analysis = {
            "entries": evaluated_moves,
            "chosen": chosen,
            "best_score": best_score,
            "trace": {
                "board": list(board),
                "mode": "Computer vs Computer" if self.cpu_vs_cpu else "Human vs Computer",
                "turn": ai,
                "human": human,
                "available": available,
                "current_candidates": [dict(item) for item in current_candidates],
                "nodes": search_stats["nodes"],
                "prunes": search_stats["prunes"],
                "entries": evaluated_moves,
                "chosen": chosen,
                "best_score": best_score,
                "steps": trace_steps,
            },
        }
        self._append_backend_log(
            f"Alpha-beta selected move {chosen + 1} with score {best_score}. "
            f"Visited {search_stats['nodes']} nodes and pruned {search_stats['prunes']} branches."
        )
        return chosen

    def on_close(self, event: Optional[tk.Event] = None) -> None:
        del event
        self._cancel_timers()
        self.close_backend_window()
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    TicTacToeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
