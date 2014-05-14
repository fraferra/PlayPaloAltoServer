## Need to use Login first to get authenticated

Registration - GET http://playpaloalto.com/api/registration/?email={EMAIL}&first_name={FIRST_NAME}&last_name={LAST_NAME}&password={PASSWORD}
        It creates a new user


###  v1 | With normal user authentication handled by the session:

#### Login - GET

It authenticates the user and it redirects to api/v1/home
	
	http://playpaloalto.com/api/v1/login/?username={EMAIL_USER}&password={PASSWORD_USER}

Return structure:

	result['message']
        
#### Leaderboard - GET

It returns the players and their experience

	http://playpaloalto.com/api/v1/leaderboard/

Return structure:

	result['user', 'score', 'experience', 'picture_url', 'players']
	players[player1,player2,....,playern]
	playern['player', player_experience']

####Coupon - GET

It reutrns list of coupons available
If parameter 'id' is passed it will link the coupon linked to that id to the authenticated user and it will update the points of the user (previous points - price of coupon)

	http://playpaloalto.com/api/v1/coupons/
    http://playpaloalto.com/api/v1/coupons/?id=1

Return structure:
	
	result['user','score','experience','picture_url','list_of_coupons'}
	list_of_coupons[1,2,3,...,n]
	n['name',price','location','shop','remaining']
        
####Event - GET
It returns the events going on
If paramenter 'id' is passed it will add the event to the events of the authenticated user

	http://www.playpaloalto.com/api/v1/events/
    http://playpaloalto.com/api/v1/events/?id=1

Return structure
	
	result['user','score','experience','picture_url','list_events']
	list_events[1,2,3,...,n]
	n['name','location','points','experience']

***

### v2 - If we can't authenticate the user automatically with sessions we will use the token provided by api/v2/

Login - GET http://playpaloalto.com/api/v2/login/?username={EMAIL_USER}&password={PASSWORD_USER}
        It authenticates the user and it returns a json dictonary with a key called 'token' equal to a string randomly            generated of 30 characters. Store the token for future authentication
        
Leaderboard - GET http://playpaloalto.com/api/v2/leaderboard/?token={TOKEN_STORED}
        It returns the players and their experience

Coupon - GET http://playpaloalto.com/api/v2/coupons/?token={TOKEN_STORED}
        It reutrns list of coupons available
        If parameter 'id' is passed it will link the coupon linked to that id to the authenticated user and it will update         the points of the user (previous points - price of coupon)
        example: GET http://playpaloalto.com/api/v2/coupons/?id=1&token={TOKEN_STORED}
        
Event - GET http://www.playpaloalto.com/api/v2/events/?token={TOKEN_STORED}
        It returns the events going on
        If paramenter 'id' is passed it will add the event to the events of the authenticated user
        example: GET http://playpaloalto.com/api/v2/events/?id=1&token={TOKEN_STORED}
