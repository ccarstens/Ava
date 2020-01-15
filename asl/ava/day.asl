

day_1(wednesday).
day_2(friday).

blocked_day(thursday, yoga).


+!init_day_options <-
    !first_day_suggestion.


+!first_day_suggestion <-
    day_1(D1);
    day_2(D2);
    blocked_day(Bd, BdA);
    dinner_person(X);
    !expect_response("/day/suggest/day_range_overview_1", [day_suggestion_1(D1), day_suggestion_2(D2), blocked_day_1(Bd), blocked_day_1_activity(BdA), person_name(X)]).


+response(first_day_suggestion, confirm, []) <-
    !second_day_suggestion.
    
+!second_day_suggestion <-
    day_1(D);
    dinner_person(X);
    !expect_response("/day/suggest/pick_second_option_1", [person_name(X), day_suggestion(D)]).

+response(second_day_suggestion, confirm, []) <-
    !init_place_suggestions.
