
# ToDo:

  1. Use Cases
  2. Tests

For this option you will only build a cloud back-end on a live publicly accessible cloud provider.

    You need to implement a REST API
    User accounts are supported (ie. there is data tied to specific users that only they can see or modify) AND the account system uses 3rd party provider, there should be able to be an arbitrary number of accounts. Accounts *must* have access to some amount of account specific information that only they can either access or modify.
    There should be at least 2 entities and they should have at least 4 properties each
    You must also implement one of the following
        There should be at least one relationship between entities
        It needs to meaningfully use a 3rd party API for something other than authentication (for example connecting to a stock market API to get stock data or a weather service to pull weather data)

Deliverables

    You should include a full set of Postman tests that show adding, deleting, updating and removing entities (every applicable verb should be used)
        This should demonstrate adding, viewing and removing things in a relationship (if applicable)
        You will need to use some more advanced features of postman to do this because you will need to pull variable names and save them to variables
    You should include a PDF
        With all the routes used for your API including which verbs work for them
        A description of the 3rd party service you used
    You should include a video of the tests being run in case we are unable to run or interpret the results.
    You should include a zip of your source code

Use Cases
=========

  R1) User should be able to login into their account via google+ login.

  R2) Visitors will be prompted to login via the google account on the home page.

  R3) Once logged in users will be able to choose a user name which will be
  associated with tweets they save.

  R4) Users should be able to search and find tweets for specific words from a
  specified date range.

  R5) Users should be able to save specific tweets that they found to their user
  page.

  R6) Users and non-users can also see saved tweets by other users on the main page
  as well as on individual user pages.

Tests
=====
  1. Creating a User Profile
    - Updating a user profile
  2. Searching a tweets for specific words and from certain dates
  3. Saving a tweet
  4. Viewing saved Tweets
    - Home page
    - User page


Models
======
  Tweets
    - author
    - body - tweet body
    - date tweeted
    - date saved
    - user - user who saved the tweet

  Users
    - User name
    - Favorite Color
    - Location
    - Saved Tweets
