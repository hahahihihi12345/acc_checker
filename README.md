Warning - I strongly advise using an burner account for these, as Insta will block you from signing in if you overdo it

# Followers
get the usernames of accouunts the root username follows

to use:
  - install python and the selenium library
  
  - enter your credentials in a file named "pass.txt" in the same folder you will be launching this script from
  - username;pasword (no spaces or enters)

  - enter your wanted usernames in a file named "wanted_usernames.txt" in the same folder you will be launching this script from
  - username1;username2;username3... (no spaces or enters)

  - enter any keywords you want to look for in the results into file keywords.txt - empty file = all results without filter
  - <--- KEEP THE KEYWORDS YOU USE TO YOURSELF - THE ENEMY IS LISTENING --->

  - I added a option of recursive search - choose depth by changing its variable at the start of the main() function, default (zero) is normal search
  - A word of warning - this is a feature with exponential complexity - which means it takes a lot of time.
  - This feature has been tested very little and could fail, proceed with caution

# acc_checker
Check if usernames exist and find potential alts or get their ID code

THE ALTS ARE POTENTIAL, MANUALLY VERIFY IF THEY ARE REALLY ALTS

to use:
  - install python and the selenium library
  
  - enter your credentials in a file named "pass.txt" in the same folder you will be launching this script from
  - username;pasword (no spaces or enters)

  - enter your wanted usernames in a file named "wanted_usernames.txt" in the same folder you will be launching this script from
  - username1;username2;username3... (no spaces or enters)

  - input your desired mode (txt or csv) into the terminal when asked

a short rant about the weird shit I have done in this script and why did I do it:

why open a browser?
to log in. Yes, I can log in without it, but the part that generates the JSON boots me out with a 401 no matter
what I do.
