# Tic Tac Toe Game

A polished Tic Tac Toe app with a premium Tkinter desktop frontend, a live backend debugger panel, and a standalone browser version.

## Features

- Premium desktop-style UI with a custom in-app icon
- Themed playboard and themed pieces
- Human vs Human mode
- Human vs Computer mode
- Computer vs Computer mode
- Unbeatable alpha-beta AI for standard 3x3 play
- Live backend simulation panel that shows:
  - board storage
  - available moves
  - candidate scoring
  - alpha and beta values
  - nodes visited
  - prunes
  - selected move
- Separate browser version in `index.html`

## Controls

- Click a tile to play
- `R` or `N` = new game
- `Space` = toggle computer control
- `R` then `Space` = computer vs computer mode(Fast Mode)
- `Esc` = exit
- `Backend Window` button = show or hide the simulation panel

## Desktop Version

Requires Python with Tkinter available.

Run:

```bash
python Game.py
```

If `python` is not available, try:

```bash
py Game.py
```

## Browser Version

Open `index.html` directly in a browser, or serve the folder with any static web server.

## How the Backend Panel Works

- The game stores the board as a 9-item list.
- When it is the computer’s turn, the AI copies that board into a search buffer.
- It builds the list of legal moves from empty cells.
- Each candidate move is scored with recursive alpha-beta pruning.
- The backend panel updates live through the search:
  - `alpha` = best guaranteed maximizing value so far
  - `beta` = best guaranteed minimizing value so far
  - `nodes` = recursive states explored
  - `prunes` = branches skipped because they cannot improve the result
  - `best` = strongest root-level score found so far
  - `choice` = final selected move
- In Human vs Computer mode, the panel uses a slower step-by-step trace so the reasoning is visible.
- In Computer vs Computer mode, the game runs at normal speed.

## Notes

- The gameplay is still standard 3x3 Tic Tac Toe.
- The AI logic remains unbeatable on the normal board.
- If you want to rebuild the packaged executable, rebuild it from the updated source instead of using the old `dist` output.

## License

GNU GPLv3
