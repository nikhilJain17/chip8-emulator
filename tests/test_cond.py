from src.cpu import CPU
"""
There are 4 COND instructions to skip the next instruction
3XNN	if (Vx == NN)	
4XNN	if (Vx != NN)	
5XY0	if (Vx == Vy)	
9XY0	if (Vx != Vy)	

From https://en.wikipedia.org/wiki/CHIP-8#Opcode_table
"""

def test_eq_const():
    """
    Test skipping eq const over one load instruction to the next load instruction
    """ 
    program = bytearray([
        0x61, 0xBD, # load 0xBD into V1
        0x31, 0xBD, # if V1 == 0xBD, skip next line
        0x62, 0x01, # load 0x01 into V2
        0x63, 0x02  # load 0x01 into V3 
    ])
    cpu = CPU(program)
    cpu.execute()
    cpu.dump_registers()
    assert cpu.data_registers[1] == 0xBD
    assert cpu.data_registers[2] == 0x00
    assert cpu.data_registers[3] == 0x02

def test_neq_const():
    """
    Test skipping neq const over one load instruction to the next load instruction
    """ 
    program = bytearray([
        0x61, 0xBD, # load 0xBD into V1
        0x41, 0xB0, # if V1 != 0xB0, skip next line
        0x62, 0x01, # load 0x01 into V2
        0x63, 0x02  # load 0x01 into V3 
    ])
    cpu = CPU(program)
    cpu.execute()
    cpu.dump_registers()
    assert cpu.data_registers[1] == 0xBD
    assert cpu.data_registers[2] == 0x00
    assert cpu.data_registers[3] == 0x02

def test_eq_reg():
    """
    Test skipping eq reg over one load instruction to the next load instruction
    """
    program = bytearray([
        0x61, 0xBD, # load 0xBD into V1
        0x62, 0xBD, # load 0xBD into V2
        0x51, 0x20, # if V1 == V2, skip next line
        0x63, 0x01, # load 0x01 into V3
        0x64, 0x02  # load 0x01 into V4
    ])
    cpu = CPU(program)
    cpu.execute()
    cpu.dump_registers()
    assert cpu.data_registers[1] == 0xBD
    assert cpu.data_registers[2] == 0xBD
    assert cpu.data_registers[3] == 0x00
    assert cpu.data_registers[4] == 0x02

def test_neq_reg():
    """
    Test skipping neq reg over one load instruction to the next load instruction
    """
    program = bytearray([
        0x61, 0xBD, # load 0xBD into V1
        0x62, 0xB0, # load 0xB0 into V2
        0x91, 0x20, # if V1 != V2, skip next line
        0x63, 0x01, # load 0x01 into V3
        0x64, 0x02  # load 0x01 into V4
    ])
    cpu = CPU(program)
    cpu.execute()
    cpu.dump_registers()
    assert cpu.data_registers[1] == 0xBD
    assert cpu.data_registers[2] == 0xB0
    assert cpu.data_registers[3] == 0x00
    assert cpu.data_registers[4] == 0x02

