{include("beliefs.asl")}

started(no).
temperature(now, 66, cloudy).
temperature(today_evening, 57, "clear skies").

myliteral(started).

# !stringtest.

+!stringtest <-
    myliteral(Value);
#    Value(StartValue);
    .print(StartValue).

+!main: started(yes) <-
    .log("Hello, this is Ava", _);
    !statement("greeting_1", main, Finished);
    .log(Finished, _).



+!myloop <-
    .wait(200);
    .print(".");
    !myloop.

+!expect_response(UtteranceID, Response) <-
    usercontroller(UserJID);
    .send(UserJID, expect_response, UtteranceID);
    while(not responded(_)){
        .wait(33);
        .print("waiting for response");
    };
    responded(Response);
    -responded(Response).

+!statement(UtteranceID, Context, Finished) <-
    usercontroller(UserJID);
    .send(UserJID, statement, UtteranceID);
    -+statement_finished(UtteranceID, Context, no);
    while(not statement_finished(UtteranceID, _, yes)){
        .wait(33);
        .print("waiting for statement to finish");
    };
    -+statement_finished(UtteranceID, Context, yes);
    statement_finished(UtteranceID, Context, Finished).

+responded_hello_1(temperature_set) <-
    .log("I am setting the temperature", _).


+responded_hello_1(temperature_get) <-
    temperature(now, Temp, Condition);
    .concat("It's currently ", Condition, " and ", Temp , " degrees.", X);
    .log(X, _).