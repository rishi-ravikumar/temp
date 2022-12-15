import sys
import os
import random
from rv2_stdlib import *

## Global Variables

# get source filename
source_fn = sys.argv[1]
tokenized_filename = source_fn.split(".")
# storing destination filename
dest_fn = tokenized_filename[0] + ".s"
dest_tmp_asm_fn = tokenized_filename[0] + "_asm.tmp.ri"
dest_tmp_stack_fn = tokenized_filename[0] + "_stack.tmp.ri"
dest_tmp_vars_fn = tokenized_filename[0] + "_vars.tmp.ri"
# open source and destination files
src = open(source_fn, "r")
# empty dest and open it in append mode
dest = open(dest_fn, "w")
dest.close()
dest = open(dest_fn, "a+")
# empty dest_asm and open it in append mode
dest_asm = open(dest_tmp_asm_fn, "w")
dest_asm.close()
dest_asm = open(dest_tmp_asm_fn, "a+")
# empty dest_stack and open it in append mode
dest_stack = open(dest_tmp_stack_fn, "w")
dest_stack.close()
dest_stack = open(dest_tmp_stack_fn, "a+")
# empty dest_vars and open it in append mode
dest_vars = open(dest_tmp_vars_fn, "w")
dest_vars.close()
dest_vars = open(dest_tmp_vars_fn, "a+")
variables = []

# set of generated random numbers
rnd_nums = []

def generate_unique_number():
    num = random.randint(0 , 1000)
    while(num in rnd_nums):
        num = random.randint(0 , 1000)
    rnd_nums.append(num)
    return num

# plays the specified note
def play_note(tokens):
    wl(dest_asm, "")
    wl(dest_asm, "; " + tokens[0] + " " + tokens[1] + " " + tokens[2] + " " + tokens[3])
    note = tokens[1]
    octave = tokens[2]
    duration = tokens[3]
    note_value = get_note_value(note, octave, duration)
    unique_number = str(generate_unique_number())
    label = "note_" + unique_number
    push(dest_asm)

    wl(dest_asm, "ld r2, " + label)
    # this function assumes that r2 contains the note value
    wl(dest_asm, "play_note_" + unique_number)
    wl(dest_asm, "ld r3, buzzer_checker_" + unique_number)
    wl(dest_asm, "ld r3, [r3]")
    wl(dest_asm, "ands r0, r3, #1")
    wl(dest_asm, "bne play_note_" + unique_number)
    wl(dest_asm, "ld r3, buzzer_" + unique_number)
    wl(dest_asm, "st r2, [r3]")

    wl(dest_asm, "b skip_" + unique_number)
    wl(dest_asm, label + " defw " + note_value)
    wl(dest_asm, "buzzer_checker_" + unique_number + " defw $ff93")
    wl(dest_asm, "buzzer_" + unique_number + " defw $ff92")
    wl(dest_asm, "skip_" + unique_number)

    pull(dest_asm)

# allows for delay in terms of the number of instructions
def delay_inst(tokens):
    wl(dest_asm, "")
    wl(dest_asm, "; " + tokens[0] + " " + tokens[1])
    unique_number = str(generate_unique_number())
    push(dest_asm)

    if tokens[1].isdigit():
        wl(dest_asm, "b skip_" + unique_number)
        wl(dest_asm, "delay_inst_" + unique_number + " defw " + str(tokens[1]))
        wl(dest_asm, "skip_" + unique_number)
        wl(dest_asm, "ld r2, " + "delay_inst_" + unique_number)
    else:
        get_var_val(tokens[1], "r5")
        wl(dest_asm, "mov r2, r5")
    
    # r2 contains the delay time in terms of the number of instructions
    wl(dest_asm, "delay_inst_loop_" + unique_number)
    wl(dest_asm, "adds r2, r2, #0")
    wl(dest_asm, "beq exit_delay_inst_" + unique_number)
    wl(dest_asm, "sub r2, r2, #1")
    wl(dest_asm, "b delay_inst_loop_" + unique_number)
    wl(dest_asm, "exit_delay_inst_" + unique_number)

    pull(dest_asm)

