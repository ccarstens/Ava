//AVA
{include("io_intentions.asl")}
{include("time.asl")}
// !main gets called from environment


+!main <-
    .log("ava from asl", _);
    .wait(1000);
    !find_time_option.





+!capture_user_speech <-
    !expect_response("default/prompt").
    
+response("default/prompt", Intent, Entities) <-
    !expect_response("default/prompt").
