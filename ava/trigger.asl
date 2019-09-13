initiated(yes).
level(0).
delay(1000).
position(7).
goal(10).
specialpos(0).

cornelius(mya).
cornelius(carstens).
cornelius(12).

day(monday).
day(tuesday).
day(wednesday).
day(thursday).
day(friday).
day(saturday).
day(sunday).


event(monday).
event(saturday).
event(friday).

#!main.

free_days(X) :- day(X) & not event(X).

#!send_test.

!mmm.

+!mmm <-
    .print("YESS").

+!send_test <-
    #!!position(50);
    .send("lauren@localhost", getuserinput, choose("Welche?", ["Zero Zero", "Beretta", "Mannys"]));
    !get_response(X);
    .print("the user chose: ", X);
    .send("lauren@localhost", getuserinput, choose("Uhrzeit?", ["19:00", "20:00"]));
    !get_response(Y);
    .print("the user chose: ", Y).


+!get_response(X) <-
    while(not responded(_)){
        .wait(33);
    };
    responded(X);
    -responded(X).



+!main <-
    .custom_action(8);
    .ask_user_a("how are you", PP);
    .print(PP);
    .findall(X, free_days(X), Days);
    .list(Days);
    .ask_user_options("Which option do you want?", Days, R);
#    for(.member(D, Days)){
#        .print("Dieser Tag ist frei: ", D);
#    };
    .print("The user chose: ", R).



+!start2 <-
    .print("start 2");
    .wait(5000);
    !position(15);
    -start3;
    .print("end start 2").

+!start3 <-
    .print("preparing sabotage");
    .wait(5000);
    .print("executing sabotage");
    -long_achievement.


+!start <-
    .b_function(2, W);
    .print(W);
    .print("Starting...");
    .my_test(100, X);
    .your_test(102, Y);
    .print(X);
    .print(Y);
    .ask_user("What do you want?: ", Z);
    .print("The user wants ", Z).

+!next_stage(Msg)[source(Sender)]  <-
    .print("NEXT STAGE INITIATED ", Msg).


+!hello(Msg)[source(Sender)]
 <-
  .print("got a message from", Sender, "saying:\n", Msg).

+!level(X) :
    level(X) <-
        .print("achieved").

+!level(X) :
    level(Y) & (Y <= X)
    <-
    .print("Goal: ", X);
    level(Current);
    .print("Current: ", Current);
    .wait(1000);
    -level(Current);
    +level(Current + 1);
    !level(X).


+!position(Z): position(Z) <-
    .print("ARRIVED").

+!position(Z) :
    position(X) &
    X > Z
    <-
    .print("Current Position: ", X);
    .print("Goal: ", Z);
    .print("Decreasing Position");
    -+position(X - 1);
    !mywait;
    !position(Z).


+!position(Z) :
    position(X) &
    X < Z
    <-
    .print("Current Position: ", X);
    .print("Goal: ", Z);
    .print("Increasing Position");
    -+position(X + 1);
    !mywait;
    !position(Z).

+position(11) <-
    .print("11 is a great number").


+!mywait <-
    delay(X);
    .wait(X).


+!long_achievement :
    initiated(yes)
    <-
    .print("Started long achievement");
    .wait(2000);
    initiated(X);
    .print("Stage 2 of long achievement ", X);
    .wait(2000);
    initiated(Y);
    .print("Stage 3 of long achievement ", Y);
    .wait(2000);
    initiated(Z);
    .print("Stage 4 of long achievement ", Z);
    .wait(2000);
    initiated(A);
    .print("Stage 5 of long achievement ", A);
    .wait(2000);
    initiated(B);
    .print("Stage 6 of long achievement ", B);
    .wait(2000);
    initiated(C);
    .print("Stage 7 of long achievement ", C);
    .wait(2000);
    initiated(D);
    .print("Stage 8 of long achievement ", D);
    .wait(2000);
    .print("ENDED LONG ACHIEVEMENT").



+!specialpos(10): specialpos(X)
    <-
    -+specialpos(X + 5);
    specialpos(5).





