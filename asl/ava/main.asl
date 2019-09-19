//AVA
{include("io_intentions.asl")}
{include("time.asl")}
// !main gets called from environment



+!main <-
    .log("ava from asl", _);
    .wait(3000);
    hello(First, Second);
    [A|B] = First;
    .print(A);
    .print(B);
    !find_time_option.
