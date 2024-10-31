# Project Code: WCC Part 1B

This is an individual project. However, you can discuss your solution designs with your mates.
You must write - from your own brain not the AI - and understand every line of code!

# Terminology

It is time to make the WCC Computer a little more formal. Below is a description of some
important terms that we will use going forward to build out the computer.

WCC code programs are given as a list of integers; these values are used as the initial state for
the computer's *memory*. When you run a WCC program, make sure to start by initializing
memory to the program's values. A position in memory is called an *address* (for example, the
first value in memory is at "address 0").

Operation codes (like 1, 2, or 99) mark the beginning of an instruction. The values used
immediately after an operation code, if any, are called the instruction's *parameters*. For
example, in the instruction ```1,2,3,4```, ```1``` is the operation code; ```2,3``` and ```4``` are the parameters.
The instruction ```99``` contains only an operation code and has no parameters.

The address of the current instruction is called the *instruction pointer*; it starts at 0. After an
instruction finishes, the instruction pointer increases by the number of values in the instruction;
until you add more instructions to the computer, this is always 4 (1 operation code + 3
parameters) for the add and multiply instructions. (The halt instruction would increase the
instruction pointer by 1, but it halts the program instead.)

# Challenge

Using your basic computer from Part 1 you need to determine the inputs to produce an output of
19690720.

The inputs should still be provided to the program by replacing the values at addresses 1 and 2,
just like before. In this program, the value placed in address 1 is called the *noun*, and the value
placed in address 2 is called the *verb*. Each of the two input values will be between 0 and 99,
inclusive.

Once the program has halted, its output is available at address 0, also just like before. Each
time you try a pair of inputs, make sure you first reset the computer's memory to the values in
the program (your puzzle input) - in other words, don't reuse memory from a previous attempt.

Find the input noun and verb that causes the program to produce the output 19690720.

*What is 100 * noun + verb?* (For example, if noun=12 and verb=2, the answer would be 1202.
Your program should already produce this output since you did Part1 correctly.)

# Your Program

```
1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,10,19,1,19,5,23,2,23,9,27,1,5,27,3
1,1,9,31,35,1,35,10,39,2,13,39,43,1,43,9,47,1,47,9,51,1,6,51,55,1,13,5
5,59,1,59,13,63,1,13,63,67,1,6,67,71,1,71,13,75,2,10,75,79,1,13,79,83,
1,83,10,87,2,9,87,91,1,6,91,95,1,9,95,99,2,99,10,103,1,103,5,107,2,6,1
07,111,1,111,6,115,1,9,115,119,1,9,119,123,2,10,123,127,1,127,5,131,2,
6,131,135,1,135,5,139,1,9,139,143,2,143,13,147,1,9,147,151,1,151,2,155
,1,9,155,0,99,2,0,14,0
```

Your Answer ________________