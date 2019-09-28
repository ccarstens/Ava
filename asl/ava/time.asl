//AVA time
day(tuesday).
day(wednesday).
day(thursday).
day(friday).
day(saturday).

schedule(thursday, arrival_home, "6pm").
suggestion_for_user(time, thursday, "7:30pm").
confirmed(day, thursday).
confirmed(person, "Lauren").

+!find_time_option <-
    .log("init find time option", _);
    confirmed(day, Day);
    schedule(Day, arrival_home, ArrivalHome);
    suggestion_for_user(time, Day, Time);
    !expect_response("/time/suggest/home_arrival_1", [arrival_home(ArrivalHome), suggested_time(Time)]).
    
    
+response(find_time_option, confirmation, InputValues) <-
    .log("confirmation received", _);
    !indicate_switch_person.

    
+!indicate_switch_person <-
    confirmed(person, Person);
    !statement("/operational/switch_person/availability_sharing_1", [person_name(Person), person_pronoun("his"), cutoff_day("Friday")]).
