!main.

+!main <-
    .log("Hello, this is User Agent").



+!tell_ava(Belief) <-
    .print("I should tell ava this:");
    .print(Belief);
    ava(AvaJID);
    .send(AvaJID, tell, Belief).