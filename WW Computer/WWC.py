# WW Computer Project 1

input = [1,12,2,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,10,19,1,19,5,23,2,23,9,27,1,5,27,31,1,9,31,35,1,35,10,39,2,13,39,43,1,43,9,47,1,47,9,51,1,6,51,55,1,13,55,59,1,59,13,63,1,13,63,67,1,6,67,71,1,71,13,75,2,10,75,79,1,13,79,83,1,83,10,87,2,9,87,91,1,6,91,95,1,9,95,99,2,99,10,103,1,103,5,107,2,6,107,111,1,111,6,115,1,9,115,119,1,9,119,123,2,10,123,127,1,127,5,131,2,6,131,135,1,135,5,139,1,9,139,143,2,143,13,147,1,9,147,151,1,151,2,155,1,9,155,0,99,2,0,14,0]

def parse_instruction(instructions):
    instructions_str = str(instructions)
    
    opcode = int(instructions_str[-2:])

    modes = []
    for i in  range(3, 0, -1):
        if len(instructions_str) > i:
            modes.append(int(instructions_str[-i-2]))
        else:
            modes.append(0)
    return (opcode, modes)
    
def get_parameter_value(memory, position, mode):
    if mode == 0:
        return memory[memory[position]]
    else:
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
            output = run_program(memory)
            if output == target_output:
                return noun, verb
 
def get_value_at_position(memory, position):
    return memory[position]

def execute_add(memory, pos1, pos2, output_pos, modes):
    
    value1 = get_value_at_position(memory, pos1)
    value2 = get_value_at_position(memory, pos2)
    result = value1 + value2
    memory[output_pos] = result

def execute_multiply(memory, pos1, pos2, output_pos, modes):

    value1 = get_value_at_position(memory,pos1)
    value2 = get_value_at_position(memory,pos2)
    result = value1 * value2
    memory[output_pos] = result

def execute_input(memory, pos, input_value):
    pass

def execute_output(memory, pos, mode):
    pass


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
    print("Part 1 Result:")
    memory = input.copy()
    print(run_program(memory))

    print("\nPart 2 Result:")
    target = 19690720
    noun,verb = find_noun_verb_combination(target)
    if noun is not None:
        answer = 100 * noun + verb
        print(answer)


if __name__ == "__main__":
    main()

