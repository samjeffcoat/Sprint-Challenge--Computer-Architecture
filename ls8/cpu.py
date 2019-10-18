"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        pass
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.operations = {
            "LDI": 0b10000010,
            "HLT": 0b00000001,
            "PRN": 0b01000111,
            "ADD": 0b10100000,
            "MUL": 0b10100010,
            "PUSH": 0b01000101,
            "POP": 0b01000110,
        }
        self.sp = 0xF4

    # should accept the address to read and return the value stored there.
    def ram_read(self, MAR):  # The MAR contains the address that is being read or written to
        return self.ram[MAR]
    # should accept a value to write, and the address to write it to.

    # The MDR contains the data that was read or the data to write.
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, filename):
        """Load a program into memory."""

        try:
            address = 0

        # For now, we've just hardcoded a program:
            with open(filename) as f:
                for line in f:
                    comment_split = line.split("#")
                    num = comment_split[0].strip()

                    try:
                        val = int(num, 2)
                    except ValueError:
                        continue
                    self.ram[address] = val
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == self.operations["ADD"]:
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == self.operations["MUL"]:
            mul = self.reg[reg_a] * self.reg[reg_b]
            self.reg[reg_a] = mul
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        # It needs to read the memory address that's stored in register `PC`
        # store that result in `IR
        # self.trace()
        running = True
        while running:
            #self.trace()
            IR = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == self.operations["LDI"]:  # loads data onto the register
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif IR == self.operations["PRN"]:  # prints
                print(self.reg[operand_a])
                self.pc += 2
            elif IR == self.operations["HLT"]:  # stops or exits the program
                running = False
            elif IR == self.operations["MUL"]:
                self.alu(self.operations["MUL"], operand_a, operand_b)
                self.pc += 3

            elif IR == self.operations["PUSH"]:
                self.sp = (self.sp-1) & 0xFF
                self.ram[self.sp] = self.reg[operand_a]
                self.pc += 2

            # pop the value of the 7th register // ram read ram write
            elif IR == self.operations["POP"]:
                self.reg[operand_a] = self.ram[self.sp]
                self.sp = (self.sp + 1) & 0xFF
                self.pc += 2

            else:
                print(f"Unknown instruction: {self.ram[self.pc]}")
                sys.exit(1)
