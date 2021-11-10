load Mult16.hdl,
output-file Mult16.out,
compare-to Mult16.cmp,
output-list a%B1.16.1 b%B1.16.1 out%B1.16.1;

set a %B0000000000000000,
set b %B0000000000000000,
eval,
output;

set a %B0000000000000010,
set b %B0000000000000001,
eval,
output;

set a %B0000000000001001,
set b %B0000000000000011,
eval,
output;

set a %B0000000000000100,
set b %B0000000000000100,
eval,
output;

set a %B1111111111111111,
set b %B1111111111111111,
eval,
output;

set a %B0000000000000101,
set b %B0000000000001000,
eval,
output;
