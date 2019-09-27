//AVA
{include("io_intentions.asl")}
{include("time.asl")}
// !main gets called from environment


+!main <-
    .log("ava from asl");
    .wait(1000);
    !expect_response("/operational/initial_blank", []).


+response(main, initial_query, Entities) <-
    .log("initial query received").









+!capture_user_speech <-
    !expect_response("default/prompt").
    
+response("default/prompt", Intent, Entities) <-
    !expect_response("default/prompt").
