!main.

+!main <-
    .log("user from asl").
    
+!tell_ava(Belief) <-
    .log("passing the following to ava");
    .log(Belief);
    ava(AvaJID);
    .send(AvaJID, tell_response, Belief).
