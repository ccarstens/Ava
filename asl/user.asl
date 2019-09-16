!main.

+!main <-
    .log("Hello, this is User Agent", _).



+!tell_ava(Belief) <-
    ava(AvaJID);
    .send(AvaJID, tell, Belief).