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
        elif binary[:5] == "00101":
            binary_file[int(binary[8:], 2)] = format(register_value[int(binary[5:8], 2)], '016b')
            graph_plotter += [int(binary[8:], 2)]
            cycle_number += [cycle_count]
            register_value[7] = 0
            print_register_state()

        elif binary[:5] == "00110":
            reg1 = int(binary[7:10], 2)
            reg2 = int(binary[10:13], 2)
            reg3 = int(binary[13:], 2)
            register_value[reg1] = register_value[reg2] * register_value[reg3]
            register_value[7] = 0

            if register_value[reg1] > 65535:
                temp = bin(register_value[reg1])[2:]
                temp = temp[-16:]
                register_value[7] = 8
                register_value[reg1] = int(temp, 2)
            print_register_state()

        elif binary[:5] == "00111":
            reg3 = int(binary[10:13], 2)
            reg4 = int(binary[13:], 2)
            register_value[0] = (register_value[reg3]) // (register_value[reg4])
            register_value[1] = (register_value[reg3]) % (register_value[reg4])
            register_value[7] = 0
            print_register_state()

        elif binary[:5] == "01000":
            temp = "0"*int(binary[8:], 2) + format(int(bin(register_value[int(binary[5:8], 2)])[2:], 2), '016b')
            if len(temp) > 16:
                temp = temp[:16]
            register_value[int(binary[5:8], 2)] = int(temp, 2)
            register_value[7] = 0
            print_register_state()

        elif binary[:5] == "01001":
            temp = bin(register_value[int(binary[5:8], 2)])[2:] + "0"*int(binary[8:], 2)
            if len(temp) > 16:
                temp = temp[-16:]
            register_value[int(binary[5:8], 2)] = int(temp, 2)
            register_value[7] = 0
            print_register_state()

        elif binary[:5] == "01010":
            register_value[7] = 0
            reg1 = int(binary[7:10], 2)
            reg2 = int(binary[10:13], 2)
            reg3 = int(binary[13:], 2)
            register_value[reg1] = register_value[reg2] ^ register_value[reg3]
            print_register_state()

        elif binary[:5] == "01011":
            register_value[7] = 0
            reg1 = int(binary[7:10], 2)
            reg2 = int(binary[10:13], 2)
            reg3 = int(binary[13:], 2)
            register_value[reg1] = register_value[reg2] | register_value[reg3]
            print_register_state()
        elif binary[:5] == "01100":
            register_value[7] = 0
            reg1 = int(binary[7:10], 2)
            reg2 = int(binary[10:13], 2)
            reg3 = int(binary[13:], 2)
            register_value[reg1] = register_value[reg2] & register_value[reg3]
            print_register_state()

        elif binary[:5] == "01101":
            register_value[7] = 0
            reg1 = int(binary[10:13], 2)
            reg2 = int(binary[13:], 2)
            register_value[reg1] = 65535 - register_value[reg2]
            print_register_state()

        elif binary[:5] == "01110":
            reg1 = int(binary[10:13], 2)
            reg2 = int(binary[13:], 2)
            if register_value[reg1] == register_value[reg2]:
                register_value[7] = 1
            elif register_value[reg1] > register_value[reg2]:
                register_value[7] = 2
            else:
                register_value[7] = 4
            print_register_state()

        elif binary[:5] == "01111":
            temp_mem_add = binary[8:]
            # check here
            register_value[7] = 0
            print_register_state()
            program_counter = int(temp_mem_add, 2) - 1

        elif binary[:5] == "10000":
            if register_value[7] == 4:
                temp_mem_add = binary[8:]
                register_value[7] = 0
                print_register_state()
                program_counter = int(temp_mem_add, 2) - 1
            else:
                register_value[7] = 0
                print_register_state()

        elif binary[:5] == "10001":
            temp_mem_add = binary[8:]
            if register_value[7] == 2:
                register_value[7] = 0
                print_register_state()
                program_counter = int(temp_mem_add, 2) - 1
            else:
                register_value[7] = 0
                print_register_state()

        elif binary[:5] == "10010":
            temp_mem_add = binary[8:]
            if register_value[7] == 1:
                register_value[7] = 0
                print_register_state()
                program_counter = int(temp_mem_add, 2) - 1
            else:
                register_value[7] = 0
                print_register_state()

        program_counter += 1
        cycle_count += 1
    memory_dump()
    plt.scatter(cycle_number, graph_plotter)
    plt.xlabel("Cycle Number")
    plt.ylabel("Memory Address")
    plt.title("Scatter Plot")
    plt.show()

