

potential_place(r1, "Falafel and Friends", "Mitte").
potential_place(r2, "Frea", "Mitte").
potential_place(r3, "Paolo Pinkel", "Neukoelln").

recommendation_via_message(r1, "Julia", "the other day").
place_context(r2, "vegan zero-waste restaurant").
place_context(r3, "combines three different cuisines and always has vegan options").
place_visits(r2, "a couple of times").



+!init_place_suggestions <-
    !request_place_preference.
    
+!request_place_preference <-
    !expect_response("/place/request_preference", []).

+response(request_place_preference, Intent, []) <-
    !first_place_suggestion;
    .wait(500);
    !second_place_suggestion;
    .wait(500);
    !third_place_suggestion;
    !request_place_option_choice.


+!first_place_suggestion <-
    potential_place(r1, Name1, Nbhd1);
    recommendation_via_message(r1, ReferringP1, ReferringTime1);
    !statement("/place/suggest/with_context/referral/friend_1", [place_name(Name1), place_nbhd(Nbhd1), referring_friend(ReferringP1), time_period_ago(ReferringTime1)]).
    
+response(first_place_suggestion, Intent, []) <-
    !second_place_suggestion.
    
    
+!second_place_suggestion <-
    potential_place(r2, Name2, _);
    place_context(r2, Traits2);
    place_visits(r2, Visits2);
    !statement("/place/suggest/with_context/frequency/medium_traits_1", [place_name(Name2), place_traits(Traits2), frequency_visits(Visits2)]).

+response(second_place_suggestion, Intent, []) <-
    !third_place_suggestion.
    



+!third_place_suggestion <-
    potential_place(r3, Name3, Nbhd3);
    place_context(r3, Traits3);
    !statement("/place/suggest/with_context/novelty_far_vs_traits/medium_1", [place_name(Name3), place_nbhd(Nbhd3), place_traits(Traits3)]).
    

    
+!request_place_option_choice <-
    !expect_response("/place/choice/request_1", []).

+response(request_place_option_choice, Intent, []) <-
    !indicate_discuss_places_with_person.
    
    
    
+!indicate_discuss_places_with_person <-
    dinner_person(X);
    !statement("/place/choice/confirm_user_choice_1", [options_count("both"), person_name(X)]);
    !init_time_suggestions.
