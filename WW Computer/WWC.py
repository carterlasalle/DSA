# WW Computer Project 1

input = [3,225,1,225,6,6,1100,1,238,225,104,0,1102,72,20,224,1001,224,-1440,224,4,224,102,8,223,223,1001,224,5,224,1,224,223,223,1002,147,33,224,101,-3036,224,224,4,224,102,8,223,223,1001,224,5,224,1,224,223,223,1102,32,90,225,101,65,87,224,101,-85,224,224,4,224,1002,223,8,223,101,4,224,224,1,223,224,223,1102,33,92,225,1102,20,52,225,1101,76,89,225,1,117,122,224,101,-78,224,224,4,224,102,8,223,223,101,1,224,224,1,223,224,223,1102,54,22,225,1102,5,24,225,102,50,84,224,101,-4600,224,224,4,224,1002,223,8,223,101,3,224,224,1,223,224,223,1102,92,64,225,1101,42,83,224,101,-125,224,224,4,224,102,8,223,223,101,5,224,224,1,224,223,223,2,58,195,224,1001,224,-6840,224,4,224,102,8,223,223,101,1,224,224,1,223,224,223,1101,76,48,225,1001,92,65,224,1001,224,-154,224,4,224,1002,223,8,223,101,5,224,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1107,677,226,224,1002,223,2,223,1005,224,329,101,1,223,223,7,677,226,224,102,2,223,223,1005,224,344,1001,223,1,223,1107,226,226,224,1002,223,2,223,1006,224,359,1001,223,1,223,8,226,226,224,1002,223,2,223,1006,224,374,101,1,223,223,108,226,226,224,102,2,223,223,1005,224,389,1001,223,1,223,1008,226,226,224,1002,223,2,223,1005,224,404,101,1,223,223,1107,226,677,224,1002,223,2,223,1006,224,419,101,1,223,223,1008,226,677,224,1002,223,2,223,1006,224,434,101,1,223,223,108,677,677,224,1002,223,2,223,1006,224,449,101,1,223,223,1108,677,226,224,102,2,223,223,1006,224,464,1001,223,1,223,107,677,677,224,102,2,223,223,1005,224,479,101,1,223,223,7,226,677,224,1002,223,2,223,1006,224,494,1001,223,1,223,7,677,677,224,102,2,223,223,1006,224,509,101,1,223,223,107,226,677,224,1002,223,2,223,1006,224,524,1001,223,1,223,1007,226,226,224,102,2,223,223,1006,224,539,1001,223,1,223,108,677,226,224,102,2,223,223,1005,224,554,101,1,223,223,1007,677,677,224,102,2,223,223,1006,224,569,101,1,223,223,8,677,226,224,102,2,223,223,1006,224,584,1001,223,1,223,1008,677,677,224,1002,223,2,223,1006,224,599,1001,223,1,223,1007,677,226,224,1002,223,2,223,1005,224,614,101,1,223,223,1108,226,677,224,1002,223,2,223,1005,224,629,101,1,223,223,1108,677,677,224,1002,223,2,223,1005,224,644,1001,223,1,223,8,226,677,224,1002,223,2,223,1006,224,659,101,1,223,223,107,226,226,224,102,2,223,223,1005,224,674,101,1,223,223,4,223,99,226]

def parse_instruction(instruction):
    # Convert to string and pad with leading zeros to ensure at least 5 digits
    instruction_str = str(instruction).zfill(5)
    
    # Get opcode (last 2 digits)
    opcode = int(instruction_str[-2:])
    
    # Get modes from right to left (excluding opcode digits)
    modes = [
        int(instruction_str[2]),  # First parameter mode
        int(instruction_str[1]),  # Second parameter mode
        int(instruction_str[0])   # Third parameter mode
    ]
    
    return (opcode, modes)

def get_parameter_value(memory, position, mode):
    if mode == 0:  # Position mode
        return memory[memory[position]]
    else:  # Immediate mode
        return memory[position]

def initialize_with_noun_verb(memory, noun, verb):
    memory_copy = memory.copy()
    memory_copy[1] = noun
    memory_copy[2] = verb
    return memory_copy

def find_noun_verb_combination(target_output):
    for noun in range(100):
        for verb in range(100):
            memory = initialize_with_noun_verb(input, noun, verb)
            result, _ = run_program(memory)  
            if result == target_output:
                return noun, verb
    return None, None  

def get_value_at_position(memory, position):
    return memory[position]

def execute_add(memory, pos1, pos2, output_pos, modes):
    value1 = get_parameter_value(memory, pos1, modes[0])
    value2 = get_parameter_value(memory, pos2, modes[1])
    result = value1 + value2
    memory[memory[output_pos]] = result

def execute_multiply(memory, pos1, pos2, output_pos, modes):
    value1 = get_parameter_value(memory, pos1, modes[0])
    value2 = get_parameter_value(memory, pos2, modes[1])
    result = value1 * value2
    memory[memory[output_pos]] = result

def execute_input(memory, pos, input_value):
    memory[memory[pos]] = input_value

def execute_output(memory, pos, mode):
    return get_parameter_value(memory, pos, mode)

def execute_instruction(memory, position, input_value=None):
    instruction = memory[position]
    opcode, modes = parse_instruction(instruction)
    
    if opcode == 99:
        return -1, None
    elif opcode == 1:
        execute_add(memory, position + 1, position + 2, position + 3, modes)
        return position + 4, None
    elif opcode == 2:
        execute_multiply(memory, position + 1, position + 2, position + 3, modes)
        return position + 4, None
    elif opcode == 3:
        execute_input(memory, position + 1, input_value)
        return position + 2, None
    elif opcode == 4:
        output_value = execute_output(memory, position + 1, modes[0])
        return position + 2, output_value

def run_program(memory, input_value=1):
    position = 0
    outputs = []
    
    while True:
        position, output = execute_instruction(memory, position, input_value)
        if output is not None:
            outputs.append(output)
        if position == -1:
            break
    
    return memory[0], outputs

def main():
    print("Running diagnostic program...")
    memory = input.copy()
    result, outputs = run_program(memory, input_value=1)
    
    print("\nDiagnostic Test Results:")
    for i, output in enumerate(outputs[:-1]):  
        if output == 0:
            print(f"Test {i+1}: PASS")
        else:
            print(f"Test {i+1}: FAIL (output: {output})")
    
    if outputs:
        print(f"\nDiagnostic Code: {outputs[-1]}") 
    else:
        print("No diagnostic code produced!")

if __name__ == "__main__":
    main()

