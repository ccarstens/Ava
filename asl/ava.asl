{include("beliefs.asl")}

started(no).
temperature(now, 66, cloudy).
temperature(today_evening, 57, "clear skies").

myliteral(started).

important_id("greeting_2").

# !stringtest.

+!stringtest <-
    myliteral(Value);
#    Value(StartValue);
    .print(StartValue).

+!main: started(yes) <-
    .log("Hello, this is Ava");

    !expect_response("offer_help_1", Response);
    .log("finished");
    .log("now we can do other things, like looping");
    !myloop.



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
    while(not statement_finished(UtteranceID, Context, yes)){
        .wait(33);
        .print("waiting for statement to finish");
    };
    .log("I CAN CONTINUE NOW");
    -+statement_finished(UtteranceID, Context, yes);
    statement_finished(UtteranceID, Context, Finished).

+responded_hello_1(temperature_set) <-
    .log("I am setting the temperature").


+responded_hello_1(temperature_get) <-
    ?temperature(now, Temp, Condition);
    .concat("It's currently ", Condition, " and ", Temp , " degrees.", X);
    .log(X).

    
+responded_offer_help_1("temperature_get") <-
    .print("no probs here");
    !statement("tell_weather_1", response, Status).

+responded_offer_help_1(Sth) <-
    .print("HEREEE").



+statement_finished("greeting_2", Context, Status) <-
    .print("CHHAAAANGE");
    .print(Context);
    .print(Status).
