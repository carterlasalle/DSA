input_file = 'AdventofCode/input.txt'

def convert_input():
    with open(input_file, 'r') as file:
        left, right = [], []
        for line in file:
            values = line.split()
            left.append(int(values[0]))
            right.append(int(values[1]))
    left.sort()
    right.sort()
    return left, right

def part_one(left, right):
    distance = 0
    for i in range(len(left)):
        distance += abs(right[i] - left[i])
    return distance

def part_two(left, right):
    similarity_score = 0
    for i in range(len(left)):
        similarity_score += left[i] * right.count(left[i])
    return similarity_score

if __name__ == "__main__":
    left, right = convert_input()
    print(part_one(left, right))
    print(part_two(left, right))


    