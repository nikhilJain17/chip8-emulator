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
            if instr.optype == OpType.MATH:
                self.execute_math_instr(instr)
                self.dump_registers()
            elif instr.optype == OpType.BITOP:
                self.dump_registers()
                pass
            elif instr.optype == OpType.UNKNOWN:
                print("Unknown instruction", instr)
                # raise ValueError("Unknown instruction", instr)
            else:
                raise ValueError("Operation type is not set", instr)

    def execute_math_instr(self, instr):
        reg_x, reg_y = int(instr[1]), int(instr[2])
        tmp = None
        if reg_x < 0 or reg_x > 16:
            raise ValueError("Invalid data register operand", instr, reg_x) 
        if reg_y < 0 or reg_y > 16:
            raise ValueError("Invalid data register operand", instr, reg_x) 
        if instr[3] == "4":
            tmp = self.data_registers[reg_x] + self.data_registers[reg_y]
        elif instr[3] == "5":
            tmp = self.data_registers[reg_x] - self.data_registers[reg_y]
        elif instr[3] == "7":
            tmp = self.data_registers[reg_y] - self.data_registers[reg_x]       
        self.data_registers[reg_x] = tmp % 0xF
        # Overflow bit is stored in register VF 
        if tmp > 0xF or tmp < 0x0:
            self.data_registers[-1] = 1
        else:
            self.data_registers[-1] = 0


    def dump_registers(self):
        s = ""
        for i in range(len(self.data_registers)):
            s += "(V" + str(i) + ": " + hex(self.data_registers[i]) + ")\t"
            if (i + 1) % 4 == 0:
                s += "\n"
        s += "(I: " + hex(self.addr_register) + ")"
        print(s)