if __name__ == "__main__":
    while True:  # true because it will run infinitely until EOF is reached
        try:
            line = input()  # trying input from stdin, might encounter EOF
        except EOFError:
            break
        else:
            binary_file += [line]

    for i in range(len(binary_file), 256):
        # populating memory with zeroes
        binary_file += ["0" * 16]
    while True:
        # storing PC for plotting purposes later
        graph_plotter += [program_counter]
        # storing current cycle num in an array
        cycle_number += [cycle_count]
        # terminating condition if halt is encountered
        if binary_file[program_counter] == "1001100000000000":
            # reset flag registers
            register_value[7] = 0  # added line
            print_register_state()
            break
        # extracting binary code in that line
        binary = binary_file[program_counter]
        # if opcode is of sum
        if binary[:5] == "00000":
            # reset flag
            register_value[7] = 0
            # extract register numbers
            reg1 = int(binary[7:10], 2)
            reg2 = int(binary[10:13], 2)
            reg3 = int(binary[13:], 2)
            # perform add operation
            register_value[reg1] = register_value[reg2] + register_value[reg3]
            # check for overflow
            if register_value[reg1] > 65535:
                temp = bin(register_value[reg1])[2:]
                # take 16 LSB
                temp = temp[-16:]
                # set overflow bit in flag register
                register_value[7] = 8
                # store valid value in register
                register_value[reg1] = int(temp, 2)
            print_register_state()

        elif binary[:5] == "00001":
            register_value[7] = 0
            reg1 = int(binary[7:10], 2)
            reg2 = int(binary[10:13], 2)
            reg3 = int(binary[13:], 2)
            register_value[reg1] = register_value[reg2] - register_value[reg3]
            if register_value[reg1] < 0:
                register_value[reg1] = 0
                register_value[7] = 8
            print_register_state()

        elif binary[:5] == "00010":
            # reg1 = imm
            register_value[int(binary[5:8], 2)] = int(binary[8:], 2)
            register_value[7] = 0
            print_register_state()

        elif binary[:5] == "00011":
            # reg1 = reg2
            register_value[int(binary[10:13], 2)] = register_value[int(binary[13:], 2)]
            register_value[7] = 0
            print_register_state()

        elif binary[:5] == "00100":
            register_value[int(binary[5:8], 2)] = int(binary_file[int(binary[8:], 2)], 2)
            graph_plotter += [int(binary[8:], 2)]
            cycle_number += [cycle_count]
            register_value[7] = 0
            # changed line
            print_register_state()

        elif binary[:5] == "00101":
            binary_file[int(binary[8:], 2)] = format(register_value[int(binary[5:8], 2)], '016b')
            graph_plotter += [int(binary[8:], 2)]
            cycle_number += [cycle_count]
            register_value[7] = 0
            print_register_state()