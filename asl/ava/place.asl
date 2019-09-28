

potential_place(r1, "Hummus and Friends", "Mitte").
potential_place(r2, "Frea", "Mitte").
potential_place(r3, "Paolo Pinkel & das Schnabulat", "Neukoelln").

recommendation_via_message(r1, "Nicholas", "the other day").
place_context(r2, "vegan zero-waste restaurant").
place_context(r3, "combines three different cuisines and always has vegan options").
place_visits(r2, "a couple of times").



+!init_place_suggestions <-
    !request_place_preference.
    
+!request_place_preference <-
    !expect_response("/place/request_preference", []).

+response(request_place_preference, confirm, []) <-
    !first_place_suggestion.

+response(request_place_preference, ask_for_suggestions, []) <-
    !first_place_suggestion.


+!first_place_suggestion <-
    potential_place(r1, Name, Nbhd);
    recommendation_via_message(r1, ReferringP, ReferringTime);
    !expect_response("/place/suggest/with_context/referral/friend_1", [place_name(Name), place_nbhd(Nbhd), referring_friend(ReferringP), time_period_ago(ReferringTime)]).
    
+response(first_place_suggestion, Intent, []) <-
    !second_place_suggestion.
    
    
+!second_place_suggestion <-
    potential_place(r2, Name, _);
    place_context(r2, Traits);
    place_visits(r2, Visits);
    !expect_response("/place/suggest/with_context/frequency/medium_traits_1", [place_name(Name), place_traits(Traits), frequency_visits(Visits)]).

+response(second_place_suggestion, Intent, []) <-
    !third_place_suggestion.
    



+!third_place_suggestion <-
    potential_place(r3, Name, Nbhd);
    place_context(r3, Traits);
    !expect_response("/place/suggest/with_context/novelty_far_vs_traits/medium_1", [place_name(Name), place_nbhd(Nbhd), place_traits(Traits)]).
    
+response(third_place_suggestion, Intent, []) <-
    !request_place_option_choice.
    
+!request_place_option_choice <-
    !expect_response("/place/choice/request_1", []).

+response(request_place_option_choice, Intent, []) <-
    !indicate_discuss_places_with_person.
    
    
    
+!indicate_discuss_places_with_person <-
    dinner_person(X);
    !statement("/place/choice/confirm_user_choice_1", [options_count("both"), person_name(X)]);
    !init_time_suggestions.
