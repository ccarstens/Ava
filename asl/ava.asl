{include("beliefs.asl")}

started(no).
temperature(now, 66, cloudy).
temperature(today_evening, 57, "clear skies").

!stringtest.

+!stringtest <-
    beliefs(FF);
    .print(FF);
    temperature(now, Temp, Condition);
    .concat("It's currently ", Condition, " and ", Temp , " degrees.", X);
    .print(X);
    temperature(today_evening, Temp2, Condition2);
    .concat("In the evening there will be ", Condition2, " and ", Temp2 , " degrees.", Y);
    .print(Y).

+!main: started(yes) <-
    .log("Hello, this is Ava", _);
    !!myloop;
    !expect_response("hello_1", Response);
    .log(Response, _).



+!myloop <-
    .wait(200);
    .print(".");
    !myloop.

+!expect_response(UtteranceID, Response) <-
    usercontroller(UserJID);
    .send(UserJID, getuserinput, UtteranceID);
    while(not responded(_)){
        .wait(400);
        .print("waiting for response");
    };
    responded(Response);
    -responded(Response).


+responded_hello_1(temperature_set) <-
    .log("I am setting the temperature", _).


+responded_hello_1(temperature_get) <-
    temperature(now, Temp, Condition);
    .concat("It's currently ", Condition, " and ", Temp , " degrees.", X);
    .log(X, _).