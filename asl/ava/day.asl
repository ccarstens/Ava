

day_1(thursday).
day_2(friday).

blocked_day(wednesday, work).
blocked_day(thursday, yoga).


+!init_day_options <-
    !first_day_suggestion.


+!first_day_suggestion <-
    day_1(D1);
    day_2(D2);
    blocked_day(D1, BdA);
    dinner_person(X);
    !expect_response("/day/suggest/day_range_overview_1", [blocked_day_2(thursday), day_suggestion_2(friday), blocked_day_1(wednesday), blocked_day_2_activity(yoga), person_name(X)]).


+response(first_day_suggestion, Intent, []) <-
    !second_day_suggestion.
    
+!second_day_suggestion <-
    day_1(D);
    dinner_person(X);
    !expect_response("/day/suggest/pick_second_option_1", [person_name(X), day_suggestion(D)]).

+response(second_day_suggestion, Intent, []) <-
    !init_place_suggestions.
