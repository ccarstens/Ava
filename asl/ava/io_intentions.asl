expect_response_counter(0).

+!expect_response(UtteranceID, Options, Response) <-
    .print(Options);
    usercontroller(UserJID);
    .send(UserJID, expect_response, [UtteranceID, Options]);
    while(not responded(_)){
        
        expect_response_counter(X);
        .modulo(X, 33, MR);
        if(MR == 0){
            .print(".");
        };
        -+expect_response_counter(X+1);
    };
    responded(Response);
    -responded(Response).
