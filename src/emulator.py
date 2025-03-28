import argparse
import cpu as cpu

class Emulator:
    """Loads program and sets up CPU, which orchestrates and delegates
    other components such as memory, APU, graphics, registers
    """

    def __init__(self, program_file):
        self.program_file = program_file
        self.program = self.load_program()
    
    def load_program(self):
        """Loads raw binary program from disk
        """
        with open(self.program_file, "rb") as f:
            return bytearray(f.read())

    def emulate(self):
        """Launches program execution
        """
        chip8 = cpu.CPU(self.program)
        chip8.execute()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--program", required=True)
    args = parser.parse_args()
    emulator = Emulator(args.program)
    emulator.emulate()
