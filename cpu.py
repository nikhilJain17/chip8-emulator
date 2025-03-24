from instruction import Instruction, OpType

class CPU:
    def __init__(self, program):
        self.pc = 0x000
        self.program = program
        self.stack = [0x0 for _ in range(48)] # 48 byte stack
        self.mem = [0x0 for _ in range(4000)] # 4k memory
        # 16 data registers, 1 addr register
        self.data_registers = [0x00 for _ in range(16)] 
        self.addr_register = 0x000
    
    def execute(self):
        for self.pc in range(0,len(self.program),2):
            self.curr_instr = Instruction(self.program[self.pc:self.pc+2])
            print(self.pc, self.curr_instr)
            if self.curr_instr.optype == OpType.MATH:
                self.execute_math_instr()
                self.dump_registers()
            elif self.curr_instr.optype == OpType.BITOP:
                pass
            elif self.curr_instr.optype == OpType.CONST:
                self.execute_const_instr()
                self.dump_registers()
            elif self.curr_instr.optype == OpType.ASSIGN:
                self.execute_assign_instr()
                self.dump_registers()
            elif self.curr_instr.optype == OpType.UNKNOWN:
                # raise ValueError("Unknown instruction", instr)
                pass
            else:
                raise ValueError("Operation type is not set", self.curr_instr)

    def execute_assign_instr(self):
        reg_x, reg_y = int(self.curr_instr.bytes[1], 16), int(self.curr_instr.bytes[2], 16)
        self.validate_register_operand(reg_x)
        self.validate_register_operand(reg_y)
        self.data_registers[reg_x] = self.data_registers[reg_y]

    def execute_const_instr(self):
        reg_x = int(self.curr_instr.bytes[1], 16)
        self.validate_register_operand(reg_x)
        const = int(self.curr_instr.bytes[2:], 16)
        if self.curr_instr.bytes[0] == "6":
            self.data_registers[reg_x] = const
        elif self.curr_instr.bytes[0] == "7":
            self.data_registers[reg_x] += const

    def execute_math_instr(self):
        reg_x, reg_y = int(self.curr_instr[1], 16), int(self.curr_instr[2], 16)
        tmp = None
        self.validate_register_operand(reg_x) 
        self.validate_register_operand(reg_y) 
        if self.curr_instr.bytes[3] == "4":
            tmp = self.data_registers[reg_x] + self.data_registers[reg_y]
        elif self.curr_instr.bytes[3] == "5":
            tmp = self.data_registers[reg_x] - self.data_registers[reg_y]
        elif self.curr_instr.bytes[3] == "7":
            tmp = self.data_registers[reg_y] - self.data_registers[reg_x]       
        self.data_registers[reg_x] = tmp % 0x100
        # Overflow bit is stored in register VF 
        if tmp > 0xF or tmp < 0x0:
            self.data_registers[-1] = 1
        else:
            self.data_registers[-1] = 0

    def validate_register_operand(self, x):
        if x < 0 or x > 16:
            raise ValueError("Invalid register operand", x, "for instruction", self.curr_instr)

    def dump_registers(self):
        s = "_" * 80 + "\n\tREGISTERS\n"
        for i in range(len(self.data_registers)):
            s += "(V" + ("%x" % i) + ": " + hex(self.data_registers[i]) + ")\t"
            if (i + 1) % 4 == 0:
                s += "\n"
        s += "(I: " + hex(self.addr_register) + ")\n" + "_" * 80 + "\n"
        print(s)