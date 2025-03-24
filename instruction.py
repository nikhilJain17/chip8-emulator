import enum
class Instruction:
    """Class encapsulating binary instructions

    - type of instr
    - operands? will need to make lots of diff subclasses etc
        - naur just process in opcode execution helper functions
    - binary repr
    """
    def __init__(self, instr_bytes):
        self.instr = instr_bytes.hex()
        self.opcode = self.get_opcode()

    def get_opcode(self):
        """Tag instruction with opcode metadata
        """
        if self.instr[0] == "8" and self.instr[3] in set(["1", "2", "3", "6", "E"]):
                return OpType.BITOP
        elif self.instr[0] == "8" and self.instr[3] in set(["4", "5", "7"]):
             return OpType.MATH
        return OpType.UNKNOWN
    
    def __str__(self):
        return(self.opcode.name + ":" + self.instr)


class OpType(enum.Enum):
    # from https://en.wikipedia.org/wiki/CHIP-8#Opcode_table
    DISPLAY = 1
    FLOW = 2
    COND = 3
    CONST = 4
    ASSIGN = 5
    BITOP = 6
    MATH = 7
    MEM = 8
    RAND = 9
    KEYOP = 10
    TIMER = 11
    SOUND = 12
    BCD = 13
    UNKNOWN = 14

