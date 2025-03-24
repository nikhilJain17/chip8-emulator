import enum
class Instruction:
    def __init__(self, instr_bytes):
        self.bytes = instr_bytes.hex()
        self.optype = self.get_optype()

    def get_optype(self):
        """Tag instruction with operation type metadata
        """
        if self.bytes[0] == "8" and self.bytes[3] in set(["1", "2", "3", "6", "E"]):
            return OpType.BITOP
        elif self.bytes[0] == "8" and self.bytes[3] in set(["4", "5", "7"]):
            return OpType.MATH
        elif self.bytes[0] == "6" or self.bytes[0] == "7":
            return OpType.CONST
        return OpType.UNKNOWN
    
    def __str__(self):
        return(self.optype.name + ":" + self.bytes)


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

