# Project Code: WWC Part 1

This is an individual project. However, you can discuss your solution designs with your mates.
You must write - from your own brain not the AI - and understand every line of code!

# Language Specification version 1.0

You have to build a WWC Computer! A WWC computer is on that can run WWC programs.
Following is a description of the WWC language. Note, the language has more features, but this
is the most basic form of the language.

An WWC program is a list of integers separated by commas (like ```1,0,0,3,99```). To run one,
start by looking at the first integer (called position 0). Here, you will find an operation code -
either ```1```, ```2```, or ```99```. The operation code indicates what to do; for example, ```99``` means that the
program is finished and should immediately halt. Encountering an unknown operation code
means something went wrong.

Operation code ```1``` adds together numbers read from two positions and stores the result in a third
position. The three integers immediately after the operation code tell you these three positions -
the first two indicate the positions from which you should read the input values, and the third
indicates the position at which the output should be stored.

For example, if your Intcode computer encounters ```1,10,20,30```, it should read the values at
positions 10 and 20, add those values, and then overwrite the value at position 30 with their sum.

Operation code ```2``` works exactly like operation code ```1```, except it multiplies the two inputs instead
of adding them. Again, the three integers after the operation code indicate where the inputs and
outputs are, not their values.

Once you're done processing an operation code, move to the next one by stepping forward 4
positions.

# Language Specification 1.0 Examples

For example, suppose you have the following program:
```
1,9,10,3,2,3,11,0,99,30,40,50
```

For the purposes of illustration, here is the same program split into multiple lines:
```
1,9,10,3,
2,3,11,0,
99,
30,40,50
```

The first four integers, ```1,9,10,3```, are at positions 0, 1, 2, and 3. Together, they represent the
first operation code (1, addition), the positions of the two inputs (9 and 10), and the position of
the output (3). To handle this operation code, you first need to get the values at the input
positions: position 9 contains 30, and position 10 contains 40. Add these numbers together to
get 70. Then, store this value at the output position; here, the output position (3) is at position 3,
so it overwrites itself. Afterward, the program looks like this:

```
1,9,10,70,
2,3,11,0,
99,
30,40,50
```

Step forward 4 positions to reach the next operation code, ```2```. This operation code works just like
the previous, but it multiplies instead of adding. The inputs are at positions 3 and 11; these
positions contain 70 and 50 respectively. Multiplying these produces 3500; this is stored at
position 0:

```
3500,9,10,70,
2,3,11,0,
99,
30,40,50
```

Stepping forward 4 more positions arrives at operation code 99, halting the program.

Here are the initial and final states of a few more small programs:

```1,0,0,0,99``` becomes ```2,0,0,0,99``` (1 + 1 = 2).

```2,3,0,3,99``` becomes ```2,3,0,6,99``` (3 * 2 = 6).

```2,4,4,5,99,0``` becomes ```2,4,4,5,99,9801``` (99 * 99 = 9801).

```1,1,1,4,99,5,6,0,99``` becomes ```30,1,1,4,2,5,6,0,99```.

# Language Specification v1.0 Test

Once you think that you have a working computer do the following to test it:

You will be given an input. Before running the program, replace position 1 with the value 12 and
replace position 2 with the value 2.

What value is left at position 0 after the program halts?

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
