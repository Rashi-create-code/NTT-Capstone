# Capstone Project: Make the Computer Draw a Box

**Course:** Nand to Tetris – I (ETCCNT301), K.R. Mangalam University
**Name:** Rashi Mangal | **Roll No:** 2501730043 | **K = 43**

A black box appears on the Hack computer's screen while a key is pressed and disappears when it is released.

## For K = 43

| Item | Value |
|---|---|
| Box start row | 43 |
| Box height | 20 rows (rows 43–62) |
| Box width | 16 × ((43 mod 4) + 1) = **64 pixels = 4 words** |
| First word address | 16384 + 32 × 43 = **17760** |
| Extra assembler feature | 43 mod 3 = 1 → error message with line number |

## Folder contents

| File | Purpose |
|---|---|
| `CPU.hdl`, `Memory.hdl`, `Computer.hdl` | Part A: the computer, built from my own chips |
| `assembler.py` | Part B: Python assembler (.asm → .hack) |
| `Box.asm` | Part C: box program in Hack assembly |
| `Box.hack` | Box.asm assembled by my own assembler |

## Part A – Computer

CPU, Memory, ComputerAdd, ComputerMax and ComputerRect all pass the official tests ("output file is identical to the compare file"). No built-in chips were used.

## Part B – Assembler

Run it from the folder with `assembler.py`:

```
python assembler.py Box.asm
```

Output:

```
Assembly successful!
Output file: Box.hack
Total instructions: 51
```

How it works:
1. **First pass:** removes comments and blank lines, and stores each label such as `(LOOP)` with its instruction number.
2. **Second pass:** converts each line to 16 bits. New variables get RAM addresses from 16 upwards.

Tested against the official assembler: **Add, Max, Rect and Pong all match.**

**Extra feature (K mod 3 = 1):** a wrong line gives a clear message instead of a crash:

```
python assembler.py Wrong.asm
Line 3: Invalid computation 'INVALID'
```

## Part C – Box program

`Box.asm` loops forever:
1. Read the keyboard (`@KBD`). If a key is pressed, `color = -1` (black); otherwise `color = 0` (white).
2. Paint 20 rows × 4 words, starting at `SCREEN + 1376`, with `color`.
3. After each row, move 32 words forward to the next screen row.

To run it:
1. Assemble: `python assembler.py Box.asm`
2. Open the CPU Emulator at [nand2tetris.org](https://nand2tetris.org) and load `Box.hack`.
3. Click **Enable Keyboard**, set the speed to **Fast**, and press Run (the ⏩ button above the screen).
4. Click the screen and hold any key. The box appears; release the key and it disappears.

## Mistake fixed

My first version cleared the whole screen (8192 words) on every pass and checked the keyboard only once per pass, so a key press was often missed. I changed it to redraw only the 64 × 20 box area using a `color` variable (0 or -1), so the keyboard is checked far more often.
