// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

//Stores the end location of the screen in the memory
@SCREEN
D=A
@8192
D=D+A
@screenend
M=D
//Stores the current location of the screen in memory
@SCREEN
D=A
@screencurrent
M=D
//Checks if a key is being held down
(CHECKKEY)
    @KBD
    D=M
    @SCREENFILL
    D;JNE
    @SCREENEMPTY
    D;JEQ
//If a key is being held down and the current location in memory is less than the end location of the screen, then turn on pixels.
//Otherwise, go back to CHECKKEY
(SCREENFILL)
    @screenend
    D=M
    @screencurrent
    D=D-M
    @CHECKKEY
    D;JEQ
    //At this point, the current location in memory is less than the end location of the screen, so it turns on pixels.
    @screencurrent
    A=M
    M=1
    @screencurrent
    M=M+1
    @CHECKKEY
    0;JMP
//If not, turn off pixels as long as the current location in memory is greater than/equal to the first location.
(SCREENEMPTY)
    @screencurrent
    D=M
    @SCREEN
    D=D-A
    @CHECKKEY
    D;JEQ
    //At this point, the current location in memory is greater than the start location of the screen, so it turns off pixels.
    @screencurrent
    A=M
    M=0
    @screencurrent
    M=M-1
    @CHECKKEY
    0;JMP