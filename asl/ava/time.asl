//AVA time

+!find_time_option <-
    .log("init find time option", _);
    !expect_response("time_suggestion_based_on_home_arrival_1", [], Response);
    .log(Response, _).
    
