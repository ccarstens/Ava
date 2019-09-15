started(yes).
!main.


+!main <-
    .log("Hello, this is Ava", _);
    !myloop.



+!myloop <-
    .wait(200);
    .print(".");
    !myloop.


