// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.
//HOW IT WORKS: Sets i to R1, loops adding R0 to R2 and decrements i by one each time, until i=0.
//Stores R1 in D
@R1
D=M
//Creates counter, sets to R1, adds to RAM at i
@i
M=D
//Creates location in RAM for result
@result
M=0
//Main loop where adding happens
(MAIN)
    //Checks if i is 0
    @i
    D=M
    @END
    D;JEQ
    //Adds R0 to R2
    @R0
    D=M
    @result
    M=D+M
    //Decrements i
    @i
    M=M-1
    //Goes back to beginning of loop
    @MAIN
    0;JMP

//Ends program
(END)
    @result
    D=M
    @R2
    M=D