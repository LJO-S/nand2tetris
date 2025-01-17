// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

// A multiplication R0 * R1 is simply R1 + R1 + R1 ... R0 times
    @sum
    M=0
    @i
    M=0
    @R2
    M=0
(LOOP) // Loop over R1 until D=R0 is smaller than 0
    @i
    D=M
    @R0
    D=D-M
    @OUTPUT
    D;JEQ
    @R1
    D=M
    @sum
    M=M+D
    @i
    M=M+1
    @LOOP
    0;JMP
(OUTPUT) // R2 output
    @sum
    D=M
    @R2
    M=D
(END)
    @END
    0;JMP



