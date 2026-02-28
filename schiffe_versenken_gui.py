#!/usr/bin/env python3
"""Schiffe Versenken mit einfacher Tkinter-GUI.

Start:
    python3 schiffe_versenken_gui.py
"""

from __future__ import annotations

import random
import tkinter as tk
from tkinter import messagebox

from schiffe_versenken import BOARD_SIZE, SHIP, HIT, MISS, Board


class BattleshipGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Schiffe Versenken")
        self.root.resizable(False, False)

        self.player_board: Board
        self.computer_board: Board
        self.enemy_buttons: list[list[tk.Button]] = []
        self.player_labels: list[list[tk.Label]] = []
        self.game_over = False

        self.status_var = tk.StringVar(value="Willkommen! Du beginnst.")
        self.remaining_var = tk.StringVar(value="")

        self._build_layout()
        self.new_game()

    def _build_layout(self) -> None:
        wrapper = tk.Frame(self.root, padx=12, pady=12)
        wrapper.pack()

        title = tk.Label(wrapper, text="Schiffe Versenken", font=("Arial", 18, "bold"))
        title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        status = tk.Label(wrapper, textvariable=self.status_var, anchor="w", font=("Arial", 11))
        status.grid(row=1, column=0, columnspan=2, sticky="we")

        remaining = tk.Label(wrapper, textvariable=self.remaining_var, anchor="w", font=("Arial", 10))
        remaining.grid(row=2, column=0, columnspan=2, sticky="we", pady=(0, 10))

        enemy_frame = tk.LabelFrame(wrapper, text="Gegnerisches Feld", padx=8, pady=8)
        enemy_frame.grid(row=3, column=0, padx=(0, 10), sticky="n")

        player_frame = tk.LabelFrame(wrapper, text="Dein Feld", padx=8, pady=8)
        player_frame.grid(row=3, column=1, sticky="n")

        self._build_enemy_grid(enemy_frame)
        self._build_player_grid(player_frame)

        controls = tk.Frame(wrapper)
        controls.grid(row=4, column=0, columnspan=2, sticky="we", pady=(10, 0))

        restart_btn = tk.Button(controls, text="Neues Spiel", command=self.new_game, width=16)
        restart_btn.pack(side="left")

        quit_btn = tk.Button(controls, text="Beenden", command=self.root.destroy, width=16)
        quit_btn.pack(side="left", padx=(8, 0))

    def _build_enemy_grid(self, parent: tk.Widget) -> None:
        self.enemy_buttons = []
        for r in range(BOARD_SIZE):
            row_buttons: list[tk.Button] = []
            for c in range(BOARD_SIZE):
                btn = tk.Button(
                    parent,
                    width=3,
                    height=1,
                    font=("Consolas", 10, "bold"),
                    bg="#7db7ff",
                    activebackground="#6aa8f5",
                    command=lambda rr=r, cc=c: self.player_shot(rr, cc),
                )
                btn.grid(row=r, column=c, padx=1, pady=1)
                row_buttons.append(btn)
            self.enemy_buttons.append(row_buttons)

    def _build_player_grid(self, parent: tk.Widget) -> None:
        self.player_labels = []
        for r in range(BOARD_SIZE):
            row_labels: list[tk.Label] = []
            for c in range(BOARD_SIZE):
                lbl = tk.Label(
                    parent,
                    width=3,
                    height=1,
                    font=("Consolas", 10, "bold"),
                    relief="ridge",
                    bg="#7db7ff",
                )
                lbl.grid(row=r, column=c, padx=1, pady=1)
                row_labels.append(lbl)
            self.player_labels.append(row_labels)

    def new_game(self) -> None:
        self.player_board = Board(BOARD_SIZE, [4, 3, 3, 2, 2, 2])
        self.computer_board = Board(BOARD_SIZE, [4, 3, 3, 2, 2, 2])
        self.game_over = False
        self.status_var.set("Neues Spiel gestartet. Du bist am Zug.")
        self._refresh_all()

    def player_shot(self, r: int, c: int) -> None:
        if self.game_over:
            return

        result = self.computer_board.fire(r, c)
        if result.already_targeted:
            self.status_var.set("Feld schon beschossen. Wähle ein anderes.")
            return

        if result.hit and result.sunk:
            self.status_var.set("Treffer und versenkt!")
        elif result.hit:
            self.status_var.set("Treffer!")
        else:
            self.status_var.set("Daneben.")

        self._refresh_enemy_grid()
        self._update_remaining_text()

        if self.computer_board.all_sunk():
            self._finish_game(True)
            return

        self.root.after(350, self.computer_turn)

    def computer_turn(self) -> None:
        if self.game_over:
            return

        candidates = [
            (r, c)
            for r in range(BOARD_SIZE)
            for c in range(BOARD_SIZE)
            if self.player_board.shots[r][c] not in (HIT, MISS)
        ]
        r, c = random.choice(candidates)

        result = self.player_board.fire(r, c)
        coord = f"{chr(ord('A') + r)}{c + 1}"

        if result.hit and result.sunk:
            self.status_var.set(f"Computer trifft {coord}: versenkt!")
        elif result.hit:
            self.status_var.set(f"Computer trifft {coord}!")
        else:
            self.status_var.set(f"Computer schießt auf {coord}: daneben.")

        self._refresh_player_grid()
        self._update_remaining_text()

        if self.player_board.all_sunk():
            self._finish_game(False)

    def _finish_game(self, player_won: bool) -> None:
        self.game_over = True
        if player_won:
            self.status_var.set("Du hast gewonnen! Alle Gegner-Schiffe sind versenkt.")
            messagebox.showinfo("Spielende", "Glückwunsch, du hast gewonnen!")
        else:
            self.status_var.set("Du hast verloren. Alle deine Schiffe wurden versenkt.")
            messagebox.showinfo("Spielende", "Der Computer hat gewonnen.")
        self._refresh_enemy_grid(reveal=True)

    def _refresh_all(self) -> None:
        self._refresh_enemy_grid()
        self._refresh_player_grid()
        self._update_remaining_text()

    def _update_remaining_text(self) -> None:
        self.remaining_var.set(
            f"Verbleibend – Du: {self.player_board.remaining_ships()} | Gegner: {self.computer_board.remaining_ships()}"
        )

    def _refresh_enemy_grid(self, reveal: bool = False) -> None:
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                btn = self.enemy_buttons[r][c]
                shot = self.computer_board.shots[r][c]
                cell = self.computer_board.grid[r][c]

                if shot == HIT:
                    btn.config(text="X", bg="#ff5f5f", state="disabled", disabledforeground="white")
                elif shot == MISS:
                    btn.config(text="•", bg="#d0d7de", state="disabled", disabledforeground="#4b5563")
                elif reveal and cell == SHIP:
                    btn.config(text="S", bg="#9ca3af", state="disabled", disabledforeground="black")
                else:
                    btn.config(text="", bg="#7db7ff", state="normal")

    def _refresh_player_grid(self) -> None:
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                lbl = self.player_labels[r][c]
                cell = self.player_board.grid[r][c]

                if cell == SHIP:
                    lbl.config(text="S", bg="#93c5fd")
                elif cell == HIT:
                    lbl.config(text="X", bg="#ef4444", fg="white")
                elif cell == MISS:
                    lbl.config(text="•", bg="#cbd5e1", fg="#334155")
                else:
                    lbl.config(text="", bg="#7db7ff", fg="black")


def main() -> None:
    root = tk.Tk()
    BattleshipGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
