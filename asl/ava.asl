started(no).


+!main: started(yes) <-
    .log("Hello, this is Ava", _);
    !!myloop;
    !expect_response("hello-1", Response);
    !expect_response("hello-1", Response);
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

