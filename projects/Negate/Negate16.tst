load Negate16.hdl,
output-file Negate16.out,
compare-to Negate16.cmp,
output-list in%B1.16.1 out%B1.16.1;

// 0 -> 0
set in %B0000000000000000,
eval,
output;

// -1 -> 1
set in %B1111111111111111,
eval,
output;

// 2 -> -2
set in %B0000000000000010,
eval,
output;

// 1800 -> -1800
set in %B0000011100001000,
eval,
output;

// -16001 -> 16001 
set in %B1100000101111111,
eval,
output;