import sys

# prints the error and exits
def error(error_msg):
    print(error_msg)
    sys.exit(1)

# writes a line to the specified file
def wl(fp, msg):
    fp.write(msg + "\n")

def get_note_value(note, octave, duration):
    return_str = "$8"
    if(int(duration) <= 15 and int(duration) >= 0):
        return_str += hex(int(duration))[2:]
    else:
        error("ValueError: duration must be between 0 and 15")
    if(int(octave) <= 15 and int(octave) >= 0):
        return_str += hex(int(octave))[2:]
    else:
        error("ValueError: octave must be between 0 and 15")

    note = note.lower()
    if(note == 'c'): return_str += "0"
    elif(note == 'c#'): return_str += "1"
    elif(note == 'd'): return_str += "2"
    elif(note == 'd#'): return_str += "3"
    elif(note == 'e'): return_str += "4"
    elif(note == 'f'): return_str += "5"
    elif(note == 'f#'): return_str += "6"
    elif(note == 'g'): return_str += "7"
    elif(note == 'g#'): return_str += "8"
    elif(note == 'a'): return_str += "9"
    elif(note == 'a#'): return_str += "a"
    elif(note == 'b'): return_str += "b"
    else: error("ValueError: note has an incorrect value - only musical notes are allowed")

    return return_str

def basic_asm_setup(dest_asm):
    wl(dest_asm, "")
    wl(dest_asm, "")
    wl(dest_asm, "org 200")
    wl(dest_asm, "; code")
    wl(dest_asm, "mov r1, #15")
    wl(dest_asm, "mov r1, #15")
    wl(dest_asm, "mov r1, #15")
    wl(dest_asm, "mov r1, #15")
    wl(dest_asm, "mov r1, #15")
    wl(dest_asm, "mov r1, #15")
    wl(dest_asm, "mov r1, #10")
    wl(dest_asm, "")
    wl(dest_asm, "")

def basic_vars_setup(dest_vars):
    wl(dest_vars, "org 0")
    wl(dest_vars, "ld pc, code_begins")
    wl(dest_vars, "code_begins defw 200")
    wl(dest_vars, "")
    wl(dest_vars, "; variables")
    wl(dest_vars, "org 3")

def basic_stack_setup(dest_stack):
    wl(dest_stack, "")
    wl(dest_stack, "")
    wl(dest_stack, "; stack")
    wl(dest_stack, "org 100")

def push(dest_asm):
    # r1 is the stack pointer - it always points to the first empty slot on top of the stack
    wl(dest_asm, "; ***")
    wl(dest_asm, "; PUSH TO STACK")
    wl(dest_asm, "st r2, [r1]")
    wl(dest_asm, "add r1, r1, #1")
    wl(dest_asm, "st r3, [r1]")
    wl(dest_asm, "add r1, r1, #1")
    wl(dest_asm, "st r4, [r1]")
    wl(dest_asm, "add r1, r1, #1")
    wl(dest_asm, "st r5, [r1]")
    wl(dest_asm, "add r1, r1, #1")
    wl(dest_asm, "st r6, [r1]")
    wl(dest_asm, "add r1, r1, #1")
    wl(dest_asm, "; ***")

def pull(dest_asm):
    # r1 is the stack pointer
    wl(dest_asm, "; ***")
    wl(dest_asm, "; PULL FROM STACK")
    wl(dest_asm, "sub r1, r1, #1")
    wl(dest_asm, "ld r6, [r1]")
    wl(dest_asm, "sub r1, r1, #1")
    wl(dest_asm, "ld r5, [r1]")
    wl(dest_asm, "sub r1, r1, #1")
    wl(dest_asm, "ld r4, [r1]")
    wl(dest_asm, "sub r1, r1, #1")
    wl(dest_asm, "ld r3, [r1]")
    wl(dest_asm, "sub r1, r1, #1")
    wl(dest_asm, "ld r2, [r1]")
    wl(dest_asm, "; ***")

def generate_led_value(red, green, blue):
    return_str = "00000000"
    rh = format(int(red), "03b")
    gh = format(int(green), "03b")
    bh = format(int(blue), "02b")
    return_str += rh + gh + bh
    return_str = format(int(return_str, 2), "04X")
    return return_str

