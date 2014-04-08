PlayPaloAlto_server
===================



APIs:

Registration - GET http://www.playpaloalto.com/api/registation/?email={EMAIL}&first_name={FIRST_NAME}&last_name={LAST_NAME}&password={PASSWORD}
        It creates a new user

Login - GET http://www.playpaloalto.com/api/login/?username={EMAIL_USER}&password={PASSWORD_USER}
        It authenticates the user
        
Leaderboard - GET http://www.playpaloalto.com/api/leaderboard/
        It returns the players and their experience

Coupon - GET http://www.playpaloalto.com/api/coupons/
        It reutrns list of coupons available
        If parameter 'id' is passed it will link the coupon linked to that id to the authenticated user and it will update the points of the user (previous points - price of coupon)
        example: GET http://www.playpaloalto.com/api/coupons/?id=1 
        
Event - GET http://www.playpaloalto.com/api/events
        It returns the events going on
        If paramenter 'id' is passed it will add the event to the events of the authenticated user
        example: GET http://www.playpaloalto.com/api/events/?id=1
