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

def Type(lst):
    # to return type of instruction
    if len(lst) == 0: # if its an only label line return Z
        return "Z"
    if lst[0] in ["add","sub","mul","xor","or","and"]:
        return "A"
    elif lst[0] in ["ld","st"]:
        return "D"
    elif lst[0] in ["jmp","jlt","jgt","je"]:
        return "E"
    elif lst[0] == "hlt":
        return "F"
    elif lst[0] in ["rs","ls"]:
        return "B"
    elif lst[0] in ["not","cmp","div"]:
        return "C"
    elif lst[0] == "mov": # special checks for mov
        if len(lst) >= 3:
            if lst[2][0] == '$':
                return "B"
            elif lst[2][0] == "R" or lst[2] == "FLAGS":
                return "C"
            else:
                return "Z"
        else:
            return "Z"
    else:
        return "Z"

def typocheck(lst):
    if len(lst) == 0: #if length is 0 means without the label there is no instruction hence shoud fail the check which will prevent the counter+1
        return True
    else:
        if lst[0] not in ["add","sub","mov","ld","st","mul","div","rs","ls","xor","or",
                      "and","not","cmp","jmp","jlt","jgt","je","hlt","var"]: # if first word doesnt match any instruction
            return False
        else:
            # print(Type(lst) ,lst)
            if Type(lst) == "A":
                if(len(lst)==4):
                    if lst[1] in registers.keys() and lst[2] in registers.keys() and lst[3] in registers.keys():
                        return True
                    else:
                        return False
                else:
                    return True
            elif Type(lst) == "B":
                if len(lst) == 3:
                    if lst[1] in registers.keys(): # if 2nd word doesnt match any flag
                        return True
                    else:
                        return False

                else:
                    return True
            elif Type(lst) == "C":

                if len(lst) == 3:
                    if lst[1] in registers.keys() and lst[2] in registers.keys():
                        return True
                    else:
                        return False
                else:
                    return True

            elif Type(lst) == "D":
                if len(lst)==3:
                    if lst[1] in registers.keys():
                        return True
                    else:
                        return False
                else:
                    return False
            elif Type(lst) == "E":
                # the mem_addr is nothing but label and label checking is done with undeflabelcheck
                return True
            elif Type(lst) == "F":
                return True
            elif Type(lst) == 'Z':
                if (lst[0]== 'mov'):
                    if(len(lst)==3):
                         if lst[2][0] == "$":
                             return True
                         elif lst[2] in registers.keys():
                             return True
                         else:
                             return False

                    else:
                        return True
                else:
                    return False
            else:
                return False

def undefvarcheck(lst):
    if Type(lst) == "D" and len(lst) == 3:
        if lst[2] not in vars.keys():  # check to see if var dict has associated key or not
            return False
        return True
    else:
        return True

def undeflabelcheck(lst):
    if Type(lst) == "E" and len(lst) == 2:
        if lst[0] != "var":
            if lst[1] not in label.keys():  # check to see if label dict has associated key or not
                return False
            return True
        else:
            return True
    else:
        return True

def illflagcheck(lst):
    # buggy AF
    if 'FLAGS' in lst and len(lst) >= 2:
        if lst[0] != 'mov' or lst.index('FLAGS') != 2:
            return False
        else:
            return True
    else:
        return True

def illvalcheck(lst):
    if Type(lst) == "B" and len(lst) == 3:
        if(lst[2][0] != "$"):
            return True
        if(lst[2][1:].isdigit() and lst[2][0]=='$'):
            if int(lst[2][1:]) < 0 or int(lst[2][1:]) > 255:  # if 3rd word (without the $ sign) not in between 0 and 255
                return False
            return True
        else:
            return False
    else:
        return True

def mislabelvar(lst):
    # if type is E then check if the 2nd word is in var or not
    if Type(lst) == "E" and len(lst) == 2:
        if lst[1] in vars.keys() and check_label_and_variable_naming_convention(lst[1]):
            ret = False
        else:
            ret = True
    # if type is D then check if 3rd word is in label or not
    elif Type(lst) == "D" and len(lst) == 3:
        if lst[2] in label.keys() and check_label_and_variable_naming_convention(lst[2]):
            ret = False
        else:
            ret = True
    else:
        ret = True
    return ret

def errorcheck(lst):
    global linenum,error_hai_kya
    # linenum += 1
    check1 = typocheck(lst)  # typo check
    check2 = undefvarcheck(lst)  # undefined variable check
    check3 = undeflabelcheck(lst)  # undefined label check
    check4 = illflagcheck(lst)  # illegal flag check
    check5 = illvalcheck(lst)  # illegal immediate value check
    check6 = mislabelvar(lst)  # mis label/variable check
    check10 = check_syntax(lst)
    global counter
    if not check1:
        print("ERROR: Typos in instruction name or register name at line " + str(linenum + 1))
    if not check2:
        print("ERROR: Use of undefined variables at line " + str(linenum + 1))
    if not check3:
        print("ERROR: Use of undefined labels at line " + str(linenum + 1))
    if not check4:
        print("ERROR: Illegal use of FLAGS register at line " + str(linenum + 1))
    if not check5:
        print("ERROR: Illegal Immediate values (less than 0 or more than 255 or non-numeric) at line " + str(linenum + 1))
    if not check6:
        print("ERROR: Misuse of labels as variables or vice-versa at line " + str(linenum + 1))
    if not check10:
        print("ERROR: Wrong syntax used for instructions at line " + str(linenum + 1))

    if not(check1 and check2 and check3 and check4 and check5 and check6 and check10):
       # print('here')
        error_hai_kya = True
           
