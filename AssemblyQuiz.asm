//while true{
//  if currentkey >= 48 and currentkey <= 57{
//      RAM[currentkey - 48] = currentkey-48
//  }
//}

(CHECKKEY)
    //Checks if key is less than the ASCII code for a number
    @KBD
    D=M
    @48
    D=D-A
    @currentnum //Stores the current number
    M=D
    @CHECKKEY
    D;JLT
    //Checks if key is greater than the ASCII code for a number
    @KBD
    D=M
    @57
    D=D-A
    @CHECKKEY
    D;JGT
//If the key is a number, it is stored in RAM
@currentnum
D=M
A=D
M=D
//Loops back to beginning
@CHECKKEY
0;JMP