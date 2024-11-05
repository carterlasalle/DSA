# Project Code.2.1

The WWC computer is fairly basic, but it has potential. Let's start building it out by adding more
functionality. Over the next challenges you will be fleshing out a full fledged WWC machine.

# New Instructions

First, you'll need to add two new instructions to your computer

**Opcode 3** takes a single integer as input and saves it to the position given by its only
parameter. For example, the instruction ```3,50``` would take an input value and store it at address
50.

**Opcode 4** outputs the value of its only parameter. For example, the instruction ```4,50``` would
output the value at address 50.

Programs that use these instructions will come with documentation that explains what should be
connected to the input and output. The program ```3,0,4,0,99``` outputs whatever it gets as input,
then halts.

# Parameter Modes

You need to add parameter modes to each instruction. Each parameter of an instruction is
handled based on its parameter mode. Right now, your computer already understands
parameter mode 0, *position mode*, which causes the parameter to be interpreted as a position -
if the parameter is 50, its value is the value stored at address 50 in memory. Until now, all
parameters have been in position mode.

Now, your computer will also need to handle parameters in mode 1, *immediate mode*. In
immediate mode, a parameter is interpreted as a value - if the parameter is 50, its value is
simply 50.

Parameter modes are stored in the same value as the instruction's opcode. The opcode is a
two-digit number based only on the ones and tens digit of the value, that is, the opcode is the
rightmost two digits of the first value in an instruction. Parameter modes are single digits, one
per parameter, read right-to-left from the opcode: the first parameter's mode is in the hundreds
digit, the second parameter's mode is in the thousands digit, the third parameter's mode is in the
ten-thousands digit, and so on. Any missing modes are 0.

For example, consider the program ```1002,4,3,4,33```.

The first instruction, ```1002,4,3,4```, is a multiply instruction - the rightmost two digits of the first
value, ```02```, indicate opcode ```2```, multiplication. Then, going right to left, the parameter modes are
```0``` (hundreds digit), ```1``` (thousands digit), and ```0``` (ten-thousands digit, not present and therefore
zero):

```
ABCDE
1002

DE - two-digit opcode, 02 == opcode 2
C - mode of 1st parameter, 0 == position mode
B - mode of 2nd parameter, 1 == immediate mode
A - mode of 3rd parameter, 0 == position mode, omitted due to being a leading zero
```

This instruction multiplies its first two parameters. The first parameter, ```4``` in position mode, works
like it did before - its value is the value stored at address ```4``` (33). The second parameter, ```3``` in
immediate mode, simply has value 3. The result of this operation, 33 * 3 = 99, is written
according to the third parameter, 4 in position mode, which also works like it did before - 99 is
written to address 4.

**Parameters that an instruction writes to will never be in immediate mode.**

# Some Notes:

* It is important to remember that the instruction pointer should increase by the number of
values in the instruction after the instruction finishes. Because of the new instructions,
this amount is no longer always 4.

* Integers can be negative: ```1101,100,-1,4,0``` is a valid program (find 100 + -1, store
the result in position 4).

* Your previous WWC programs should still work and produce the same output with this
version of the instruction specification.

# Challenge

As input you will be given a new program. This is a diagnostic style program that is meant to
output a code that indicates if the test passed or failed. If the program outputs a 0 the test was
successful. Any other number indicates a failed test.

The program will start by requesting from the user the ID of a hypothetical system to test by
running an input instruction - provide it a value of 1.

It will then perform a series of diagnostic tests confirming that various parts of the WWC
computer, like parameter modes, function correctly. For each test, it will run an output instruction
indicating how far the result of the test was from the expected value, where 0 means the test
was successful. Non-zero outputs mean that a function is not working correctly; check the
instructions that were run before the output instruction to see which one failed.

Finally, the program will output a diagnostic code and immediately halt. This final output isn't an
error; an output followed immediately by a halt means the program finished. If all outputs were
zero except the diagnostic code, the diagnostic program ran successfully.

After providing 1 to the only input instruction and passing all the tests, what diagnostic code
does the program produce?

# Your Program

```
3,225,1,225,6,6,1100,1,238,225,104,0,1102,72,20,224,1001,224,-1440,224,4,224,102,8,223
,223,1001,224,5,224,1,224,223,223,1002,147,33,224,101,-3036,224,224,4,224,102,8,223,22
3,1001,224,5,224,1,224,223,223,1102,32,90,225,101,65,87,224,101,-85,224,224,4,224,1002
,223,8,223,101,4,224,224,1,223,224,223,1102,33,92,225,1102,20,52,225,1101,76,89,225,1,
117,122,224,101,-78,224,224,4,224,102,8,223,223,101,1,224,224,1,223,224,223,1102,54,22
,225,1102,5,24,225,102,50,84,224,101,-4600,224,224,4,224,1002,223,8,223,101,3,224,224,
1,223,224,223,1102,92,64,225,1101,42,83,224,101,-125,224,224,4,224,102,8,223,223,101,5
,224,224,1,224,223,223,2,58,195,224,1001,224,-6840,224,4,224,102,8,223,223,101,1,224,2
24,1,223,224,223,1101,76,48,225,1001,92,65,224,1001,224,-154,224,4,224,1002,223,8,223,
101,5,224,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105
,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265
,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225
,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,
0,0,106,0,0,1105,1,99999,1107,677,226,224,1002,223,2,223,1005,224,329,101,1,223,223,7,
677,226,224,102,2,223,223,1005,224,344,1001,223,1,223,1107,226,226,224,1002,223,2,223,
1006,224,359,1001,223,1,223,8,226,226,224,1002,223,2,223,1006,224,374,101,1,223,223,10
8,226,226,224,102,2,223,223,1005,224,389,1001,223,1,223,1008,226,226,224,1002,223,2,22
3,1005,224,404,101,1,223,223,1107,226,677,224,1002,223,2,223,1006,224,419,101,1,223,22
3,1008,226,677,224,1002,223,2,223,1006,224,434,101,1,223,223,108,677,677,224,1002,223,
2,223,1006,224,449,101,1,223,223,1108,677,226,224,102,2,223,223,1006,224,464,1001,223,
1,223,107,677,677,224,102,2,223,223,1005,224,479,101,1,223,223,7,226,677,224,1002,223,
2,223,1006,224,494,1001,223,1,223,7,677,677,224,102,2,223,223,1006,224,509,101,1,223,2
23,107,226,677,224,1002,223,2,223,1006,224,524,1001,223,1,223,1007,226,226,224,102,2,2
23,223,1006,224,539,1001,223,1,223,108,677,226,224,102,2,223,223,1005,224,554,101,1,22
3,223,1007,677,677,224,102,2,223,223,1006,224,569,101,1,223,223,8,677,226,224,102,2,22
3,223,1006,224,584,1001,223,1,223,1008,677,677,224,1002,223,2,223,1006,224,599,1001,22
3,1,223,1007,677,226,224,1002,223,2,223,1005,224,614,101,1,223,223,1108,226,677,224,10
02,223,2,223,1005,224,629,101,1,223,223,1108,677,677,224,1002,223,2,223,1005,224,644,1
001,223,1,223,8,226,677,224,1002,223,2,223,1006,224,659,101,1,223,223,107,226,226,224,
102,2,223,223,1005,224,674,101,1,223,223,4,223,99,226
```

Your Answer ________________