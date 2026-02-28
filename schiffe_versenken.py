#!/usr/bin/env python3
"""Einfaches Schiffe-Versenken für das Terminal.

Start:
    python3 schiffe_versenken.py
"""

from __future__ import annotations

import random
from dataclasses import dataclass

BOARD_SIZE = 8
SHIP_LENGTHS = [4, 3, 3, 2, 2, 2]
WATER = "~"
SHIP = "S"
HIT = "X"
MISS = "o"


@dataclass
class ShotResult:
    hit: bool
    sunk: bool
    already_targeted: bool = False


class Board:
    def __init__(self, size: int, ship_lengths: list[int]) -> None:
        self.size = size
        self.grid = [[WATER for _ in range(size)] for _ in range(size)]
        self.shots = [[WATER for _ in range(size)] for _ in range(size)]
        self.ships: list[set[tuple[int, int]]] = []
        self._place_ships_randomly(ship_lengths)

    def _place_ships_randomly(self, lengths: list[int]) -> None:
        for length in lengths:
            placed = False
            for _ in range(500):
                horizontal = random.choice([True, False])
                if horizontal:
                    r = random.randrange(self.size)
                    c = random.randrange(self.size - length + 1)
                    coords = {(r, c + i) for i in range(length)}
                else:
                    r = random.randrange(self.size - length + 1)
                    c = random.randrange(self.size)
                    coords = {(r + i, c) for i in range(length)}

                if self._can_place(coords):
                    for rr, cc in coords:
                        self.grid[rr][cc] = SHIP
                    self.ships.append(coords)
                    placed = True
                    break
            if not placed:
                raise RuntimeError("Schiffe konnten nicht platziert werden.")

    def _can_place(self, coords: set[tuple[int, int]]) -> bool:
        for r, c in coords:
            if self.grid[r][c] == SHIP:
                return False
            for rr in range(max(0, r - 1), min(self.size, r + 2)):
                for cc in range(max(0, c - 1), min(self.size, c + 2)):
                    if self.grid[rr][cc] == SHIP:
                        return False
        return True

    def fire(self, r: int, c: int) -> ShotResult:
        if self.shots[r][c] in (HIT, MISS):
            return ShotResult(hit=False, sunk=False, already_targeted=True)

        if self.grid[r][c] == SHIP:
            self.shots[r][c] = HIT
            self.grid[r][c] = HIT
            sunk = self._check_if_ship_sunk(r, c)
            return ShotResult(hit=True, sunk=sunk)

        self.shots[r][c] = MISS
        self.grid[r][c] = MISS
        return ShotResult(hit=False, sunk=False)

    def _check_if_ship_sunk(self, hit_r: int, hit_c: int) -> bool:
        for ship in self.ships:
            if (hit_r, hit_c) in ship:
                return all(self.grid[r][c] == HIT for r, c in ship)
        return False

    def remaining_ships(self) -> int:
        return sum(1 for ship in self.ships if not all(self.grid[r][c] == HIT for r, c in ship))

    def all_sunk(self) -> bool:
        return self.remaining_ships() == 0


def print_board(board: list[list[str]], reveal_ships: bool = False) -> None:
    size = len(board)
    header = "   " + " ".join(f"{i + 1:2}" for i in range(size))
    print(header)
    for idx, row in enumerate(board):
        label = chr(ord("A") + idx)
        rendered = []
        for cell in row:
            if cell == SHIP and not reveal_ships:
                rendered.append(WATER)
            else:
                rendered.append(cell)
        print(f"{label:>2} " + " ".join(f"{c:>2}" for c in rendered))


def parse_coordinate(text: str, size: int) -> tuple[int, int] | None:
    text = text.strip().upper()
    if len(text) < 2:
        return None

    row_char = text[0]
    if not ("A" <= row_char <= chr(ord("A") + size - 1)):
        return None

    number_part = text[1:]
    if not number_part.isdigit():
        return None

    col = int(number_part) - 1
    row = ord(row_char) - ord("A")
    if 0 <= row < size and 0 <= col < size:
        return row, col
    return None


def random_available_shot(shots: list[list[str]]) -> tuple[int, int]:
    candidates = [
        (r, c)
        for r in range(len(shots))
        for c in range(len(shots))
        if shots[r][c] not in (HIT, MISS)
    ]
    return random.choice(candidates)


def run_game() -> None:
    player = Board(BOARD_SIZE, SHIP_LENGTHS)
    computer = Board(BOARD_SIZE, SHIP_LENGTHS)

    print("Willkommen zu Schiffe Versenken!\n")
    print("Koordinaten eingeben wie A1, C5 oder H8.\n")

    while True:
        print("Dein Radar auf gegnerische Schiffe:")
        print_board(computer.shots)
        print(f"Gegnerische verbleibende Schiffe: {computer.remaining_ships()}\n")

        while True:
            user_input = input("Dein Schuss: ")
            coord = parse_coordinate(user_input, BOARD_SIZE)
            if coord is None:
                print("Ungültige Eingabe. Beispiel: B4")
                continue

            r, c = coord
            result = computer.fire(r, c)
            if result.already_targeted:
                print("Diese Position hast du schon beschossen.")
                continue

            if result.hit and result.sunk:
                print("Treffer und versenkt!\n")
            elif result.hit:
                print("Treffer!\n")
            else:
                print("Daneben.\n")
            break

        if computer.all_sunk():
            print("Du hast gewonnen! Alle gegnerischen Schiffe sind versenkt.")
            break

        print("Computer ist am Zug...")
        cr, cc = random_available_shot(player.shots)
        comp_result = player.fire(cr, cc)
        coord_label = f"{chr(ord('A') + cr)}{cc + 1}"

        if comp_result.hit and comp_result.sunk:
            print(f"Computer trifft {coord_label}: versenkt!")
        elif comp_result.hit:
            print(f"Computer trifft {coord_label}!")
        else:
            print(f"Computer schießt {coord_label} daneben.")

        print("\nDein Spielfeld:")
        print_board(player.grid, reveal_ships=True)
        print(f"Deine verbleibenden Schiffe: {player.remaining_ships()}\n")

        if player.all_sunk():
            print("Du hast verloren. Der Computer hat alle deine Schiffe versenkt.")
            break


if __name__ == "__main__":
    try:
        run_game()
    except KeyboardInterrupt:
        print("\nSpiel abgebrochen.")
