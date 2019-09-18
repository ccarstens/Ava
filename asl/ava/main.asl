//AVA
{include("io_intentions.asl")}
{include("time.asl")}
!main.



+!main <-
    .log("ava from asl", _);
    .wait(1000);
    !find_time_option.
