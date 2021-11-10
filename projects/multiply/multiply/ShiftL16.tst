// This file is an extension of the nand2Tetris curriculum
// File name: projects/01/ShiftL16.tst

load ShiftL16.hdl,
output-file ShiftL16.out,
compare-to ShiftL16.cmp,
output-list in%B1.16.1 out%B1.16.1;

set in %B0000000000000000,
eval,
output;

set in %B1111111111111111,
eval,
output;

set in %B1010101010101010,
eval,
output;

set in %B0011110011000011,
eval,
output;

set in %B0001001000110100,
eval,
output;