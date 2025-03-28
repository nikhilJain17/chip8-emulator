from src.cpu import CPU

def test_register_add():
    """
    Addition, no overflow
    Load 0x3 into V1, load 0x4 into V3, V1 := V1 + V3
    """
    program = bytearray([
        0x61, 0x03,
        0x64, 0x04,
        0x81, 0x44
    ])
    add_cpu = CPU(program)
    # print("foo", add_cpu.program.hex())
    add_cpu.execute()
    add_cpu.dump_registers()
    assert add_cpu.data_registers[1] == 0x7
    assert add_cpu.data_registers[4] == 0x4
    assert add_cpu.data_registers[0xF] == 0x0

def test_register_add_overflow():
    """
    Addition with overflow
    Load 0xFF into V2, 0xA into V0, V0 := V0 + V2, VF is set
    0xFF + 0xA = 0x109
    """
    program = bytearray([
        0x62, 0xFF,
        0x60, 0x0a,
        0x80, 0x24
    ])
    overflow_cpu = CPU(program)
    overflow_cpu.execute()
    overflow_cpu.dump_registers()
    assert overflow_cpu.data_registers[2] == 0xFF
    assert overflow_cpu.data_registers[0] == 0x9
    assert overflow_cpu.data_registers[0xF] == 0x1

def test_register_sub():
    """
    Subtraction no overflow
    Load 0x0A into V5, 0x2 into V3, V5 := V5 - V3 
    """
    program = bytearray([
        0x65, 0x0A,
        0x63, 0x02,
        0x85, 0x35
    ])
    cpu = CPU(program)
    assert cpu.data_registers[3] == 0x2
    assert cpu.data_registers[5] == 0x8
    assert cpu.data_registers[0xF] == 0x0