# sets the lcds
def set_lcd_inst(tokens):
    wl(dest_asm, "")
    wl(dest_asm, "; " + tokens[0] + " " + tokens[1] + " " + tokens[2] + " " + tokens[3])

    push(dest_asm)

    cell_no = int(tokens[1]) * int(tokens[2])
    unique_number = str(generate_unique_number())
    
    wl(dest_asm, "ld r2, lcd_cell_no_" + unique_number)
    wl(dest_asm, "ld r3, ascii_" + unique_number)

    # r2 specifies the lcd cell number and r3 specifies the ascii value
    wl(dest_asm, "ld r4, lcd_base_value_" + unique_number)
    wl(dest_asm, "add r4, r4, r2")
    wl(dest_asm, "st r3, [r4]")
    wl(dest_asm, "b skip_" + unique_number)
    wl(dest_asm, "lcd_cell_no_" + unique_number + " defw " + str(cell_no))
    wl(dest_asm, "ascii_" + unique_number + " defw '" + tokens[3] + "'")
    wl(dest_asm, "lcd_base_value_" + unique_number + " defw $ff40")
    wl(dest_asm, "skip_" + unique_number)
    
    pull(dest_asm)

# sets the lcds - supports variables
def set_lcd_val_inst(tokens):
    wl(dest_asm, "")
    wl(dest_asm, "; " + tokens[0] + " " + tokens[1] + " " + tokens[2])

    push(dest_asm)

    unique_number = str(generate_unique_number())
    
    get_var_val(tokens[1], "r5")
    wl(dest_asm, "mov r2, r5")
    wl(dest_asm, "ld r3, ascii_" + unique_number)
    # r2 specifies the lcd cell number and r3 specifies the ascii value
    wl(dest_asm, "ld r4, lcd_base_value_" + unique_number)
    wl(dest_asm, "add r4, r4, r2")
    wl(dest_asm, "st r3, [r4]")
    wl(dest_asm, "b skip_" + unique_number)
    wl(dest_asm, "ascii_" + unique_number + " defw '" + tokens[2] + "'")
    wl(dest_asm, "lcd_base_value_" + unique_number + " defw $ff40")
    wl(dest_asm, "skip_" + unique_number)
    
    pull(dest_asm)

# sets the leds
# row and col can be specified in terms of variables
def set_led_inst(tokens):
    wl(dest_asm, "")
    wl(dest_asm, "; " + tokens[0] + " " + tokens[1] + " " + tokens[2] + " " + tokens[3] + " " + tokens[4] + " " + tokens[5])

    push(dest_asm)

    unique_number = str(generate_unique_number())

    if not tokens[1].isdigit() or tokens[2].isdigit():
        # calculates the led cell number
        get_var_val(tokens[1], "r5")
        get_var_val(tokens[2], "r6")
        wl(dest_asm, "mov r2, r0")
        wl(dest_asm, "add r2, r5, r2")
        wl(dest_asm, "add r2, r5, r2")
        wl(dest_asm, "add r2, r5, r2")
        wl(dest_asm, "add r2, r5, r2")
        wl(dest_asm, "add r2, r5, r2")
        wl(dest_asm, "add r2, r5, r2")
        wl(dest_asm, "add r2, r5, r2")
        wl(dest_asm, "add r2, r5, r2")
        wl(dest_asm, "add r2, r6, r2")
    else:
        cell_no = int(tokens[1]) * 8 + int(tokens[2])
        wl(dest_asm, "ld r2, led_cell_no_" + unique_number)
        wl(dest_asm, "b skip_0_" + unique_number)
        wl(dest_asm, "led_cell_no_" + unique_number + " defw " + str(cell_no))
        wl(dest_asm, "skip_0_" + unique_number)
    
    led_value = "$" + generate_led_value(tokens[3], tokens[4], tokens[5])
    
    wl(dest_asm, "ld r3, led_value_" + unique_number)
    # r2 specifies the led cell number and r3 specifies the led value
    wl(dest_asm, "ld r4, led_base_value_" + unique_number)
    wl(dest_asm, "add r4, r4, r2")
    wl(dest_asm, "st r3, [r4]")
    wl(dest_asm, "b skip_" + unique_number)
    wl(dest_asm, "led_value_" + unique_number + " defw " + led_value)
    wl(dest_asm, "led_base_value_" + unique_number + " defw $ff00")
    wl(dest_asm, "skip_" + unique_number)

    pull(dest_asm)

