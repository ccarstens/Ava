expect_response_counter(0).

+!expect_response(UtteranceID, Options) <-
    usercontroller(UserJID);
    .send(UserJID, expect_response, [UtteranceID, Options]).
