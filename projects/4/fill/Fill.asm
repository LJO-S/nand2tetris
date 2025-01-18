// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

(INIT)
    @SCREEN
    D=A
    // save addr of screen base
    @addr 
    M=D
    // check keystroke
    @24576 
    D=M
    // save keystroke
    @last_keystroke
    M=D
(LOOP_1)
    // check if current != previous keystroke
    @24576
    D=M
    @last_keystroke
    D=D-M
    @INIT
    D;JNE
    // check keystroke
    @24576
    D=M
    @WHITE
    D;JEQ
    @BLACK
    D;JMP
(LOOP_2)
    // incr address
    @addr
    M=M+1
    // check if we are at end of screen RAM
    D=M
    @24575
    D=D-A
    @INIT
    D;JGT
    @LOOP_1
    D;JMP
(WHITE)
    @addr
    A=M
    // set to 0x0000
    M=0
    @LOOP_2
    D;JMP
(BLACK)
    @addr
    A=M
    // set to 0xFFFF
    M=-1
    @LOOP_2
    D;JMP