# handles while instructions
def while_true_inst(instructions):
    wl(dest_asm, "")
    wl(dest_asm, "; WHILE_TRUE")
    wl(dest_asm, "st pc, [r1]")
    wl(dest_asm, "add r1, r1, #1")
    wl(dest_asm, "mov r2, #0")
    wl(dest_asm, "mov r3, #0")
    wl(dest_asm, "mov r4, #0")
    wl(dest_asm, "mov r5, #0")
    wl(dest_asm, "mov r6, #0")
    print(instructions)
    unique_number = str(generate_unique_number())
    i = 0
    while(i < len(instructions)):
        print(instructions[i])
        if(instructions[i] == "endwhiletrue"):
            break
        ret_val = parse_and_execute(instructions[i:], instructions[i], unique_number)
        i += ret_val
    wl(dest_asm, "; endwhiletrue")
    wl(dest_asm, "sub r1, r1, #1")
    wl(dest_asm, "ld pc, [r1]")
    
    # stores the address of the instruction after endwhiletrue
    dest_asm.seek(0)
    asm_lines = dest_asm.readlines()
    asm_lines = [line for line in asm_lines if line.strip() != "" and line[0] != ";"]
    break_add = 200 + len(asm_lines)
    dest_asm.seek(0)
    asm_lines = dest_asm.readlines()
    for k, line in enumerate(asm_lines):
        if line == ("break_" + unique_number + " defw 0\n"):
            asm_lines[k] = "break_" + unique_number + " defw " + str(break_add) + "\n"
    dest_asm.truncate(0)
    dest_asm.writelines(asm_lines)

    wl(dest_asm, "org " + str(break_add))
    wl(dest_asm, "sub r1, r1, #1")
    wl(dest_asm, "ld r0, [r1]")
    wl(dest_asm, "break_leads_here_" + unique_number)

    return i + 2

# configures the sw buttons
def on_btn_press_inst(tokens, instructions):
    wl(dest_asm, "")
    wl(dest_asm, "; ON_BUTTON_PRESS")
    push(dest_asm)

    unique_number = str(generate_unique_number())
    btn_no = str(2**(ord(tokens[1]) - 97))
    wl(dest_asm, "ld r2, sw_switches_" + unique_number)
    wl(dest_asm, "b skip_" + unique_number)
    wl(dest_asm, "sw_switches_" + unique_number + " defw " + "$ff95")
    wl(dest_asm, "btn_no_" + unique_number + " defw " + btn_no)
    wl(dest_asm, "skip_" + unique_number)
    
    
    wl(dest_asm, "ld r2, [r2]")
    wl(dest_asm, "ld r3, btn_no_" + unique_number)
    wl(dest_asm, "ands r0, r2, r3")
    # wl(dest_asm, "beq endobp_" + unique_number)
    wl(dest_asm, "bne exec_obp_" + unique_number)
    wl(dest_asm, "b skip_1_" + unique_number)
    wl(dest_asm, "endobp_address_" + unique_number + " defw 0")
    wl(dest_asm, "skip_1_" + unique_number)
    wl(dest_asm, "ld pc, endobp_address_" + unique_number)
    wl(dest_asm, "exec_obp_" + unique_number)

    i = 0
    while(i < len(instructions)):
        if(instructions[i] == "endobp"): break
        ret_val = parse_and_execute(instructions[i:], instructions[i])
        i += ret_val

    # stores in the specified location the address of the instruction after endobp
    dest_asm.seek(0)
    asm_lines = dest_asm.readlines()
    asm_lines = [line for line in asm_lines if line.strip() != "" and line[0] != ";"]
    endobp_add = 200 + len(asm_lines)
    dest_asm.seek(0)
    asm_lines = dest_asm.readlines()
    for k, line in enumerate(asm_lines):
        if line == ("endobp_address_" + unique_number + " defw 0\n"):
            asm_lines[k] = "endobp_address_" + unique_number + " defw " + str(endobp_add) + "\n"
    dest_asm.truncate(0)
    dest_asm.writelines(asm_lines)
    ## 

    wl(dest_asm, "org " + str(endobp_add))
    wl(dest_asm, "endobp_" + unique_number)
    wl(dest_asm, "; endobp")

    pull(dest_asm)
    return i + 2

