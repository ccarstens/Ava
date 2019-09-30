//AVA
{include("io_intentions.asl")}
{include("time.asl")}
{include("day.asl")}
{include("place.asl")}
// !main gets called from environment


dinner_person(david).
pronouns(david, "he", "his", "him").


+!main <-
    .log("ava from asl", _);
    .wait(1000);
    // !find_time_option.
    // !request_place_option_choice.
    // !summary_availability_sharing.
    // !first_day_time_suggestion.
    !expect_response("/operational/initial_blank", []).


+!accept_query <-
    // !statement("/query/accept/1", []);
    !init_day_options.
    

+response(main, Intent, Entities) <-
    !accept_query.








+!capture_user_speech <-
    !expect_response("default/prompt").
    
+response("default/prompt", Intent, Entities) <-
    !expect_response("default/prompt").
