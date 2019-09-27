expect_response_counter(0).
statement_iterator(0).

+!expect_response(UtteranceID, FillIns) <-
    usercontroller(UserJID);
    .get_parent_intention(PI);
    .send(UserJID, expect_response, [utterance_id(UtteranceID), eliciting_intention(PI), fill_ins(FillIns)]).

+!expect_response(UtteranceID) <-
    !expect_response(UtteranceID, []).

+!statement(UtteranceID, FillIns) <-
    usercontroller(UserJID);
    .get_parent_intention(PI);
    .send(UserJID, statement, [utterance_id(UtteranceID), eliciting_intention(PI), fill_ins(FillIns)]);
    -+statement_finished(UtteranceID, no);
    while(not statement_finished(UtteranceID, yes)){
        statement_iterator(X);
        if(X mod 33 == 0){
            .log(".");
        }
        -+statement_iterator(X + 1);
    };
    -+statement_iterator(0);
    .concat("received signal ", UtteranceID, " finished", LogMessage);
    .log(LogMessage).