# sets the leds next to the sw btns
def set_btn_led_instr(tokens):
    wl(dest_asm, "")
    wl(dest_asm, "; " + tokens[0] + " " + tokens[1])

    push(dest_asm)

    led_no = str(2**(ord(tokens[1]) - 97))
    unique_number = str(generate_unique_number())
    wl(dest_asm, "b skip_" + unique_number)
    wl(dest_asm, "led_no_" + unique_number + " defw " + led_no)
    wl(dest_asm, "swled_" + unique_number + " defw $ff97")
    wl(dest_asm, "skip_" + unique_number)
    wl(dest_asm, "ld r2, led_no_" + unique_number)
    # r2 specifies the sw led that must be lit
    wl(dest_asm, "ld r3, swled_" + unique_number)
    wl(dest_asm, "st r2, [r3]")

    pull(dest_asm)

# adds assembly to ftech value of variables in the specified register
def get_var_val(var, register):
    for i, var_name in enumerate(variables):
        if var_name == var:
            wl(dest_asm, "; getting variable value")
            wl(dest_asm, "mov " + register + ", #" + str(i + 3))
            wl(dest_asm, "ld " + register + ", [" + register + "]")
            break;   

# creates variable
def set_var_inst(tokens):
    wl(dest_vars, tokens[1] + " defw " + tokens[2])
    variables.append(tokens[1])

# adds to the value of the specified variable
def add_inst(tokens):
    for i, var in enumerate(variables):
        if var == tokens[1]:
            wl(dest_asm, "")
            wl(dest_asm, "; " + tokens[0] + " " + tokens[1] + " " + tokens[2])

            push(dest_asm)

            unique_number = str(generate_unique_number())

            wl(dest_asm, "mov r3, #" + str(i + 3))
            wl(dest_asm, "ld r2, [r3]")
            wl(dest_asm, "b skip_" + unique_number)
            wl(dest_asm, "inc_val_" + unique_number + " defw " + tokens[2])
            wl(dest_asm, "skip_" + unique_number)
            wl(dest_asm, "ld r4, inc_val_" + unique_number)
            wl(dest_asm, "add r2, r2, r4")
            wl(dest_asm, "st r2, [r3]")

            pull(dest_asm)
            break;      

# changes the content of variables
def change_inst(tokens):
    for i, var in enumerate(variables):
        if var == tokens[1]:
            wl(dest_asm, "")
            wl(dest_asm, "; " + tokens[0] + " " + tokens[1] + " " + tokens[2])

            push(dest_asm)

            unique_number = str(generate_unique_number())

            wl(dest_asm, "mov r3, #" + str(i + 3))

            # allows the change instruction to accept variables
            if tokens[2].isdigit():
                wl(dest_asm, "b skip_" + unique_number)
                wl(dest_asm, "var_val_" + unique_number + " defw " + tokens[2])
                wl(dest_asm, "skip_" + unique_number)
                wl(dest_asm, "ld r2, var_val_" + unique_number)
            else:
                get_var_val(tokens[2], "r5")
                wl(dest_asm, "mov r2, r5")

            wl(dest_asm, "st r2, [r3]")

            pull(dest_asm)
            break; 

