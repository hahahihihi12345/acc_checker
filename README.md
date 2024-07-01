# acc_checker
Check if usernames exist and find potential alts or get their ID code

to use:
  - install python and the selenium package
  
  - enter your credentials in a file named "pass.txt" in the same folder you will be launching this script from
  - username;pasword (no spaces or enters)

  - enter your wanted usernames in a file named "wanted_usernames.txt" in the same folder you will be launching this script from
  - username1;username2;username3... (no spaces or enters)

  - input your desired mode (txt or csv) into the terminal when asked

a short rant about the weird shit I have done in this script and why did I do it:

why open a browser?
to log in. Yes, I can log in without it, but the part that generates the JSON boots me out with a 401 no matter
what I do. After 12 hours I said f*ck it and went this way.

why does it shit itself currently? It doesn't - for now, at least. Yay.
