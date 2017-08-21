Tweeter
========

http://tweet-saver.appspot.com/index.html

The application I decided to write for my final project is a simple web
application that allows visitors to sign in with their Google+ accounts
and then make Tweets from a Twitter account
[TwetTweetTweeet](https://twitter.com/TwetTweetTweeet/)! Essentially its
everyone can pretend to Tweet from a single twitter account without
having to log in!

Users sign in with their Google+ account and can update their profile, user
name, location, favorite color, and then can create Tweets using that profile.
The application uses the twitter API to post status updates (tweets)
to the account above. When a user posts a tweet using the application, that
tweet will be associated to them. Users can update their account, but only
if they have the access code present, furthermore users can only make tweets
if they have an access code.

I'm looking forward to seeing the tweets that you all make when you grade this,
so be sure to make them fun! :)

## Using the Site

The application is currently just a RESTFul API, so its core functionality
is only accessible via Postman or another similar application.

To use it however you must visit to the web page provided above with a  browser
to sign in using the Google+ Oauth API. Once you have done that you need to copy
and paste your access token into post man tests in the *test* section of the
**Start Test** test. You will also need to specify unique tweets that will be
used for the test suite that you run. After you do that, run the test suite.

These values will be in the same area as where the access token is pasted. Each
tweet will need to be unique, because Twitter will through a fit if you try
and post the two tweets with the same content!

So here is how to run the tests is a succinct format:

1. Get your access token: Navigate to [http://tweet-saver.appspot.com/index.html](http://tweet-saver.appspot.com/index.html)
  and click the **Log-In** in the nav bar and follow the google plus prompts to
  allow access to your google+ account. Copy your access token, the wibsite
  will display it for you after you've signed in, and paste it into the Postman
  test section of the **Start Test** test.
2. Create Tweets: In the same section you provided your access token create
  three different and unique tweets that will be tweeted by the account
3. Run the tests! And see your tweets that you tweeted on the     
  [account](https://twitter.com/TwetTweetTweeet/)
4. Boom Shakalak!

# API Reference

## Profile

### Create a Profile
```
POST /profile
```
With the following attributes in the body of the request:

Name        | Type        | Description
------------|:-----------:|--------------:
userName (Required) | String      | Your desired user name
color       | String      | Your favorite color
loc         | String      | Your location


And the authorization token in the header of the request:

Name        | Type        | Description
------------|:-----------:|--------------:
token | String | A valid authorization token provided by website. See above.


### List all Profiles
```
GET /profile
```

### List a single Profile
```
GET /profile/:id/
```

### Modify a Profile
```
PATCH /profile/:id/
```

Name              | Type    | Description
------------------|:-------:|--------------:
Color (optional)   | String  | Updated favorite color
loc (optional)   | String  | Updated location

### Delete a Profile
```
DELETE /profile/:id/
```

## Tweets

### Post a Tweet
```
POST /tweet/:user_id/
```

Name        | Type        | Description
------------|:-----------:|--------------:
Body | String | Body of the tweet to be tweeted!

### List all Tweets
```
GET /tweet
```

### List a single Tweet
```
GET /tweet/:tweet_id
```

### List the Tweets by a specific user
```
GET /profile/:user_id/tweets/
```
