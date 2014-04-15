PlayPaloAlto_server
===================



APIs:


THE USERS NEED TO USE Login BEFORE TO GET AUTHENTICATED 

Registration - GET http://playpaloalto.com/api/registation/?email={EMAIL}&first_name={FIRST_NAME}&last_name={LAST_NAME}&password={PASSWORD}
        It creates a new user

Login - GET http://playpaloalto.com/api/login/?username={EMAIL_USER}&password={PASSWORD_USER}
        It authenticates the user and it returns a json dictonary with a key called 'token' equal to a string randomly            generated of 30 characters. Store the token for future authentication
        
Leaderboard - GET http://playpaloalto.com/api/leaderboard/?token={TOKEN_STORED}
        It returns the players and their experience

Coupon - GET http://playpaloalto.com/api/coupons/?token={TOKEN_STORED}
        It reutrns list of coupons available
        If parameter 'id' is passed it will link the coupon linked to that id to the authenticated user and it will update         the points of the user (previous points - price of coupon)
        example: GET http://playpaloalto.com/api/coupons/?id=1&token={TOKEN_STORED}
        
Event - GET http://www.playpaloalto.com/api/events/?token={TOKEN_STORED}
        It returns the events going on
        If paramenter 'id' is passed it will add the event to the events of the authenticated user
        example: GET http://playpaloalto.com/api/events/?id=1&token={TOKEN_STORED}