# handles if statements
def if_inst(tokens, instructions, un=""):
    wl(dest_asm, "")
    wl(dest_asm, "; " + tokens[0] + " " + tokens[1] + " " + tokens[2] + " " + tokens[3])

    push(dest_asm)

    unique_number = str(generate_unique_number())
    get_var_val(tokens[1], "r5")
    wl(dest_asm, "ld r2, check_var_val_" + unique_number)
    wl(dest_asm, "b skip_" + unique_number)
    wl(dest_asm, "check_var_val_" + unique_number + " defw " + tokens[3])
    wl(dest_asm, "skip_" + unique_number)
    # supports the = and != operator for now
    if tokens[2] == "=":
        wl(dest_asm, "subs r0, r2, r5")
        wl(dest_asm, "beq exec_if_" + unique_number)
    if tokens[2] == "!=":
        wl(dest_asm, "subs r0, r2, r5")
        wl(dest_asm, "bne exec_if_" + unique_number)
    wl(dest_asm, "b skip_1_" + unique_number)
    wl(dest_asm, "endif_address_" + unique_number + " defw 0")
    wl(dest_asm, "skip_1_" + unique_number)
    wl(dest_asm, "ld pc, endif_address_" + unique_number)
    wl(dest_asm, "exec_if_" + unique_number)

    i = 0
    while(i < len(instructions)):
        if(instructions[i] == "endif"): break
        if instructions[i] == "break":
            ret_val = parse_and_execute(instructions[i:], instructions[i], un)
        else:
            ret_val = parse_and_execute(instructions[i:], instructions[i])
        i += ret_val

    dest_asm.seek(0)
    asm_lines = dest_asm.readlines()
    asm_lines = [line for line in asm_lines if line.strip() != "" and line[0] != ";"]
    endif_add = 200 + len(asm_lines)
    dest_asm.seek(0)
    asm_lines = dest_asm.readlines()
    for k, line in enumerate(asm_lines):
        if line == ("endif_address_" + unique_number + " defw 0\n"):
            asm_lines[k] = "endif_address_" + unique_number + " defw " + str(endif_add) + "\n"
    dest_asm.truncate(0)
    dest_asm.writelines(asm_lines)

    wl(dest_asm, "org " + str(endif_add))
    wl(dest_asm, "endif_" + unique_number)
    wl(dest_asm, "; endif")

    pull(dest_asm)
    return i + 2

# handles break; statements
def break_inst(un):
    wl(dest_asm, "b skip_" + un)
    wl(dest_asm, "break_" + un + " defw " + str(0))
    wl(dest_asm, "skip_" + un)
    wl(dest_asm, "ld pc, break_" + un)

def parse_and_execute(instructions, instr, un=""):
    if instr == "":
        return
    tokens = instr.split(" ")
    inst_tok = tokens[0].upper()
    if inst_tok == "//":
        return 1
    elif inst_tok == "PLAY_NOTE":
        play_note(tokens)
    elif inst_tok == "DELAY_INST":
        delay_inst(tokens)
    elif inst_tok == "SET_LCD":
        set_lcd_inst(tokens)
    elif inst_tok == "SET_LED_MATRIX":
        set_led_inst(tokens)
    elif inst_tok == "WHILE_TRUE":
        return while_true_inst(instructions[1:])
    elif inst_tok == "ON_BUTTON_PRESS":
        return on_btn_press_inst(tokens, instructions[1:])
    elif inst_tok == "SET_BTN_LED":
        set_btn_led_instr(tokens)
    elif inst_tok == "VAR":
        set_var_inst(tokens)
    elif inst_tok == "ADD":
        add_inst(tokens)
    elif inst_tok == "CHANGE":
        change_inst(tokens)
    elif inst_tok == "IF":
        return if_inst(tokens, instructions[1:], un)
    elif inst_tok == "BREAK":
        break_inst(un)
    elif inst_tok == "SET_LCD_VAL":
        set_lcd_val_inst(tokens)
    return 1

# terminates compilation
def initiate_termination():
    dest_stack.seek(0)
    dest_asm.seek(0)
    dest_vars.seek(0)

    dest_vars_cnt = dest_vars.read()
    dest_stack_cnt = dest_stack.read()
    dest_asm_cnt = dest_asm.read()

    # write to destination files
    dest.write(dest_vars_cnt)
    dest.write(dest_stack_cnt)
    dest.write(dest_asm_cnt)
    
    wl(dest, "")
    wl(dest, "b .")
    wl(dest, "")
    wl(dest, "")
    # artefacts!
    wl(dest, "; compiled from the rish language using the rish_STUMP compiler")
    wl(dest, "; The rish language and the rish_STUMP compiler were created by Rishi Ravikumar, 2022")

    # close files
    dest.close()
    dest_asm.close()
    src.close()

    os.remove(dest_tmp_asm_fn)
    os.remove(dest_tmp_stack_fn)
    os.remove(dest_tmp_vars_fn)

def main():
    # basic file setups
    basic_stack_setup(dest_stack)
    basic_asm_setup(dest_asm)
    basic_vars_setup(dest_vars)
    # instruction parsing
    src_data = src.read()
    instructions = [instr.strip() for instr in src_data.split(";")]
    i = 0
    while(i < len(instructions) - 1):
        ret_val = parse_and_execute(instructions[i:], instructions[i])
        i += ret_val
    initiate_termination()

# ----------

main()

