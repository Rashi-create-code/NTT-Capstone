
import re
import sys

# Hack instruction tables
COMP = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "M": "1110000",
    "!D": "0001101",
    "!A": "0110001",
    "!M": "1110001",
    "-D": "0001111",
    "-A": "0110011",
    "-M": "1110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "M-1": "1110010",
    "D+A": "0000010",
    "D+M": "1000010",
    "D-A": "0010011",
    "D-M": "1010011",
    "A-D": "0000111",
    "M-D": "1000111",
    "D&A": "0000000",
    "D&M": "1000000",
    "D|A": "0010101",
    "D|M": "1010101"
}

JUMP = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

PREDEFINED = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "SCREEN": 16384, "KBD": 24576
}

for i in range(16):
    PREDEFINED["R" + str(i)] = i


LABEL_PATTERN = re.compile(r"^[a-zA-Z_.$:][a-zA-Z0-9_.$:]*$")


def clean_file(filename):
    """Remove comments, blank lines and unnecessary spaces."""
    instructions = []

    with open(filename, "r") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.split("//")[0]
            line = re.sub(r"\s+", "", line)

            if line:
                instructions.append((line, line_number))

    return instructions


def first_pass(instructions):
    """Find labels and store their ROM addresses."""
    symbols = PREDEFINED.copy()
    rom_address = 0

    for instruction, line_number in instructions:

        if instruction.startswith("(") and instruction.endswith(")"):
            label = instruction[1:-1]

            if not LABEL_PATTERN.fullmatch(label):
                raise ValueError(
                    f"Line {line_number}: Invalid label '{label}'"
                )

            if label in symbols:
                raise ValueError(
                    f"Line {line_number}: Duplicate label '{label}'"
                )

            symbols[label] = rom_address

        else:
            rom_address += 1

    return symbols


def second_pass(instructions, symbols):
    """Translate assembly instructions into 16-bit machine code."""
    machine_code = []
    next_variable = 16

    for instruction, line_number in instructions:

        try:
            # Ignore labels
            if instruction.startswith("(") and instruction.endswith(")"):
                continue

            # A-instruction
            if instruction.startswith("@"):
                value = instruction[1:]

                if value.isdigit():
                    address = int(value)

                else:
                    if value not in symbols:
                        symbols[value] = next_variable
                        next_variable += 1

                    address = symbols[value]

                if not 0 <= address <= 32767:
                    raise ValueError("Address must be between 0 and 32767")

                binary = format(address, "016b")

            # C-instruction
            else:
                dest = ""
                jump = ""
                comp = instruction

                if "=" in comp:
                    dest, comp = comp.split("=", 1)

                if ";" in comp:
                    comp, jump = comp.split(";", 1)

                # Validate destination registers
                if any(ch not in "ADM" for ch in dest):
                    raise ValueError(f"Invalid destination '{dest}'")

                if len(set(dest)) != len(dest):
                    raise ValueError(f"Duplicate destination '{dest}'")

                # Correct destination bits: A, D, M
                dest_bits = (
                    ("1" if "A" in dest else "0") +
                    ("1" if "D" in dest else "0") +
                    ("1" if "M" in dest else "0")
                )

                if comp not in COMP:
                    raise ValueError(f"Invalid computation '{comp}'")

                if jump not in JUMP:
                    raise ValueError(f"Invalid jump '{jump}'")

                binary = "111" + COMP[comp] + dest_bits + JUMP[jump]

            machine_code.append(binary)

        except ValueError as error:
            raise ValueError(f"Line {line_number}: {error}")

    return machine_code


def assemble(input_file):
    instructions = clean_file(input_file)

    symbols = first_pass(instructions)
    machine_code = second_pass(instructions, symbols)

    output_file = input_file.rsplit(".", 1)[0] + ".hack"

    with open(output_file, "w") as file:
        for instruction in machine_code:
            file.write(instruction + "\n")

    print("Assembly successful!")
    print("Output file:", output_file)
    print("Total instructions:", len(machine_code))


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python assembler.py filename.asm")
        sys.exit(1)

    try:
        assemble(sys.argv[1])

    except (ValueError, FileNotFoundError) as error:
        print(error)
        sys.exit(1)
