from instruction import Instruction, OpType
from display import Display

class CPU:
    FONT_DATA = [
        0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
        0x20, 0x60, 0x20, 0x20, 0x70,  # 1
        0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
        0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
        0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
        0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
        0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
        0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
        0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
        0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
        0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
        0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
        0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
        0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
        0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
        0xF0, 0x80, 0xF0, 0x80, 0x80,  # F
    ]

    def __init__(self, program):
        self.pc = 0x000
        self.program = program
        self.stack = [0x0 for _ in range(48)] # 48 byte stack
        self.mem = [0x0 for _ in range(4000)] # 4k memory
        self.mem[0x50:0x9F] = self.FONT_DATA
        # 16 data registers, 1 addr register
        self.data_registers = [0x00 for _ in range(16)] 
        self.addr_register = 0x000
        self.display = Display()
    
    def execute(self):
        for self.pc in range(0,len(self.program),2):
            self.curr_instr = Instruction(self.program[self.pc:self.pc+2])
            # print(self.pc, self.curr_instr)
            if self.curr_instr.optype == OpType.MATH:
                self.execute_math_instr()
                # self.dump_registers()
            elif self.curr_instr.optype == OpType.BITOP:
                pass
            elif self.curr_instr.optype == OpType.CONST:
                self.execute_const_instr()
                # self.dump_registers()
            elif self.curr_instr.optype == OpType.ASSIGN:
                self.execute_assign_instr()
                # self.dump_registers()
            elif self.curr_instr.optype == OpType.MEM:
                self.execute_mem_instr()
            elif self.curr_instr.optype == OpType.DISPLAY:
                self.execute_display_instr()
                pass
            elif self.curr_instr.optype == OpType.COND:
                self.execute_cond_instr()
            elif self.curr_instr.optype == OpType.UNKNOWN:
                # print("unknown", self.pc, self.curr_instr)

                # raise ValueError("Unknown instruction", instr)
                pass
            else:
                raise ValueError("Operation type is not set", self.curr_instr)

    def execute_cond_instr(self):
        if self.curr_instr.bytes[0] == "3" or self.curr_instr.bytes[0] == "4":
            reg_x = int(self.curr_instr.bytes[1], 16)
            self.validate_register_operand(reg_x)
            val = self.curr_instr.bytes[2:]
            should_skip = (self.curr_instr.bytes[0] == "3" and self.data_registers[reg_x] == val) \
                or (self.curr_instr.bytes[0] == "4" and self.data_registers[reg_x] != val)
            if should_skip:
                self.pc += 2
        elif (self.curr_instr.bytes[0] == "5" or self.curr_instr == "9") and self.curr_instr.bytes[-1] == "0":
            reg_x = int(self.curr_instr.bytes[1], 16)
            reg_y = int(self.curr_instr.bytes[2], 16)
            self.validate_register_operand(reg_x)
            self.validate_register_operand(reg_y)
            should_skip = (self.curr_instr.bytes[0] == "5" and self.data_registers[reg_x] == self.data_registers[reg_y]) \
                or (self.curr_instr.bytes[0] == "9" and self.data_registers[reg_x] != self.data_registers[reg_y])
            if should_skip:
                self.pc += 2

    def execute_display_instr(self):
        if self.curr_instr.bytes[0] == "d":
            # print("display", self.curr_instr)
            # pull sprite data from memory
            reg_x, reg_y, n = int(self.curr_instr.bytes[1], 16), int(self.curr_instr.bytes[2], 16), int(self.curr_instr.bytes[3], 16)
            self.validate_register_operand(reg_x)
            self.validate_register_operand(reg_y)
            sprite_rows = self.mem[self.addr_register : self.addr_register + n]
            # expand bytes to bits
            collision_detected = self.display.draw(reg_x, reg_y, sprite_rows)
            if collision_detected:
                self.data_registers[-1] = 1
            else:
                self.data_registers[-1] = 0
        elif self.curr_instr.bytes[0] == "a":
            self.addr_register = int(self.curr_instr[1:], 16)

    def execute_mem_instr(self):
        # 4 memory instructions
        print("curr instr", self.curr_instr)
        if self.curr_instr.bytes[0] == "a":
            self.addr_register = int(self.curr_instr.bytes[1:], 16)
            return
        reg_x = self.curr_instr.bytes[1]
        if self.curr_instr.bytes[2:] == "1e":
            self.validate_register_operand(reg_x)
            self.addr_register += self.data_registers[reg_x]
        elif self.curr_instr.bytes[2:] == "29":
            # I = sprite_addr[Vx]	
            nibble = self.data_registers[reg_x] % 0x10
            self.addr_register = 0x50 + nibble * 5
        elif self.curr_instr.bytes[2:] == "55":
            # register range dump
            for i in range(reg_x + 1):
                self.mem[self.addr_register + i] = self.data_registers[i]
        elif self.curr_instr.bytes[2:] == "65":
            # register range load
            for i in range(reg_x + 1):
                self.data_registers[i] = self.mem[self.addr_register + i]


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
        reg_x, reg_y = int(self.curr_instr.bytes[1], 16), int(self.curr_instr.bytes[2], 16)
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
        if tmp > 0xFF or tmp < 0x0:
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