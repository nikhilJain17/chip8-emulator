from instruction import Instruction, OpType

class CPU:
    def __init__(self, program):
        self.pc = 0x000
        self.program = program
        self.stack = [0x0 for _ in range(48)] # 48 byte stack
        self.mem = [0x0 for _ in range(4000)] # 4k memory
        # 16 data registers, 1 addr register
        self.data_registers = [0x0 for _ in range(16)] 
        self.addr_register = 0x000
    
    def execute(self):
        for self.pc in range(0,len(self.program),2):
            instr = Instruction(self.program[self.pc:self.pc+2])
            print(self.pc, instr)
            if instr == "00e0":
                print("Clear display")
