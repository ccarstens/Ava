possible_dinner(wednesday, "7:30pm", "8:00pm").


+!init_time_suggestions <-
    !request_time_commitment_preference.
    
+!request_time_commitment_preference <-
    !expect_response("/time/request_time_commitment_1", []).
    
+response(request_time_commitment_preference, Intent, []) <-
    !first_day_time_suggestion.
    
+!first_day_time_suggestion <-
    day_1(Day);
    possible_dinner(Day, StartInt, EndInt);
    !expect_response("/time/suggest/with_context/home_arrival_1", [
        day_option(Day), 
        time_interval_start(StartInt), 
        time_interval_end(EndInt)
    ]).
    
+response(first_day_time_suggestion, Intent, []) <-
    !summary_availability_sharing.
    

+!summary_availability_sharing <-
    day_1(D1);
    day_2(D2);
    dinner_person(X);
    possible_dinner(D1, Start, End);
    potential_place(r2, P1, _);
    potential_place(r3, P2, _);
    pronouns(X, _, _, Pronoun);
    !expect_response("/operational/switch_person/availability_sharing_1", [
        person_name(X),
        day_option_1(D1),
        day_option_2(D2),
        time_interval_start(Start),
        time_interval_end(End),
        person_pronoun(Pronoun),
        place_option_1(P1),
        place_option_2(P2),
        cutoff_day(D2)
    ]).
    
    
+response(summary_availability_sharing, Intent, []) <-
    !indicate_return_after_first_round.
    
    
+!indicate_return_after_first_round <-
    !statement("/operational/switch_person/indicate_return", []).


    
    
    
    
