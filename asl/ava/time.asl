//AVA time
day(tuesday).
day(wednesday).
day(thursday).
day(friday).
day(saturday).

schedule(thursday, arrival_home, "6pm").
suggestion_for_user(time, thursday, "7:30pm").
confirmed(day, thursday).

+!find_time_option <-
    .log("init find time option", _);
    confirmed(day, Day);
    schedule(Day, arrival_home, ArrivalHome);
    suggestion_for_user(time, Day, Time);
    !expect_response("time_suggestion_based_on_home_arrival_1", [ArrivalHome, Time], Response);
    .log(Response, _).
    
