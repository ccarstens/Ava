expect_response_counter(0).
statement_iterator(0).

+!expect_response(UtteranceID, FillIns) <-
    usercontroller(UserJID);
    .send(UserJID, expect_response, [UtteranceID, FillIns]).

+!statement(UtteranceID, FillIns) <-
    usercontroller(UserJID);
    .send(UserJID, statement, [UtteranceID, FillIns]);
    -+statement_finished(UtteranceID, no);
    statement_iterator(X);
    while(not statement_finished(UtteranceID, yes)){
        if(X mod 33 == 0){
            .log(".", _);
        }
        -+statement_iterator(X + 1);
    };
    -+statement_iterator(0);
    .concat("received signal ", UtteranceID, " finished", LogMessage);
    .log(LogMessage, _).
