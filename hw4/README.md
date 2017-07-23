
  1. A page that has a link a user clicks to visit the Google OAuth 2.0 endpoint
  2. A page that handles the user getting redirect back to your website from
   Google's endpoint and handles the exchanging of the access code for a token
  3. A page (which could use the same handler as the page they were redirected
   to) which uses that token to access and display  the following information:
   The users first and last name and the URL to access their Google Plus
   account. It should also print out the value of the state variable that was
   used to secure the original redirect.



   https://www.googleapis.com/auth/userinfo.profile

https://acounts.google.com/o/oauth2/v2/auth?scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Foath-redir&response_type=code&client_id=17036770916-bigvjpd6tn58esbb7fmbmpdq9iivcj5d.apps.googleusercontent.com


 131252496690-oq1f5n3762l9l3n9qvi11qf40f0cm7qj.apps.googleusercontent.com
