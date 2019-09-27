!main.

+!main <-
    .log("user from asl", _).
    
+!tell_ava(Belief) <-
    .log("passing the following to ava", _);
    .log(Belief);
    ava(AvaJID);
    .send(AvaJID, tell_response, Belief).
