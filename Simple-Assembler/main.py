label = {}  # dict for storing or labels and their mem locations
vars = {}  # dict for storing or labels and their mem locations
boolvar = True  # boolean to check if any instruction has been passed or not
halt = False  # boolean to check if halt has been called or not
counter = 0  # program counter
linenum = 0  # line number
memory_address = []
assembly_code = []
real_lines_of_code = 0
asm_with_spaces = []
# stores all the instruction of ISA and opcodes
opcodes = {'add': '00000', 'sub': '00001', 'mov1': '00010', 'mov2': '00011', 'ld': '00100', 'st': '00101',
           'mul': '00110', 'div': '00111',
           'rs': '01000', 'ls': '01001', 'xor': '01010', 'or': '01011', 'and': '01100', 'not': '01101', 'cmp': '01110',
           'jmp': '01111', 'jlt': '10000', 'jgt': '10001', 'je': '10010', 'hlt': '10011'}

# stores the type
opcodes_type = {'add': 'A', 'sub': 'A', 'mov1': 'B', 'mov2': 'C', 'ld': 'D', 'st': 'D', 'mul': 'A', 'div': 'C',
                'rs': 'B', 'ls': 'B', 'xor': 'A', 'or': 'A', 'and': 'A', 'not': 'C', 'cmp': 'C',
                'jmp': 'E', 'jlt': 'E', 'jgt': 'E', 'je': 'E', 'hlt': 'F'}
# registers and their binary representation
registers = {'R0': '000', 'R1': '001', 'R2': '010', 'R3': '011', 'R4': '100', 'R5': '101', 'R6': '110', 'FLAGS': '111'}
# unused bits for each type of representation
unused_bits = {'A': '00', 'B': '', 'C': '00000', 'D': '', 'E': '000', 'F': '00000000000'}
halt_checker = False
# name of registers except FLAG register
register_names = ['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6']
error_hai_kya = False
var_error = {}
global_input_line = 0
