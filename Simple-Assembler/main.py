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
def check_label_and_variable_naming_convention(varlabel):
    # real_line_count : program counter ,i.e. real lines of code which use up memory
    # vars is a dictionary of variables with keys as variable names and values as NONE initially
    if varlabel in opcodes_type.keys() or varlabel in registers.keys():
        return False

    for j in range(len(varlabel)):
        if not (varlabel[j].isalnum()):
            if varlabel[j] != '_':
                return False
    return True

def allocate_memory_to_var(real_line_count, vars):
    for allocate in vars.keys():
        bin_8bit_num = format(real_line_count, '#010b')
        vars[allocate] = bin_8bit_num[2:]
        real_line_count += 1
    return vars

def assembly_to_binary(assembly_code):
    binary_code = []
    for i in range(len(assembly_code)):
        bin_out = ''
        assembly_line_i = assembly_code[i]
        # print(assembly_line_i)
        if assembly_line_i[0] == 'var':
            continue
        if assembly_line_i[0][-1] == ':':
            assembly_line_i = assembly_line_i[1:]
        if assembly_line_i[0] in opcodes.keys() or assembly_line_i[0] == 'mov':
            if (assembly_line_i[0] == 'mov'):
                if (assembly_line_i[2][1:].isdigit() and assembly_line_i[2][0] == '$'):
                    assembly_line_i[0] = 'mov1'
                else:
                    assembly_line_i[0] = 'mov2'
            # print(assembly_line_i[0])
            bin_out += opcodes[assembly_line_i[0]]
            bin_out += unused_bits[opcodes_type[assembly_line_i[0]]]
            # print(bin_out)
            # print(opcodes_type[assembly_line_i[0]])
            if opcodes_type[assembly_line_i[0]] == 'A':
                bin_out += registers[assembly_line_i[1]] + registers[assembly_line_i[2]] + registers[assembly_line_i[3]]
            if opcodes_type[assembly_line_i[0]] == 'B':
                bin_out += registers[assembly_line_i[1]] + format(int(assembly_line_i[2][1:]), '#010b')[2:]
            if opcodes_type[assembly_line_i[0]] == 'C':
                bin_out += registers[assembly_line_i[1]] + registers[assembly_line_i[2]]
            if opcodes_type[assembly_line_i[0]] == 'D':
                bin_out += registers[assembly_line_i[1]] + vars[assembly_line_i[2]]
            if opcodes_type[assembly_line_i[0]] == 'E':
                bin_out += label[assembly_line_i[1]]
            if opcodes_type[assembly_line_i[0]] == 'F':
                bin_out += ''
            # print(bin_out)
            binary_code += [bin_out]
    return binary_code

def check_syntax(lst):  # checks syntactical errors ,i.e if a command is in its correct fomrat
    if len(lst) != 0:
        if lst[0] == 'mov':  # special check for 'mov' as it has two types
            if (len(lst) == 3):  # mov instruction should be of len 3
                return True
            else:
                return False
        elif lst[0] == 'mov1' or lst[0] == 'mov2':
            return True
        elif lst[0] in opcodes.keys():  # other instructions except mov
            if opcodes_type[lst[0]] == 'A':  # if type A ,length should be 4 followed by 3 valid register names
                if len(lst) == 4:
                    return True
                else:
                    return False
            elif opcodes_type[lst[0]] == 'B':  # if type B, len =3 followed by register and imm value
                if len(lst) == 3:
                    if lst[2][0] != "$":
                        return False
                    else:
                        return True
                else:
                    return False
            elif opcodes_type[lst[0]] == 'C':  # if type C ,len 3 and 2 valid register names
                if len(lst) == 3:
                    return True
                else:
                    return False
            elif opcodes_type[lst[0]] == 'D':  # if type D ,len 3, register and label name
                if len(lst) == 3:
                    return True
                else:
                    return False
            elif opcodes_type[lst[0]] == 'E':  # type E len 2,command and  label name
                if len(lst) == 2:
                    return True
                else:
                    return False
            elif opcodes_type[lst[0]] == 'F':  # halt statement
                if len(lst) == 1:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return True
    else:
        # modified statement
        return False

